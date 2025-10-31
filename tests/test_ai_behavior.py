"""
Tests for AI/ML behavior prediction
"""

import pytest
from backend.services.ml_service import MLService


class TestAIBehavior:
    """Test cases for ML behavior prediction"""
    
    @pytest.fixture
    def ml_service(self):
        return MLService()
    
    def test_pattern_analysis(self, ml_service):
        """Test player pattern analysis"""
        decision_history = [
            {
                "mentor_influence": "LOGIC",
                "confidence": 0.8,
                "decision_time": 5,
                "cognitive_impact": {"logic": 0.2}
            },
            {
                "mentor_influence": "LOGIC",
                "confidence": 0.85,
                "decision_time": 4,
                "cognitive_impact": {"logic": 0.15}
            },
            {
                "mentor_influence": "COMPASSION",
                "confidence": 0.6,
                "decision_time": 8,
                "cognitive_impact": {"empathy": 0.2}
            }
        ]
        
        pattern = ml_service.analyze_player_pattern("test_player", decision_history)
        
        assert "pattern_type" in pattern
        assert "mentor_affinity" in pattern
        assert pattern["mentor_affinity"] == "LOGIC"
    
    def test_decision_prediction(self, ml_service):
        """Test decision prediction"""
        cognitive_state = {
            "logic": 60,
            "empathy": 40,
            "creativity": 30,
            "fear": 20,
            "trust": 25
        }
        
        context = {"difficulty": 1.0, "time_pressure": 0.5}
        history = []
        
        prediction = ml_service.predict_next_decision(
            cognitive_state,
            context,
            history
        )
        
        assert "predicted_decision" in prediction
        assert "confidence" in prediction
        assert 0 <= prediction["confidence"] <= 1
    
    def test_markov_chain_update(self, ml_service):
        """Test Markov chain state transitions"""
        state_sequence = ["state_A", "state_B", "state_C", "state_B", "state_A"]
        
        ml_service.update_markov_chain(state_sequence)
        
        # Check that transitions were recorded
        assert "state_A" in ml_service.markov_chain
        assert "state_B" in ml_service.markov_chain["state_A"]
    
    def test_markov_prediction(self, ml_service):
        """Test Markov chain prediction"""
        # Build chain
        state_sequence = ["start", "middle", "end", "start", "middle", "end"]
        ml_service.update_markov_chain(state_sequence)
        
        # Predict next state
        next_state = ml_service.predict_next_state("start", temperature=1.0)
        
        assert next_state in ["middle", "unknown"]
    
    def test_adaptive_difficulty(self, ml_service):
        """Test adaptive difficulty calculation"""
        # Train pattern
        ml_service.player_patterns["test_player"] = {
            "average_confidence": 0.8,
            "consistency_score": 0.7
        }
        
        performance = {"success_rate": 0.85}
        
        multiplier = ml_service.generate_adaptive_difficulty("test_player", performance)
        
        assert multiplier > 1.0  # Should increase difficulty
        assert multiplier <= 2.0
    
    def test_player_similarity(self, ml_service):
        """Test player similarity calculation"""
        pattern1 = {
            "pattern_type": "decisive",
            "cognitive_focus": "logic",
            "average_confidence": 0.8,
            "consistency_score": 0.7
        }
        
        pattern2 = {
            "pattern_type": "decisive",
            "cognitive_focus": "logic",
            "average_confidence": 0.75,
            "consistency_score": 0.65
        }
        
        similarity = ml_service._calculate_player_similarity(pattern1, pattern2)
        
        assert 0 <= similarity <= 1
        assert similarity > 0.5  # Should be fairly similar
    
    def test_behavior_graph_building(self, ml_service):
        """Test behavior graph construction"""
        player_histories = {
            "player1": [
                {"mentor_influence": "LOGIC", "confidence": 0.8, "decision_time": 5}
            ],
            "player2": [
                {"mentor_influence": "LOGIC", "confidence": 0.75, "decision_time": 6}
            ]
        }
        
        ml_service.build_behavior_graph(player_histories)
        
        assert ml_service.behavior_graph.number_of_nodes() == 2