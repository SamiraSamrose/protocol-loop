"""
Markov chain utilities for state prediction
"""

import random
from typing import Dict, List, Any, Optional


class MarkovChainUtil:
    """Utility class for Markov chain operations"""
    
    @staticmethod
    def build_transition_matrix(
        state_sequences: List[List[str]]
    ) -> Dict[str, Dict[str, float]]:
        """Build transition probability matrix from sequences"""
        
        transitions = {}
        
        for sequence in state_sequences:
            for i in range(len(sequence) - 1):
                current = sequence[i]
                next_state = sequence[i + 1]
                
                if current not in transitions:
                    transitions[current] = {}
                
                if next_state not in transitions[current]:
                    transitions[current][next_state] = 0
                
                transitions[current][next_state] += 1
        
        # Convert counts to probabilities
        for current_state in transitions:
            total = sum(transitions[current_state].values())
            for next_state in transitions[current_state]:
                transitions[current_state][next_state] /= total
        
        return transitions
    
    @staticmethod
    def predict_sequence(
        transition_matrix: Dict[str, Dict[str, float]],
        start_state: str,
        length: int,
        temperature: float = 1.0
    ) -> List[str]:
        """Predict a sequence of states"""
        
        if start_state not in transition_matrix:
            return [start_state]
        
        sequence = [start_state]
        current = start_state
        
        for _ in range(length - 1):
            if current not in transition_matrix or not transition_matrix[current]:
                break
            
            next_state = MarkovChainUtil._sample_next_state(
                transition_matrix[current],
                temperature
            )
            
            sequence.append(next_state)
            current = next_state
        
        return sequence
    
    @staticmethod
    def _sample_next_state(
        probabilities: Dict[str, float],
        temperature: float
    ) -> str:
        """Sample next state with temperature"""
        
        import numpy as np
        
        states = list(probabilities.keys())
        probs = np.array(list(probabilities.values()))
        
        # Apply temperature
        probs = np.power(probs, 1.0 / temperature)
        probs = probs / probs.sum()
        
        return np.random.choice(states, p=probs)
    
    @staticmethod
    def calculate_stationary_distribution(
        transition_matrix: Dict[str, Dict[str, float]],
        iterations: int = 1000
    ) -> Dict[str, float]:
        """Calculate stationary distribution of Markov chain"""
        
        states = list(transition_matrix.keys())
        distribution = {state: 1.0 / len(states) for state in states}
        
        for _ in range(iterations):
            new_distribution = {state: 0.0 for state in states}
            
            for current_state in states:
                for next_state, prob in transition_matrix.get(current_state, {}).items():
                    new_distribution[next_state] += distribution[current_state] * prob
            
            distribution = new_distribution
        
        return distribution
    
    @staticmethod
    def analyze_behavior_patterns(
        decision_history: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Analyze behavioral patterns using Markov chains"""
        
        # Extract state sequence
        state_sequence = []
        
        for decision in decision_history:
            mentor = decision.get("mentor_influence", "none")
            confidence = decision.get("confidence", 0.5)
            
            # Create state representation
            if confidence > 0.7:
                state = f"{mentor}_confident"
            elif confidence < 0.4:
                state = f"{mentor}_uncertain"
            else:
                state = f"{mentor}_moderate"
            
            state_sequence.append(state)
        
        # Build transition matrix
        transitions = MarkovChainUtil.build_transition_matrix([state_sequence])
        
        # Calculate metrics
        most_common_state = max(
            set(state_sequence),
            key=state_sequence.count
        ) if state_sequence else "unknown"
        
        transition_diversity = len(transitions) / max(len(set(state_sequence)), 1)
        
        return {
            "transition_matrix": transitions,
            "most_common_state": most_common_state,
            "state_diversity": len(set(state_sequence)),
            "transition_diversity": transition_diversity,
            "sequence_length": len(state_sequence)
        }
    
    @staticmethod
    def predict_next_mentor_choice(
        recent_choices: List[str],
        transition_matrix: Dict[str, Dict[str, float]]
    ) -> Dict[str, float]:
        """Predict next mentor choice probabilities"""
        
        if not recent_choices or not transition_matrix:
            return {"LOGIC": 0.25, "COMPASSION": 0.25, "CURIOSITY": 0.25, "FEAR": 0.25}
        
        current_state = recent_choices[-1]
        
        if current_state not in transition_matrix:
            return {"LOGIC": 0.25, "COMPASSION": 0.25, "CURIOSITY": 0.25, "FEAR": 0.25}
        
        predictions = {}
        
        for next_state, prob in transition_matrix[current_state].items():
            # Extract mentor from state
            mentor = next_state.split('_')[0]
            predictions[mentor] = predictions.get(mentor, 0) + prob
        
        return predictions