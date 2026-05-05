import json
import os

class RuleEngine:
    def __init__(self, rules_path=None):
        if rules_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
            rules_path = os.path.join(base_dir, "AI_Module", "models", "routing_rules.json")
        
        if os.path.exists(rules_path):
            with open(rules_path, 'r', encoding='utf-8') as f:
                self.rules = json.load(f)
        else:
            self.rules = {}

    def get_routing(self, intent: str) -> dict:
        return self.rules.get(intent, {"urgency": "low", "department": "general"})

rule_engine = RuleEngine()