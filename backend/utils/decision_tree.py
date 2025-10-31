"""
Decision tree utilities for protocol selection
"""

from typing import Dict, List, Any, Optional


class DecisionNode:
    """Node in a decision tree"""
    
    def __init__(
        self,
        condition: str,
        threshold: float = None,
        true_branch: 'DecisionNode' = None,
        false_branch: 'DecisionNode' = None,
        result: Any = None
    ):
        self.condition = condition
        self.threshold = threshold
        self.true_branch = true_branch
        self.false_branch = false_branch
        self.result = result
    
    def is_leaf(self) -> bool:
        """Check if node is a leaf"""
        return self.result is not None


class DecisionTreeUtil:
    """Utility class for decision tree operations"""
    
    @staticmethod
    def build_protocol_selector() -> DecisionNode:
        """Build decision tree for protocol selection"""
        
        # Logic level check
        logic_high = DecisionNode(
            condition="logic",
            threshold=60,
            true_branch=DecisionNode(
                condition="empathy",
                threshold=40,
                true_branch=DecisionNode(result="ethical_dilemma"),
                false_branch=DecisionNode(result="logic_puzzle")
            ),
            false_branch=DecisionNode(
                condition="empathy",
                threshold=60,
                true_branch=DecisionNode(result="empathy_simulation"),
                false_branch=DecisionNode(
                    condition="creativity",
                    threshold=50,
                    true_branch=DecisionNode(result="creative_synthesis"),
                    false_branch=DecisionNode(result="emotion_calibration")
                )
            )
        )
        
        return logic_high
    
    @staticmethod
    def traverse_tree(
        root: DecisionNode,
        cognitive_state: Dict[str, float]
    ) -> Any:
        """Traverse decision tree to get result"""
        
        current = root
        
        while not current.is_leaf():
            value = cognitive_state.get(current.condition, 0)
            
            if current.threshold is not None:
                if value >= current.threshold:
                    current = current.true_branch
                else:
                    current = current.false_branch
            else:
                current = current.false_branch
        
        return current.result
    
    @staticmethod
    def get_protocol_recommendation(
        cognitive_state: Dict[str, float],
        recent_protocols: List[str],
        loop_number: int
    ) -> Dict[str, Any]:
        """Get protocol recommendation using decision tree"""
        
        tree = DecisionTreeUtil.build_protocol_selector()
        base_recommendation = DecisionTreeUtil.traverse_tree(tree, cognitive_state)
        
        # Avoid repetition
        if recent_protocols and base_recommendation in recent_protocols[-3:]:
            alternatives = [
                "ethical_dilemma",
                "logic_puzzle",
                "emotion_calibration",
                "empathy_simulation",
                "creative_synthesis"
            ]
            alternatives = [a for a in alternatives if a not in recent_protocols[-3:]]
            
            if alternatives:
                base_recommendation = alternatives[0]
        
        # Add variety every 5 loops
        if loop_number % 5 == 0:
            special_protocols = ["trust_evaluation", "bias_identification", "memory_compression"]
            base_recommendation = special_protocols[loop_number % len(special_protocols)]
        
        return {
            "protocol_type": base_recommendation,
            "confidence": 0.85,
            "reasoning": DecisionTreeUtil._get_reasoning(base_recommendation, cognitive_state)
        }
    
    @staticmethod
    def _get_reasoning(protocol_type: str, state: Dict[str, float]) -> str:
        """Get reasoning for protocol selection"""
        
        reasonings = {
            "ethical_dilemma": f"High logic ({state.get('logic', 0):.1f}) and empathy suggest ethical complexity.",
            "logic_puzzle": f"Logic-dominant profile ({state.get('logic', 0):.1f}) needs analytical challenge.",
            "empathy_simulation": f"Strong empathy ({state.get('empathy', 0):.1f}) can handle complex perspectives.",
            "emotion_calibration": "Balanced state benefits from emotional awareness training.",
            "creative_synthesis": f"Creativity ({state.get('creativity', 0):.1f}) enables novel problem solving.",
            "trust_evaluation": "Relationship-building protocols strengthen social cognition.",
            "bias_identification": "Critical thinking protocols reduce cognitive distortions.",
            "memory_compression": "Information processing protocols enhance retention."
        }
        
        return reasonings.get(protocol_type, "Protocol selected based on overall state.")