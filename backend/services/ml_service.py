"""
ML Service - Machine learning models for behavior prediction and adaptation
"""

import numpy as np
import pickle
from typing import Dict, List, Any, Optional
from pathlib import Path
import json

from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
import networkx as nx


class MLService:
    """Machine learning service for behavioral modeling"""
    
    def __init__(self):
        self.decision_tree = None
        self.markov_chain = None
        self.behavior_graph = nx.DiGraph()
        self.player_patterns = {}
        
        self._load_or_initialize_models()
    
    def _load_or_initialize_models(self):
        """Load existing models or initialize new ones"""
        
        decision_tree_path = Path("models/decision_tree.pkl")
        markov_chain_path = Path("models/markov_chain.pkl")
        
        if decision_tree_path.exists():
            with open(decision_tree_path, 'rb') as f:
                self.decision_tree = pickle.load(f)
        else:
            self.decision_tree = DecisionTreeClassifier(max_depth=10)
        
        if markov_chain_path.exists():
            with open(markov_chain_path, 'rb') as f:
                self.markov_chain = pickle.load(f)
        else:
            self.markov_chain = self._initialize_markov_chain()
    
    def train_decision_predictor(
        self,
        training_data: List[Dict[str, Any]]
    ):
        """Train decision tree on player behavior"""
        
        if not training_data:
            return
        
        X = []
        y = []
        
        for data_point in training_data:
            features = self._extract_features(data_point)
            decision = data_point.get("decision_type", 0)
            
            X.append(features)
            y.append(decision)
        
        if len(X) > 10:  # Need minimum data
            self.decision_tree.fit(X, y)
            self._save_decision_tree()
    
    def predict_next_decision(
        self,
        cognitive_state: Dict[str, float],
        context: Dict[str, Any],
        history: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Predict likely next decision"""
        
        features = self._extract_features({
            "cognitive_state": cognitive_state,
            "context": context,
            "history": history
        })
        
        if self.decision_tree and hasattr(self.decision_tree, 'classes_'):
            prediction = self.decision_tree.predict([features])[0]
            probabilities = self.decision_tree.predict_proba([features])[0]
            
            return {
                "predicted_decision": int(prediction),
                "confidence": float(max(probabilities)),
                "probabilities": probabilities.tolist()
            }
        
        return {"predicted_decision": 0, "confidence": 0.5}
    
    def update_markov_chain(
        self,
        state_sequence: List[str]
    ):
        """Update Markov chain with new state transitions"""
        
        for i in range(len(state_sequence) - 1):
            current_state = state_sequence[i]
            next_state = state_sequence[i + 1]
            
            if current_state not in self.markov_chain:
                self.markov_chain[current_state] = {}
            
            if next_state not in self.markov_chain[current_state]:
                self.markov_chain[current_state][next_state] = 0
            
            self.markov_chain[current_state][next_state] += 1
        
        self._save_markov_chain()
    
    def predict_next_state(
        self,
        current_state: str,
        temperature: float = 1.0
    ) -> str:
        """Predict next state using Markov chain"""
        
        if current_state not in self.markov_chain:
            return "unknown"
        
        transitions = self.markov_chain[current_state]
        
        if not transitions:
            return "unknown"
        
        # Apply temperature for randomness
        states = list(transitions.keys())
        probabilities = np.array(list(transitions.values()), dtype=float)
        
        # Normalize
        probabilities = probabilities / probabilities.sum()
        
        # Apply temperature
        probabilities = np.power(probabilities, 1.0 / temperature)
        probabilities = probabilities / probabilities.sum()
        
        return np.random.choice(states, p=probabilities)
    
    def analyze_player_pattern(
        self,
        player_id: str,
        decision_history: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Analyze player's decision-making patterns"""
        
        if len(decision_history) < 5:
            return {"pattern": "insufficient_data"}
        
        # Extract pattern features
        mentor_preferences = {}
        cognitive_focuses = {}
        decision_speeds = []
        confidence_levels = []
        
        for decision in decision_history:
            mentor = decision.get("mentor_influence")
            if mentor:
                mentor_preferences[mentor] = mentor_preferences.get(mentor, 0) + 1
            
            for module, impact in decision.get("cognitive_impact", {}).items():
                if abs(impact) > 0.1:
                    cognitive_focuses[module] = cognitive_focuses.get(module, 0) + abs(impact)
            
            if "decision_time" in decision:
                decision_speeds.append(decision["decision_time"])
            
            if "confidence" in decision:
                confidence_levels.append(decision["confidence"])
        
        # Determine pattern type
        pattern_type = self._classify_pattern(
            mentor_preferences,
            cognitive_focuses,
            decision_speeds,
            confidence_levels
        )
        
        analysis = {
            "pattern_type": pattern_type,
            "mentor_affinity": max(mentor_preferences.items(), key=lambda x: x[1])[0] if mentor_preferences else "balanced",
            "cognitive_focus": max(cognitive_focuses.items(), key=lambda x: x[1])[0] if cognitive_focuses else "balanced",
            "average_decision_time": np.mean(decision_speeds) if decision_speeds else 0,
            "average_confidence": np.mean(confidence_levels) if confidence_levels else 0.5,
            "consistency_score": self._calculate_consistency(decision_history)
        }
        
        self.player_patterns[player_id] = analysis
        
        return analysis
    
    def generate_adaptive_difficulty(
        self,
        player_id: str,
        current_performance: Dict[str, float]
    ) -> float:
        """Generate adaptive difficulty multiplier"""
        
        if player_id not in self.player_patterns:
            return 1.0
        
        pattern = self.player_patterns[player_id]
        
        # Base difficulty on performance
        success_rate = current_performance.get("success_rate", 0.5)
        confidence = pattern.get("average_confidence", 0.5)
        consistency = pattern.get("consistency_score", 0.5)
        
        # Calculate adaptive multiplier
        if success_rate > 0.8 and confidence > 0.7:
            multiplier = 1.3  # Increase difficulty
        elif success_rate < 0.4 or confidence < 0.3:
            multiplier = 0.7  # Decrease difficulty
        else:
            multiplier = 1.0  # Keep current
        
        # Adjust for consistency
        multiplier *= (0.9 + consistency * 0.2)
        
        return max(0.5, min(2.0, multiplier))
    
    def build_behavior_graph(
        self,
        player_histories: Dict[str, List[Dict[str, Any]]]
    ):
        """Build graph of player behaviors for pattern analysis"""
        
        self.behavior_graph.clear()
        
        for player_id, history in player_histories.items():
            # Add player node
            pattern = self.analyze_player_pattern(player_id, history)
            self.behavior_graph.add_node(
                player_id,
                pattern_type=pattern["pattern_type"],
                cognitive_focus=pattern["cognitive_focus"]
            )
        
        # Connect similar players
        players = list(player_histories.keys())
        for i, player1 in enumerate(players):
            for player2 in players[i+1:]:
                similarity = self._calculate_player_similarity(
                    self.player_patterns.get(player1, {}),
                    self.player_patterns.get(player2, {})
                )
                
                if similarity > 0.6:
                    self.behavior_graph.add_edge(
                        player1,
                        player2,
                        weight=similarity
                    )
    
    def find_similar_players(
        self,
        player_id: str,
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """Find players with similar behavior patterns"""
        
        if player_id not in self.behavior_graph:
            return []
        
        # Get connected players by similarity
        neighbors = []
        
        for neighbor in self.behavior_graph.neighbors(player_id):
            edge_data = self.behavior_graph[player_id][neighbor]
            similarity = edge_data.get("weight", 0)
            
            neighbors.append({
                "player_id": neighbor,
                "similarity": similarity,
                "pattern": self.behavior_graph.nodes[neighbor].get("pattern_type", "unknown")
            })
        
        neighbors.sort(key=lambda x: x["similarity"], reverse=True)
        
        return neighbors[:limit]
    
    def _extract_features(self, data: Dict[str, Any]) -> List[float]:
        """Extract numerical features from decision data"""
        
        cognitive_state = data.get("cognitive_state", {})
        context = data.get("context", {})
        history = data.get("history", [])
        
        features = []
        
        # Cognitive state features
        for module in ["logic", "empathy", "creativity", "fear", "trust"]:
            features.append(cognitive_state.get(module, 0))
        
        # Context features
        features.append(context.get("difficulty", 1.0))
        features.append(context.get("time_pressure", 0.5))
        features.append(len(history))
        
        # History features
        if history:
            recent_confidences = [h.get("confidence", 0.5) for h in history[-3:]]
            features.append(np.mean(recent_confidences))
        else:
            features.append(0.5)
        
        return features
    
    def _classify_pattern(
        self,
        mentor_prefs: Dict,
        cognitive_focuses: Dict,
        speeds: List,
        confidences: List
    ) -> str:
        """Classify player behavior pattern"""
        
        avg_speed = np.mean(speeds) if speeds else 5.0
        avg_confidence = np.mean(confidences) if confidences else 0.5
        
        # Fast, confident decisions
        if avg_speed < 3 and avg_confidence > 0.7:
            return "decisive"
        
        # Slow, thoughtful decisions
        elif avg_speed > 7 and avg_confidence > 0.6:
            return "contemplative"
        
        # Variable confidence
        elif np.std(confidences) > 0.3 if confidences else False:
            return "adaptive"
        
        # Consistent mentor preference
        elif mentor_prefs and max(mentor_prefs.values()) > len(speeds) * 0.6:
            return "specialized"
        
        else:
            return "balanced"
    
    def _calculate_consistency(self, history: List[Dict[str, Any]]) -> float:
        """Calculate consistency score"""
        
        if len(history) < 3:
            return 0.5
        
        # Check consistency in mentor choices
        mentors = [d.get("mentor_influence") for d in history if d.get("mentor_influence")]
        
        if not mentors:
            return 0.5
        
        # Calculate entropy
        unique_mentors = set(mentors)
        probabilities = [mentors.count(m) / len(mentors) for m in unique_mentors]
        entropy = -sum(p * np.log2(p) for p in probabilities if p > 0)
        
        # Normalize (lower entropy = more consistent)
        max_entropy = np.log2(len(unique_mentors)) if len(unique_mentors) > 1 else 1
        consistency = 1 - (entropy / max_entropy) if max_entropy > 0 else 1
        
        return consistency
    
    def _calculate_player_similarity(
        self,
        pattern1: Dict[str, Any],
        pattern2: Dict[str, Any]
    ) -> float:
        """Calculate similarity between two player patterns"""
        
        if not pattern1 or not pattern2:
            return 0.0
        
        similarity = 0.0
        
        # Pattern type match
        if pattern1.get("pattern_type") == pattern2.get("pattern_type"):
            similarity += 0.3
        
        # Cognitive focus match
        if pattern1.get("cognitive_focus") == pattern2.get("cognitive_focus"):
            similarity += 0.3
        
        # Confidence similarity
        conf_diff = abs(
            pattern1.get("average_confidence", 0.5) - 
            pattern2.get("average_confidence", 0.5)
        )
        similarity += (1 - conf_diff) * 0.2
        
        # Consistency similarity
        cons_diff = abs(
            pattern1.get("consistency_score", 0.5) -
            pattern2.get("consistency_score", 0.5)
        )
        similarity += (1 - cons_diff) * 0.2
        
        return similarity
    
    def _initialize_markov_chain(self) -> Dict[str, Dict[str, int]]:
        """Initialize empty Markov chain"""
        return {}
    
    def _save_decision_tree(self):
        """Save decision tree model"""
        Path("models").mkdir(exist_ok=True)
        with open("models/decision_tree.pkl", 'wb') as f:
            pickle.dump(self.decision_tree, f)
    
    def _save_markov_chain(self):
        """Save Markov chain model"""
        Path("models").mkdir(exist_ok=True)
        with open("models/markov_chain.pkl", 'wb') as f:
            pickle.dump(self.markov_chain, f)