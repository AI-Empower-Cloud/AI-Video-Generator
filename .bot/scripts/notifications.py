#!/usr/bin/env python3
"""
🤖 AI Video Generator Bot Notifications
=======================================

Simple notification system for bot activities.
Supports Discord, Slack, and other webhook services.
"""

import json
import os
import requests
from datetime import datetime
from typing import Optional, Dict, Any


class BotNotifier:
    """Handles notifications for bot activities"""
    
    def __init__(self):
        self.discord_webhook = os.environ.get('DISCORD_WEBHOOK_URL')
        self.slack_webhook = os.environ.get('SLACK_WEBHOOK_URL')
        self.enabled = bool(self.discord_webhook or self.slack_webhook)
    
    def send_commit_notification(self, commit_info: Dict[str, Any]):
        """Send notification for new commits"""
        if not self.enabled:
            return
        
        message = {
            "title": "🤖 New Automated Commit",
            "description": f"**{commit_info.get('message', 'Automated update')}**",
            "fields": [
                {"name": "Branch", "value": commit_info.get('branch', 'main'), "inline": True},
                {"name": "Files Changed", "value": str(commit_info.get('files_changed', 0)), "inline": True},
                {"name": "Timestamp", "value": datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC'), "inline": True}
            ],
            "color": 0x00ff00  # Green
        }
        
        self._send_webhook(message)
    
    def send_deployment_notification(self, deployment_info: Dict[str, Any]):
        """Send notification for deployments"""
        if not self.enabled:
            return
        
        status = deployment_info.get('status', 'unknown')
        color = 0x00ff00 if status == 'success' else 0xff0000
        
        message = {
            "title": f"🚀 Deployment {status.title()}",
            "description": f"**Environment:** {deployment_info.get('environment', 'production')}",
            "fields": [
                {"name": "Status", "value": status.title(), "inline": True},
                {"name": "Version", "value": deployment_info.get('version', 'latest'), "inline": True},
                {"name": "Duration", "value": deployment_info.get('duration', 'N/A'), "inline": True}
            ],
            "color": color
        }
        
        self._send_webhook(message)
    
    def send_error_notification(self, error_info: Dict[str, Any]):
        """Send notification for errors"""
        if not self.enabled:
            return
        
        message = {
            "title": "❌ Bot Error Detected",
            "description": f"**Error:** {error_info.get('message', 'Unknown error')}",
            "fields": [
                {"name": "Component", "value": error_info.get('component', 'Unknown'), "inline": True},
                {"name": "Severity", "value": error_info.get('severity', 'Medium'), "inline": True},
                {"name": "Timestamp", "value": datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC'), "inline": True}
            ],
            "color": 0xff0000  # Red
        }
        
        self._send_webhook(message)
    
    def send_daily_report(self, report_data: Dict[str, Any]):
        """Send daily activity report"""
        if not self.enabled:
            return
        
        message = {
            "title": "📊 Daily Bot Report",
            "description": "**AI Video Generator Bot Daily Summary**",
            "fields": [
                {"name": "Commits", "value": str(report_data.get('commits', 0)), "inline": True},
                {"name": "Tests Run", "value": str(report_data.get('tests', 0)), "inline": True},
                {"name": "Deployments", "value": str(report_data.get('deployments', 0)), "inline": True},
                {"name": "Issues Fixed", "value": str(report_data.get('issues_fixed', 0)), "inline": True},
                {"name": "Code Quality", "value": report_data.get('quality_score', 'A+'), "inline": True},
                {"name": "Uptime", "value": report_data.get('uptime', '99.9%'), "inline": True}
            ],
            "color": 0x0099ff  # Blue
        }
        
        self._send_webhook(message)
    
    def _send_webhook(self, message: Dict[str, Any]):
        """Send webhook notification"""
        try:
            # Discord webhook
            if self.discord_webhook:
                discord_payload = {
                    "embeds": [{
                        "title": message["title"],
                        "description": message["description"],
                        "fields": message["fields"],
                        "color": message["color"],
                        "timestamp": datetime.now().isoformat(),
                        "footer": {
                            "text": "AI Video Generator Bot",
                            "icon_url": "https://cdn.discordapp.com/embed/avatars/0.png"
                        }
                    }]
                }
                
                response = requests.post(
                    self.discord_webhook,
                    json=discord_payload,
                    headers={'Content-Type': 'application/json'},
                    timeout=10
                )
                response.raise_for_status()
            
            # Slack webhook
            if self.slack_webhook:
                # Convert Discord format to Slack format
                fields_text = "\n".join([
                    f"*{field['name']}:* {field['value']}"
                    for field in message["fields"]
                ])
                
                slack_payload = {
                    "text": message["title"],
                    "attachments": [{
                        "color": "good" if message["color"] == 0x00ff00 else "danger" if message["color"] == 0xff0000 else "warning",
                        "fields": [
                            {
                                "title": message["description"],
                                "value": fields_text,
                                "short": False
                            }
                        ],
                        "footer": "AI Video Generator Bot",
                        "ts": int(datetime.now().timestamp())
                    }]
                }
                
                response = requests.post(
                    self.slack_webhook,
                    json=slack_payload,
                    headers={'Content-Type': 'application/json'},
                    timeout=10
                )
                response.raise_for_status()
                
        except Exception as e:
            print(f"Failed to send webhook notification: {e}")


def main():
    """Example usage"""
    notifier = BotNotifier()
    
    # Example commit notification
    notifier.send_commit_notification({
        "message": "🏗️ Core: Add modular backend architecture",
        "branch": "main",
        "files_changed": 15
    })
    
    # Example deployment notification
    notifier.send_deployment_notification({
        "status": "success",
        "environment": "production",
        "version": "v1.0.0",
        "duration": "2m 30s"
    })
    
    # Example daily report
    notifier.send_daily_report({
        "commits": 8,
        "tests": 25,
        "deployments": 3,
        "issues_fixed": 2,
        "quality_score": "A+",
        "uptime": "99.9%"
    })


if __name__ == "__main__":
    main()
