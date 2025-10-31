"""
Tests for loop system functionality
"""

import pytest
from datetime import datetime

from backend.services.loop_manager import LoopManager
from backend.models.cognitive_state import CognitiveState
from backend.models.memory import MemoryBank
from backend.services.evolution_engine import EvolutionEngine


class TestLoopSystem:
    """Test cases for loop system"""
    
    @pytest.fixture
    def loop_manager(self):
        return LoopManager()
    
    @pytest.fixture
    def evolution_engine(self):
        return EvolutionEngine()
    
    @pytest.fixture
    def player_state(self, evolution_engine):
        return evolution_engine.initialize_cognitive_state("test_player")
    
    @pytest.fixture
    def memory_bank(self):
        return MemoryBank(player_id="test_player")
    
    def test_start_loop(self, loop_manager, player_state, memory_bank):
        """Test starting a new loop"""
        loop_data = loop_manager.start_loop("test_player", player_state, memory_bank)
        
        assert loop_data is not None
        assert loop_data["player_id"] == "test_player"
        assert loop_data["loop_number"] == 1
        assert loop_data["status"] == "active"
        assert "loop_id" in loop_data
    
    def test_loop_timer_update(self, loop_manager, player_state, memory_bank):
        """Test loop timer updates"""
        loop_data = loop_manager.start_loop("test_player", player_state, memory_bank)
        loop_id = loop_data["loop_id"]
        
        result = loop_manager.update_loop_timer(loop_id, 60)
        
        assert result["status"] == "running"
        assert result["time_remaining"] == 240  # 300 - 60
    
    def test_loop_completion(self, loop_manager, player_state, memory_bank):
        """Test loop completion"""
        loop_data = loop_manager.start_loop("test_player", player_state, memory_bank)
        loop_id = loop_data["loop_id"]
        
        result = loop_manager._complete_loop(loop_id)
        
        assert result["status"] == "completed"
        assert "stats" in result
        assert result["ready_for_next"] is True
    
    def test_persistent_data(self, loop_manager, player_state, memory_bank):
        """Test data persistence across loops"""
        # Start and complete first loop
        loop1 = loop_manager.start_loop("test_player", player_state, memory_bank)
        loop_manager.collect_item(loop1["loop_id"], "item_1", {"persistent": True})
        loop_manager._complete_loop(loop1["loop_id"])
        
        # Start second loop
        loop2 = loop_manager.start_loop("test_player", player_state, memory_bank)
        
        # Get persistent data
        persistent = loop_manager.get_persistent_data("test_player")
        
        assert len(persistent["items"]) == 1
        assert persistent["total_loops"] == 1
    
    def test_loop_break_conditions(self, loop_manager, player_state, memory_bank):
        """Test loop break conditions"""
        loop_data = loop_manager.start_loop("test_player", player_state, memory_bank)
        loop_id = loop_data["loop_id"]
        
        # Test with low evolution
        result = loop_manager.check_loop_break_conditions(loop_id, player_state)
        assert result["can_break"] is False
        
        # Simulate high evolution
        player_state.evolution_score = 80
        player_state.loop_number = 15
        
        result = loop_manager.check_loop_break_conditions(loop_id, player_state)
        # Should be closer to breaking conditions
        assert result["conditions_met"] >= 2
    
    def test_multiple_loops(self, loop_manager, player_state, memory_bank):
        """Test multiple loop iterations"""
        for i in range(3):
            loop_data = loop_manager.start_loop("test_player", player_state, memory_bank)
            loop_manager._complete_loop(loop_data["loop_id"])
            player_state.loop_number += 1
        
        analytics = loop_manager.get_loop_analytics("test_player")
        
        assert analytics["total_loops"] == 3
        assert "progression_trend" in analytics