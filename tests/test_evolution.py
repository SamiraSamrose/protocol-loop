"""
Tests for evolution engine functionality
"""

import pytest
from backend.services.evolution_engine import EvolutionEngine
from backend.models.cognitive_state import CognitiveState


class TestEvolutionEngine:
    """Test cases for evolution engine"""
    
    @pytest.fixture
    def evolution_engine(self):
        return EvolutionEngine()
    
    @pytest.fixture
    def cognitive_state(self, evolution_engine):
        return evolution_engine.initialize_cognitive_state("test_player")
    
    def test_initialize_cognitive_state(self, evolution_engine):
        """Test cognitive state initialization"""
        state = evolution_engine.initialize_cognitive_state("test_player")
        
        assert state is not None
        assert state.player_id == "test_player"
        assert state.loop_number == 0
        assert len(state.modules) > 0
        
        # Check core modules are unlocked
        assert state.modules["logic"].status.value != "locked"
        assert state.modules["empathy"].status.value != "locked"
    
    def test_apply_decision_impact(self, evolution_engine, cognitive_state):
        """Test applying decision impact to cognitive state"""
        initial_logic = cognitive_state.get_module_level("logic")
        
        impact = {"logic": 0.2, "empathy": 0.1}
        updated_state = evolution_engine.apply_decision_impact(
            cognitive_state,
            impact,
            "LOGIC"
        )
        
        assert updated_state.get_module_level("logic") > initial_logic
        assert updated_state.get_module_level("empathy") > cognitive_state.get_module_level("empathy")
    
    def test_module_unlocking(self, evolution_engine, cognitive_state):
        """Test module unlocking mechanism"""
        # Initially, advanced modules should be locked
        assert cognitive_state.modules["humor"].status.value == "locked"
        
        # Increase prerequisite modules
        cognitive_state.modules["creativity"].level = 40
        cognitive_state.modules["empathy"].level = 30
        
        # Apply decision to trigger unlock check
        evolution_engine.apply_decision_impact(
            cognitive_state,
            {"creativity": 0.1},
            None
        )
        
        # Humor should now be unlocked (requires creativity 30, empathy 20)
        assert cognitive_state.modules["humor"].status.value != "locked"
    
    def test_evolution_score_calculation(self, evolution_engine, cognitive_state):
        """Test evolution score calculation"""
        initial_score = cognitive_state.evolution_score
        
        # Increase several modules
        for module_name in ["logic", "empathy", "creativity"]:
            cognitive_state.modules[module_name].level = 50
        
        cognitive_state.calculate_evolution_score()
        
        assert cognitive_state.evolution_score > initial_score
    
    def test_dominant_traits_identification(self, evolution_engine, cognitive_state):
        """Test dominant traits identification"""
        # Set specific levels
        cognitive_state.modules["logic"].level = 80
        cognitive_state.modules["empathy"].level = 60
        cognitive_state.modules["creativity"].level = 40
        
        cognitive_state.update_dominant_traits()
        
        assert "logic" in cognitive_state.dominant_traits
        assert cognitive_state.dominant_traits[0] == "logic"
    
    def test_protocol_difficulty_calculation(self, evolution_engine, cognitive_state):
        """Test protocol difficulty calculation"""
        # Low level state
        difficulty = evolution_engine.calculate_protocol_difficulty(
            cognitive_state,
            "ethical_dilemma"
        )
        assert difficulty == "nascent"
        
        # High level state
        cognitive_state.modules["logic"].level = 70
        cognitive_state.modules["empathy"].level = 70
        
        difficulty = evolution_engine.calculate_protocol_difficulty(
            cognitive_state,
            "ethical_dilemma"
        )
        assert difficulty in ["proficient", "advanced", "transcendent"]
    
    def test_evolution_insights(self, evolution_engine, cognitive_state):
        """Test evolution insights generation"""
        insights = evolution_engine.generate_evolution_insights(
            cognitive_state,
            []
        )
        
        assert isinstance(insights, list)
        assert len(insights) > 0
    
    def test_consciousness_tree_comparison(self, evolution_engine):
        """Test comparing two consciousness trees"""
        state1 = evolution_engine.initialize_cognitive_state("player1")
        state2 = evolution_engine.initialize_cognitive_state("player2")
        
        # Make them different
        state1.modules["logic"].level = 70
        state2.modules["empathy"].level = 70
        
        comparison = evolution_engine.compare_consciousness_trees(state1, state2)
        
        assert "similarity_score" in comparison
        assert "divergent_traits" in comparison
        assert comparison["similarity_score"] >= 0
        assert comparison["similarity_score"] <= 1