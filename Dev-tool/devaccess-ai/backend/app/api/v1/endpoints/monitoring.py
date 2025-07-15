"""
Usage monitoring endpoints for tracking free tier usage and alerts
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.api.v1.endpoints.auth import get_current_user
from app.models.user import User
from app.services.usage_monitoring_service import UsageMonitoringService
import structlog

logger = structlog.get_logger()

router = APIRouter()


@router.get("/usage/summary")
async def get_usage_summary(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get usage summary for all user's accounts"""
    
    try:
        monitoring_service = UsageMonitoringService(db)
        summary = await monitoring_service.get_usage_summary(current_user.id)
        
        return summary
        
    except Exception as e:
        logger.error("Failed to get usage summary", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to get usage summary")


@router.post("/usage/check")
async def trigger_usage_check(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Manually trigger usage monitoring for user's accounts"""
    
    try:
        monitoring_service = UsageMonitoringService(db)
        
        # Get user's accounts and monitor them
        from sqlalchemy import select
        from app.models.account import DevAccount
        
        result = await db.execute(
            select(DevAccount).where(DevAccount.user_id == current_user.id)
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
                result = await monitoring_service.monitor_account_usage(account)
                monitoring_results["results"].append(result)
                monitoring_results["monitored"] += 1
                monitoring_results["alerts_generated"] += result.get("alerts_generated", 0)
            except Exception as e:
                monitoring_results["errors"] += 1
                logger.error(f"Error monitoring account {account.id}: {e}")
        
        return monitoring_results
        
    except Exception as e:
        logger.error("Failed to trigger usage check", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to trigger usage check")


@router.get("/alerts")
async def get_user_alerts(
    unread_only: bool = False,
    limit: int = 50,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get alerts for the user"""
    
    try:
        from sqlalchemy import select, and_, desc
        from app.models.enhanced_models import UsageAlert
        
        query = select(UsageAlert).where(UsageAlert.user_id == current_user.id)
        
        if unread_only:
            query = query.where(UsageAlert.is_read == False)
        
        query = query.order_by(desc(UsageAlert.triggered_at)).limit(limit)
        
        result = await db.execute(query)
        alerts = result.scalars().all()
        
        formatted_alerts = []
        for alert in alerts:
            formatted_alerts.append({
                "id": alert.id,
                "alert_type": alert.alert_type.value,
                "title": alert.title,
                "message": alert.message,
                "severity": alert.severity,
                "is_read": alert.is_read,
                "is_resolved": alert.is_resolved,
                "recommended_actions": alert.recommended_actions,
                "triggered_at": alert.triggered_at,
                "expires_at": alert.expires_at,
                "dev_account_id": alert.dev_account_id
            })
        
        return {
            "alerts": formatted_alerts,
            "total": len(formatted_alerts),
            "unread_count": len([a for a in alerts if not a.is_read])
        }
        
    except Exception as e:
        logger.error("Failed to get user alerts", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to get alerts")


@router.put("/alerts/{alert_id}/read")
async def mark_alert_as_read(
    alert_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Mark an alert as read"""
    
    try:
        from sqlalchemy import select
        from app.models.enhanced_models import UsageAlert
        
        result = await db.execute(
            select(UsageAlert).where(
                and_(
                    UsageAlert.id == alert_id,
                    UsageAlert.user_id == current_user.id
                )
            )
        )
        alert = result.scalar_one_or_none()
        
        if not alert:
            raise HTTPException(status_code=404, detail="Alert not found")
        
        alert.is_read = True
        await db.commit()
        
        return {"message": "Alert marked as read"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to mark alert as read", error=str(e), alert_id=alert_id)
        raise HTTPException(status_code=500, detail="Failed to mark alert as read")


@router.put("/alerts/{alert_id}/resolve")
async def resolve_alert(
    alert_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Resolve an alert"""
    
    try:
        from sqlalchemy import select
        from app.models.enhanced_models import UsageAlert
        from datetime import datetime
        
        result = await db.execute(
            select(UsageAlert).where(
                and_(
                    UsageAlert.id == alert_id,
                    UsageAlert.user_id == current_user.id
                )
            )
        )
        alert = result.scalar_one_or_none()
        
        if not alert:
            raise HTTPException(status_code=404, detail="Alert not found")
        
        alert.is_resolved = True
        alert.resolved_at = datetime.utcnow()
        await db.commit()
        
        return {"message": "Alert resolved"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to resolve alert", error=str(e), alert_id=alert_id)
        raise HTTPException(status_code=500, detail="Failed to resolve alert")


@router.get("/metrics/account/{account_id}")
async def get_account_metrics(
    account_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get usage metrics for a specific account"""
    
    try:
        from sqlalchemy import select, and_
        from app.models.account import DevAccount
        from app.models.enhanced_models import UsageMetric
        
        # Verify account belongs to user
        account_result = await db.execute(
            select(DevAccount).where(
                and_(
                    DevAccount.id == account_id,
                    DevAccount.user_id == current_user.id
                )
            )
        )
        account = account_result.scalar_one_or_none()
        
        if not account:
            raise HTTPException(status_code=404, detail="Account not found")
        
        # Get metrics for this account
        metrics_result = await db.execute(
            select(UsageMetric).where(UsageMetric.dev_account_id == account_id)
        )
        metrics = metrics_result.scalars().all()
        
        formatted_metrics = []
        for metric in metrics:
            formatted_metrics.append({
                "id": metric.id,
                "metric_name": metric.metric_name,
                "current_usage": metric.current_usage,
                "limit_value": metric.limit_value,
                "unit": metric.unit,
                "usage_percentage": metric.usage_percentage,
                "is_warning": metric.is_warning,
                "is_critical": metric.is_critical,
                "data_source": metric.data_source,
                "last_updated": metric.last_updated,
                "last_checked": metric.last_checked
            })
        
        return {
            "account_id": account_id,
            "software_name": account.software.name if account.software else "Unknown",
            "metrics": formatted_metrics,
            "total_metrics": len(formatted_metrics)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to get account metrics", error=str(e), account_id=account_id)
        raise HTTPException(status_code=500, detail="Failed to get account metrics")
