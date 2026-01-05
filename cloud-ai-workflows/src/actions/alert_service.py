from datetime import datetime
from typing import Dict, Any, List
import json

# Confidence threshold fyrir manual review
CONFIDENCE_THRESHOLD = 0.7


class AlertService:
    """
    í production væri þetta Slack, email
    """
    
    def __init__(self, alert_threshold: str = "high"):
        """
        alert_threshold: minimum severity til að senda alert
        """
        self.alert_threshold = alert_threshold
        self.severity_priority = {
            "critical": 4,
            "high": 3,
            "medium": 2,
            "low": 1
        }
        self.alerts_sent = []
        self.manual_review_flagged = []  # Track incidents sem þarfnast manual review
    
    def should_alert(self, severity: str) -> bool:
        """
        Ákveða hvort á að senda alert based on severity
        """
        threshold_level = self.severity_priority.get(self.alert_threshold, 2)
        incident_level = self.severity_priority.get(severity, 1)
        return incident_level >= threshold_level
    
    def send_alert(self, incident_id: str, decision: Dict[str, Any], title: str = "") -> bool:
        """
        Send alert ef severity er nógu high

        Returns True ef alert var sent
        """
        # Athuga fyrst hvort þetta þarfnast manual review
        if decision.get("needs_manual_review", False):
            review_item = {
                "timestamp": datetime.now().isoformat(),
                "incident_id": incident_id,
                "severity": decision["severity"],
                "category": decision["category"],
                "title": title,
                "action": decision["recommended_action"],
                "confidence": decision["confidence"],
                "reasoning": decision.get("reasoning", "")
            }
            self.manual_review_flagged.append(review_item)
            self._print_manual_review_flag(review_item)

        if not self.should_alert(decision.get("severity", "low")):
            return False

        alert = {
            "timestamp": datetime.now().isoformat(),
            "incident_id": incident_id,
            "severity": decision["severity"],
            "category": decision["category"],
            "title": title,
            "action": decision["recommended_action"],
            "confidence": decision["confidence"]
        }

        self.alerts_sent.append(alert)
        self._print_alert(alert)
        return True
    
    def _print_alert(self, alert: Dict[str, Any]):
        """
        Alert til console
        """
        print("\n" + "="*60)
        print(f"ALERT: {alert['severity'].upper()} SEVERITY")
        print("="*60)
        print(f"Time:     {alert['timestamp']}")
        print(f"ID:       {alert['incident_id']}")
        print(f"Category: {alert['category']}")
        if alert.get('title'):
            print(f"Title:    {alert['title'][:70]}")
        print(f"Action:   {alert['action']}")
        print(f"Confidence: {alert['confidence']:.2f}")
        print("="*60 + "\n")

    def _print_manual_review_flag(self, review_item: Dict[str, Any]):
        """Flag fyrir manual review"""
        print(f"[MANUAL REVIEW] {review_item['incident_id']} - confidence: {review_item['confidence']:.2f} < {CONFIDENCE_THRESHOLD}")
    
    def send_batch_summary(self, total_processed: int, decisions: List[Dict[str, Any]]):
        """
        Send summary eftir batch processing
        """
        severity_counts = {
            "critical": 0,
            "high": 0,
            "medium": 0,
            "low": 0
        }
        
        for decision in decisions:
            severity = decision.get("severity", "low")
            severity_counts[severity] += 1
        
        print("BATCH PROCESSING SUMMARY")
        print("="*60)
        print(f"Total Incidents Processed: {total_processed}")
        print(f"Alerts Sent: {len(self.alerts_sent)}")
        print(f"Manual Review Flagged: {len(self.manual_review_flagged)}")
        print("\nSeverity Breakdown:")
        print(f"  Critical: {severity_counts['critical']}")
        print(f"  High:     {severity_counts['high']}")
        print(f"  Medium:   {severity_counts['medium']}")
        print(f"  Low:      {severity_counts['low']}")
        print("="*60 + "\n")
    
    def get_alert_log(self) -> List[Dict[str, Any]]:
        """
        Skilar allar sendar alerts
        """
        return self.alerts_sent

    def get_manual_review_items(self) -> List[Dict[str, Any]]:
        """
        Skilar öllum incidents sem þarfnast manual review
        """
        return self.manual_review_flagged


# Test frá claude
if __name__ == "__main__":
    alert_service = AlertService(alert_threshold="high")
    
    # Test critical alert
    test_decision_critical = {
        "severity": "critical",
        "category": "security",
        "recommended_action": "escalate to security team immediately",
        "confidence": 0.95,
        "reasoning": "potential data breach detected"
    }
    
    alert_service.send_alert("INC-001", test_decision_critical, "Database access unauthorized")
    
    # Test low severity (should not alert)
    test_decision_low = {
        "severity": "low",
        "category": "ui_ux",
        "recommended_action": "add to backlog for future review",
        "confidence": 0.78,
        "reasoning": "minor cosmetic issue"
    }
    
    alert_service.send_alert("INC-002", test_decision_low, "Button alignment off by 2px")
    
    # Summary
    alert_service.send_batch_summary(2, [test_decision_critical, test_decision_low])