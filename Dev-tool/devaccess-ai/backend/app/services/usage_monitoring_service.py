"""
Usage Monitoring Service - Track free tier usage and generate alerts
"""
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
import httpx
import structlog

from app.models.account import DevAccount
from app.models.enhanced_models import UsageMetric, UsageAlert, AlertTypeEnum
from app.models.software import Software
from app.core.config import settings
from app.services.notification_service import NotificationService

logger = structlog.get_logger()


class UsageMonitoringService:
    """Service for monitoring free tier usage and generating alerts"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.notification_service = NotificationService()
        
        # Built-in monitoring strategies for popular services
        self.monitoring_strategies = {
            "vercel": self._monitor_vercel_usage,
            "netlify": self._monitor_netlify_usage,
            "heroku": self._monitor_heroku_usage,
            "supabase": self._monitor_supabase_usage,
            "planetscale": self._monitor_planetscale_usage,
            "railway": self._monitor_railway_usage,
            "render": self._monitor_render_usage,
        }

    async def monitor_all_accounts(self) -> Dict[str, Any]:
        """Monitor usage for all active accounts"""
        
        logger.info("Starting usage monitoring for all accounts")
        
        # Get all active dev accounts
        result = await self.db.execute(
            select(DevAccount).where(
                and_(
                    DevAccount.status == "active",
                    DevAccount.is_verified == True
                )
            )
        )
        accounts = result.scalars().all()
        
        monitoring_results = {
            "total_accounts": len(accounts),
            "monitored": 0,
            "errors": 0,
            "alerts_generated": 0,
            "results": []
        }
        
        for account in accounts:
            try:
                result = await self.monitor_account_usage(account)
                monitoring_results["results"].append(result)
                monitoring_results["monitored"] += 1
                monitoring_results["alerts_generated"] += result.get("alerts_generated", 0)
                
            except Exception as e:
                logger.error(f"Error monitoring account {account.id}: {e}")
                monitoring_results["errors"] += 1
        
        logger.info(
            "Usage monitoring completed",
            total_accounts=monitoring_results["total_accounts"],
            monitored=monitoring_results["monitored"],
            errors=monitoring_results["errors"],
            alerts_generated=monitoring_results["alerts_generated"]
        )
        
        return monitoring_results

    async def monitor_account_usage(self, account: DevAccount) -> Dict[str, Any]:
        """Monitor usage for a specific account"""
        
        software_name = account.software.name.lower() if account.software else ""
        
        result = {
            "account_id": account.id,
            "software": software_name,
            "metrics_updated": 0,
            "alerts_generated": 0,
            "status": "success",
            "error": None
        }
        
        try:
            # Use specific monitoring strategy if available
            if software_name in self.monitoring_strategies:
                metrics = await self.monitoring_strategies[software_name](account)
            else:
                # Generic monitoring approach
                metrics = await self._generic_usage_monitoring(account)
            
            # Update or create usage metrics
            for metric_data in metrics:
                await self._update_usage_metric(account, metric_data)
                result["metrics_updated"] += 1
            
            # Check for alerts
            alerts = await self._check_usage_alerts(account)
            result["alerts_generated"] = len(alerts)
            
        except Exception as e:
            result["status"] = "error"
            result["error"] = str(e)
            logger.error(f"Error monitoring account {account.id}: {e}")
        
        return result

    async def _monitor_vercel_usage(self, account: DevAccount) -> List[Dict[str, Any]]:
        """Monitor Vercel usage via API"""
        
        # Try to get API token from stored credentials
        api_token = await self._get_api_credential(account, "api_token")
        if not api_token:
            logger.warning(f"No API token found for Vercel account {account.id}")
            return []
        
        metrics = []
        
        try:
            async with httpx.AsyncClient() as client:
                headers = {"Authorization": f"Bearer {api_token}"}
                
                # Get team/user info and usage
                response = await client.get(
                    "https://api.vercel.com/v2/user",
                    headers=headers,
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Extract usage metrics
                    if "usage" in data:
                        usage = data["usage"]
                        
                        # Build minutes
                        if "buildTime" in usage:
                            metrics.append({
                                "metric_name": "build_minutes",
                                "current_usage": usage["buildTime"] / 60000,  # Convert from ms to minutes
                                "limit_value": 6000,  # Free tier limit
                                "unit": "minutes",
                                "data_source": "api"
                            })
                        
                        # Bandwidth
                        if "bandwidth" in usage:
                            metrics.append({
                                "metric_name": "bandwidth_gb",
                                "current_usage": usage["bandwidth"] / (1024**3),  # Convert to GB
                                "limit_value": 100,  # Free tier limit
                                "unit": "GB",
                                "data_source": "api"
                            })
                        
                        # Function invocations
                        if "executions" in usage:
                            metrics.append({
                                "metric_name": "function_invocations",
                                "current_usage": usage["executions"],
                                "limit_value": 125000,  # Free tier limit
                                "unit": "invocations",
                                "data_source": "api"
                            })
                
        except Exception as e:
            logger.error(f"Error monitoring Vercel usage for account {account.id}: {e}")
        
        return metrics

    async def _monitor_supabase_usage(self, account: DevAccount) -> List[Dict[str, Any]]:
        """Monitor Supabase usage"""
        
        api_key = await self._get_api_credential(account, "service_role_key")
        project_url = await self._get_api_credential(account, "project_url")
        
        if not api_key or not project_url:
            return []
        
        metrics = []
        
        try:
            async with httpx.AsyncClient() as client:
                headers = {
                    "apikey": api_key,
                    "Authorization": f"Bearer {api_key}"
                }
                
                # Get database usage (simplified - actual API might differ)
                response = await client.get(
                    f"{project_url}/rest/v1/rpc/get_usage_stats",
                    headers=headers,
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Database rows
                    if "database_rows" in data:
                        metrics.append({
                            "metric_name": "database_rows",
                            "current_usage": data["database_rows"],
                            "limit_value": 500000,  # Free tier limit
                            "unit": "rows",
                            "data_source": "api"
                        })
                    
                    # Storage
                    if "storage_gb" in data:
                        metrics.append({
                            "metric_name": "storage_gb",
                            "current_usage": data["storage_gb"],
                            "limit_value": 1,  # Free tier limit
                            "unit": "GB",
                            "data_source": "api"
                        })
                
        except Exception as e:
            logger.error(f"Error monitoring Supabase usage for account {account.id}: {e}")
        
        return metrics

    async def _generic_usage_monitoring(self, account: DevAccount) -> List[Dict[str, Any]]:
        """Generic usage monitoring for services without specific API integration"""
        
        # This could involve web scraping the dashboard or other methods
        # For now, return empty list - can be expanded with generic scraping
        logger.info(f"Generic monitoring not yet implemented for {account.software.name}")
        return []

    async def _update_usage_metric(self, account: DevAccount, metric_data: Dict[str, Any]):
        """Update or create a usage metric"""
        
        # Check if metric already exists
        result = await self.db.execute(
            select(UsageMetric).where(
                and_(
                    UsageMetric.dev_account_id == account.id,
                    UsageMetric.metric_name == metric_data["metric_name"]
                )
            )
        )
        metric = result.scalar_one_or_none()
        
        if metric:
            # Update existing metric
            metric.current_usage = metric_data["current_usage"]
            metric.limit_value = metric_data.get("limit_value", metric.limit_value)
            metric.unit = metric_data.get("unit", metric.unit)
            metric.data_source = metric_data.get("data_source", "api")
            metric.last_updated = datetime.utcnow()
            metric.last_checked = datetime.utcnow()
            
            # Calculate percentage
            if metric.limit_value and metric.limit_value > 0:
                metric.usage_percentage = (metric.current_usage / metric.limit_value) * 100
                metric.is_warning = metric.usage_percentage >= 75
                metric.is_critical = metric.usage_percentage >= 90
            
        else:
            # Create new metric
            usage_percentage = 0
            is_warning = False
            is_critical = False
            
            if metric_data.get("limit_value") and metric_data["limit_value"] > 0:
                usage_percentage = (metric_data["current_usage"] / metric_data["limit_value"]) * 100
                is_warning = usage_percentage >= 75
                is_critical = usage_percentage >= 90
            
            metric = UsageMetric(
                dev_account_id=account.id,
                metric_name=metric_data["metric_name"],
                current_usage=metric_data["current_usage"],
                limit_value=metric_data.get("limit_value"),
                unit=metric_data.get("unit"),
                usage_percentage=usage_percentage,
                is_warning=is_warning,
                is_critical=is_critical,
                data_source=metric_data.get("data_source", "api"),
                last_updated=datetime.utcnow(),
                last_checked=datetime.utcnow()
            )
            
            self.db.add(metric)
        
        await self.db.commit()

    async def _check_usage_alerts(self, account: DevAccount) -> List[UsageAlert]:
        """Check if any alerts should be generated for an account"""
        
        alerts = []
        
        # Get all metrics for this account
        result = await self.db.execute(
            select(UsageMetric).where(UsageMetric.dev_account_id == account.id)
        )
        metrics = result.scalars().all()
        
        for metric in metrics:
            # Check for critical usage (>90%)
            if metric.is_critical and metric.usage_percentage >= 90:
                alert = await self._create_usage_alert(
                    account=account,
                    metric=metric,
                    alert_type=AlertTypeEnum.QUOTA_EXCEEDED,
                    title=f"Critical: {metric.metric_name} usage at {metric.usage_percentage:.1f}%",
                    message=f"Your {account.software.name} {metric.metric_name} usage is critically high at {metric.usage_percentage:.1f}% ({metric.current_usage:.1f} of {metric.limit_value} {metric.unit}). Consider upgrading or optimizing usage.",
                    severity="critical"
                )
                alerts.append(alert)
            
            # Check for warning usage (>75%)
            elif metric.is_warning and metric.usage_percentage >= 75:
                alert = await self._create_usage_alert(
                    account=account,
                    metric=metric,
                    alert_type=AlertTypeEnum.USAGE_WARNING,
                    title=f"Warning: {metric.metric_name} usage at {metric.usage_percentage:.1f}%",
                    message=f"Your {account.software.name} {metric.metric_name} usage is high at {metric.usage_percentage:.1f}% ({metric.current_usage:.1f} of {metric.limit_value} {metric.unit}).",
                    severity="warning"
                )
                alerts.append(alert)
        
        return alerts

    async def _create_usage_alert(self, account: DevAccount, metric: UsageMetric, alert_type: AlertTypeEnum, title: str, message: str, severity: str) -> UsageAlert:
        """Create a usage alert"""
        
        # Check if similar alert already exists and is unresolved
        existing_alert = await self.db.execute(
            select(UsageAlert).where(
                and_(
                    UsageAlert.dev_account_id == account.id,
                    UsageAlert.usage_metric_id == metric.id,
                    UsageAlert.alert_type == alert_type,
                    UsageAlert.is_resolved == False,
                    UsageAlert.triggered_at >= datetime.utcnow() - timedelta(hours=24)  # Within last 24 hours
                )
            )
        )
        
        if existing_alert.scalar_one_or_none():
            return None  # Don't create duplicate alert
        
        # Generate recommended actions
        recommended_actions = self._generate_usage_recommendations(metric, account.software.name)
        
        alert = UsageAlert(
            user_id=account.user_id,
            dev_account_id=account.id,
            usage_metric_id=metric.id,
            alert_type=alert_type,
            title=title,
            message=message,
            severity=severity,
            recommended_actions=recommended_actions,
            triggered_at=datetime.utcnow(),
            expires_at=datetime.utcnow() + timedelta(days=7)
        )
        
        self.db.add(alert)
        await self.db.commit()
        
        # Send notification
        await self.notification_service.send_usage_alert(account.user, alert)
        
        return alert

    def _generate_usage_recommendations(self, metric: UsageMetric, software_name: str) -> List[str]:
        """Generate recommendations based on usage patterns"""
        
        recommendations = []
        
        if metric.metric_name == "build_minutes":
            recommendations.extend([
                "Optimize your build process to reduce build times",
                "Consider caching dependencies",
                "Review if all builds are necessary",
                "Upgrade to a paid plan for more build minutes"
            ])
        
        elif metric.metric_name == "bandwidth_gb":
            recommendations.extend([
                "Optimize images and assets",
                "Enable compression",
                "Use a CDN for static assets",
                "Consider upgrading for higher bandwidth limits"
            ])
        
        elif metric.metric_name == "function_invocations":
            recommendations.extend([
                "Review function usage patterns",
                "Optimize function code for efficiency",
                "Consider batching requests",
                "Upgrade for higher invocation limits"
            ])
        
        elif metric.metric_name == "database_rows":
            recommendations.extend([
                "Review data retention policies",
                "Clean up unnecessary data",
                "Optimize database queries",
                "Consider archiving old data"
            ])
        
        return recommendations

    async def _get_api_credential(self, account: DevAccount, credential_type: str) -> Optional[str]:
        """Get decrypted API credential for an account"""
        
        # This would integrate with the credential decryption service
        # For now, return None - to be implemented with actual encryption service
        return None

    async def get_usage_summary(self, user_id: int) -> Dict[str, Any]:
        """Get usage summary for a user across all their accounts"""
        
        # Get all user's accounts
        result = await self.db.execute(
            select(DevAccount).where(DevAccount.user_id == user_id)
        )
        accounts = result.scalars().all()
        
        summary = {
            "total_accounts": len(accounts),
            "accounts_with_warnings": 0,
            "accounts_with_critical_usage": 0,
            "recent_alerts": 0,
            "accounts": []
        }
        
        for account in accounts:
            # Get metrics for this account
            metrics_result = await self.db.execute(
                select(UsageMetric).where(UsageMetric.dev_account_id == account.id)
            )
            metrics = metrics_result.scalars().all()
            
            account_summary = {
                "id": account.id,
                "software": account.software.name if account.software else "Unknown",
                "status": account.status.value,
                "metrics_count": len(metrics),
                "has_warnings": any(m.is_warning for m in metrics),
                "has_critical": any(m.is_critical for m in metrics),
                "metrics": [
                    {
                        "name": m.metric_name,
                        "usage": m.current_usage,
                        "limit": m.limit_value,
                        "percentage": m.usage_percentage,
                        "unit": m.unit,
                        "is_warning": m.is_warning,
                        "is_critical": m.is_critical
                    }
                    for m in metrics
                ]
            }
            
            if account_summary["has_warnings"]:
                summary["accounts_with_warnings"] += 1
            if account_summary["has_critical"]:
                summary["accounts_with_critical_usage"] += 1
            
            summary["accounts"].append(account_summary)
        
        # Get recent alerts count
        alerts_result = await self.db.execute(
            select(UsageAlert).where(
                and_(
                    UsageAlert.user_id == user_id,
                    UsageAlert.triggered_at >= datetime.utcnow() - timedelta(days=7),
                    UsageAlert.is_resolved == False
                )
            )
        )
        summary["recent_alerts"] = len(alerts_result.scalars().all())
        
        return summary
