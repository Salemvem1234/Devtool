#!/usr/bin/env python3
"""
DevAccess AI CLI Tool
A comprehensive command-line interface for managing free-tier development tools
"""

import click
import json
import asyncio
import aiohttp
import os
import sys
from typing import List, Dict, Optional
from datetime import datetime
from pathlib import Path
import configparser
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from rich.syntax import Syntax
from rich.prompt import Prompt, Confirm
import yaml

console = Console()

# Configuration management
class Config:
    def __init__(self):
        self.config_dir = Path.home() / ".devaccess"
        self.config_file = self.config_dir / "config.ini"
        self.credentials_file = self.config_dir / "credentials.json"
        self.config_dir.mkdir(exist_ok=True)
        self.config = configparser.ConfigParser()
        self.load_config()
    
    def load_config(self):
        if self.config_file.exists():
            self.config.read(self.config_file)
        else:
            self.config['DEFAULT'] = {
                'api_url': 'http://localhost:8000',
                'timeout': '30',
                'max_retries': '3',
                'output_format': 'table'
            }
            self.save_config()
    
    def save_config(self):
        with open(self.config_file, 'w') as f:
            self.config.write(f)
    
    def get(self, key: str, default: str = None) -> str:
        return self.config.get('DEFAULT', key, fallback=default)
    
    def set(self, key: str, value: str):
        self.config.set('DEFAULT', key, value)
        self.save_config()

config = Config()

# API Client
class DevAccessAPI:
    def __init__(self, base_url: str = None):
        self.base_url = base_url or config.get('api_url')
        self.timeout = int(config.get('timeout', '30'))
        self.session = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=self.timeout)
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def get(self, endpoint: str, params: dict = None) -> dict:
        async with self.session.get(f"{self.base_url}{endpoint}", params=params) as response:
            return await response.json()
    
    async def post(self, endpoint: str, data: dict = None) -> dict:
        async with self.session.post(f"{self.base_url}{endpoint}", json=data) as response:
            return await response.json()
    
    async def put(self, endpoint: str, data: dict = None) -> dict:
        async with self.session.put(f"{self.base_url}{endpoint}", json=data) as response:
            return await response.json()
    
    async def delete(self, endpoint: str) -> dict:
        async with self.session.delete(f"{self.base_url}{endpoint}") as response:
            return await response.json()

# Helper functions
def format_table(data: List[Dict], title: str = None) -> Table:
    """Format data as a rich table"""
    if not data:
        return Table(title=title or "No data")
    
    table = Table(title=title, show_header=True, header_style="bold magenta")
    
    # Add columns based on first row
    for key in data[0].keys():
        table.add_column(key.replace('_', ' ').title(), style="cyan")
    
    # Add rows
    for row in data:
        table.add_row(*[str(v) for v in row.values()])
    
    return table

def save_output(data: dict, filename: str, format: str = 'json'):
    """Save output to file in specified format"""
    output_dir = Path.home() / ".devaccess" / "outputs"
    output_dir.mkdir(exist_ok=True)
    
    if format == 'json':
        with open(output_dir / f"{filename}.json", 'w') as f:
            json.dump(data, f, indent=2)
    elif format == 'yaml':
        with open(output_dir / f"{filename}.yaml", 'w') as f:
            yaml.dump(data, f, default_flow_style=False)
    elif format == 'csv':
        import pandas as pd
        df = pd.DataFrame(data)
        df.to_csv(output_dir / f"{filename}.csv", index=False)

# CLI Commands
@click.group()
@click.option('--config-file', help='Path to configuration file')
@click.option('--api-url', help='API base URL')
@click.option('--debug', is_flag=True, help='Enable debug mode')
def cli(config_file, api_url, debug):
    """DevAccess AI CLI - Manage free-tier development tools"""
    if api_url:
        config.set('api_url', api_url)
    
    if debug:
        console.print("[yellow]Debug mode enabled[/yellow]")

@cli.group()
def account():
    """Account management commands"""
    pass

@account.command()
@click.option('--software', '-s', multiple=True, help='Software to create accounts for')
@click.option('--count', '-c', type=int, default=1, help='Number of accounts per software')
@click.option('--email-domain', help='Email domain preference')
@click.option('--usage-context', help='Usage context description')
@click.option('--output', '-o', help='Output file name')
@click.option('--format', 'output_format', type=click.Choice(['json', 'yaml', 'table']), default='table')
def create(software, count, email_domain, usage_context, output, output_format):
    """Create new accounts for specified software"""
    
    async def _create_accounts():
        if not software:
            # Interactive software selection
            async with DevAccessAPI() as api:
                software_list = await api.get('/api/frontend/software-list')
                
                console.print("\n[bold]Available Software:[/bold]")
                for i, sw in enumerate(software_list['software'], 1):
                    console.print(f"{i}. {sw['name']} - {sw['description']}")
                
                selected_indices = Prompt.ask(
                    "\nSelect software (comma-separated numbers)",
                    default="1"
                ).split(',')
                
                software_names = [
                    software_list['software'][int(i.strip()) - 1]['id'] 
                    for i in selected_indices
                ]
        else:
            software_names = list(software)
        
        request_data = {
            'software': software_names,
            'accountCounts': {sw: count for sw in software_names},
            'emailDomain': email_domain or '',
            'usageContext': usage_context or ''
        }
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Creating accounts...", total=None)
            
            async with DevAccessAPI() as api:
                result = await api.post('/api/frontend/create-accounts', request_data)
                
                progress.update(task, completed=True)
                
                if result.get('success'):
                    console.print(f"\n[green]✅ {result['message']}[/green]")
                    
                    if output_format == 'table':
                        table = format_table(result['accounts'], "Created Accounts")
                        console.print(table)
                    else:
                        console.print(json.dumps(result, indent=2))
                    
                    if output:
                        save_output(result, output, output_format)
                        console.print(f"\n[blue]Output saved to ~/.devaccess/outputs/{output}.{output_format}[/blue]")
                else:
                    console.print(f"[red]❌ Failed to create accounts[/red]")
    
    asyncio.run(_create_accounts())

@account.command()
@click.option('--account-id', type=int, help='Account ID to check')
@click.option('--software', help='Filter by software name')
@click.option('--format', 'output_format', type=click.Choice(['json', 'yaml', 'table']), default='table')
def list(account_id, software, output_format):
    """List all accounts or get specific account details"""
    
    async def _list_accounts():
        async with DevAccessAPI() as api:
            if account_id:
                result = await api.get(f'/api/frontend/account-data?account_id={account_id}')
                
                if output_format == 'table':
                    # Display account details in panels
                    console.print(Panel(
                        f"Software: {result['software_info']['name']}\n"
                        f"Email: {result['credentials']['email']}\n"
                        f"Status: {'Active' if result['status']['active'] else 'Inactive'}\n"
                        f"Context: {result['status']['usage_context']}",
                        title="Account Details"
                    ))
                    
                    # Display usage metrics
                    metrics_table = format_table(result['usage_metrics'], "Usage Metrics")
                    console.print(metrics_table)
                else:
                    console.print(json.dumps(result, indent=2))
            else:
                # List all accounts (mock implementation)
                accounts = [
                    {"id": 1, "software": "cursor", "email": "user@temp.com", "status": "active"},
                    {"id": 2, "software": "vercel", "email": "dev@temp.com", "status": "active"},
                ]
                
                if software:
                    accounts = [acc for acc in accounts if acc['software'] == software]
                
                if output_format == 'table':
                    table = format_table(accounts, "Accounts")
                    console.print(table)
                else:
                    console.print(json.dumps(accounts, indent=2))
    
    asyncio.run(_list_accounts())

@cli.group()
def monitor():
    """Usage monitoring commands"""
    pass

@monitor.command()
@click.option('--account-id', type=int, help='Account ID to monitor')
@click.option('--refresh', is_flag=True, help='Refresh usage data')
@click.option('--format', 'output_format', type=click.Choice(['json', 'yaml', 'table']), default='table')
def usage(account_id, refresh, output_format):
    """Monitor usage across accounts"""
    
    async def _monitor_usage():
        async with DevAccessAPI() as api:
            if refresh:
                await api.post('/api/frontend/refresh-usage')
                console.print("[green]✅ Usage data refreshed[/green]")
            
            result = await api.get(f'/api/frontend/account-data?account_id={account_id or 1}')
            
            if output_format == 'table':
                # Create usage table with status colors
                table = Table(title="Usage Metrics", show_header=True, header_style="bold magenta")
                table.add_column("Metric", style="cyan")
                table.add_column("Current", style="white")
                table.add_column("Limit", style="white")
                table.add_column("Usage %", style="white")
                table.add_column("Status", style="white")
                table.add_column("Reset Date", style="white")
                
                for metric in result['usage_metrics']:
                    usage_pct = (metric['current'] / metric['limit']) * 100
                    status_color = "green" if metric['status'] == 'normal' else "yellow" if metric['status'] == 'warning' else "red"
                    
                    table.add_row(
                        metric['name'],
                        f"{metric['current']} {metric['unit']}",
                        f"{metric['limit']} {metric['unit']}",
                        f"{usage_pct:.1f}%",
                        f"[{status_color}]{metric['status']}[/{status_color}]",
                        metric['reset_date']
                    )
                
                console.print(table)
            else:
                console.print(json.dumps(result['usage_metrics'], indent=2))
    
    asyncio.run(_monitor_usage())

@cli.group()
def software():
    """Software management commands"""
    pass

@software.command()
@click.option('--category', help='Filter by category')
@click.option('--format', 'output_format', type=click.Choice(['json', 'yaml', 'table']), default='table')
def list(category, output_format):
    """List available software"""
    
    async def _list_software():
        async with DevAccessAPI() as api:
            result = await api.get('/api/frontend/software-list')
            
            software_list = result['software']
            if category:
                software_list = [sw for sw in software_list if sw['category'].lower() == category.lower()]
            
            if output_format == 'table':
                table = Table(title="Available Software", show_header=True, header_style="bold magenta")
                table.add_column("Name", style="cyan")
                table.add_column("Category", style="green")
                table.add_column("Description", style="white")
                table.add_column("Free Tier", style="yellow")
                
                for sw in software_list:
                    free_tier_info = ", ".join([f"{k}: {v}" for k, v in sw['free_tier'].items() if k != 'features'])
                    table.add_row(
                        sw['name'],
                        sw['category'],
                        sw['description'],
                        free_tier_info
                    )
                
                console.print(table)
            else:
                console.print(json.dumps(software_list, indent=2))
    
    asyncio.run(_list_software())

@cli.group()
def config():
    """Configuration commands"""
    pass

@config.command()
@click.option('--key', help='Configuration key')
@click.option('--value', help='Configuration value')
def set(key, value):
    """Set configuration value"""
    if key and value:
        config.set(key, value)
        console.print(f"[green]✅ Set {key} = {value}[/green]")
    else:
        console.print("[red]❌ Both key and value are required[/red]")

@config.command()
@click.option('--key', help='Configuration key to get')
def get(key):
    """Get configuration value"""
    if key:
        value = config.get(key)
        if value:
            console.print(f"{key} = {value}")
        else:
            console.print(f"[red]❌ Key '{key}' not found[/red]")
    else:
        # Show all configuration
        table = Table(title="Configuration", show_header=True, header_style="bold magenta")
        table.add_column("Key", style="cyan")
        table.add_column("Value", style="white")
        
        for key in config.config['DEFAULT']:
            table.add_row(key, config.get(key))
        
        console.print(table)

@cli.command()
def health():
    """Check API health status"""
    
    async def _check_health():
        try:
            async with DevAccessAPI() as api:
                result = await api.get('/api/health')
                
                if result.get('status') == 'healthy':
                    console.print(f"[green]✅ API is healthy[/green]")
                    console.print(f"Service: {result.get('service')}")
                    console.print(f"Version: {result.get('version')}")
                else:
                    console.print(f"[red]❌ API is unhealthy[/red]")
        except Exception as e:
            console.print(f"[red]❌ Failed to connect to API: {e}[/red]")
    
    asyncio.run(_check_health())

@cli.command()
def init():
    """Initialize DevAccess AI CLI"""
    console.print("[bold]Initializing DevAccess AI CLI...[/bold]")
    
    api_url = Prompt.ask("API URL", default="http://localhost:8000")
    config.set('api_url', api_url)
    
    console.print(f"\n[green]✅ Configuration saved to {config.config_file}[/green]")
    console.print(f"[blue]Run 'devaccess health' to test the connection[/blue]")

if __name__ == '__main__':
    cli()
