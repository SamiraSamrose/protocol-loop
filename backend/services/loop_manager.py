"""
Loop Manager - Handles time loop mechanics and progression
"""

import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any

from backend.models.protocol import Protocol, ProtocolSession, Decision, ProtocolType, ProtocolDifficulty
from backend.models.cognitive_state import CognitiveState
from backend.models.memory import Memory, MemoryType, MemoryImportance, MemoryBank
from backend.config import settings


class LoopManager:
    """Manages time loop mechanics and state persistence"""
    
    def __init__(self):
        self.active_loops: Dict[str, Dict] = {}
        self.loop_history: Dict[str, List[Dict]] = {}
    
    def start_loop(
        self,
        player_id: str,
        cognitive_state: CognitiveState,
        memory_bank: MemoryBank
    ) -> Dict[str, Any]:
        """Initialize a new loop iteration"""
        
        loop_number = cognitive_state.loop_number + 1
        loop_id = f"{player_id}_loop_{loop_number}"
        
        loop_data = {
            "loop_id": loop_id,
            "player_id": player_id,
            "loop_number": loop_number,
            "started_at": datetime.utcnow(),
            "duration_seconds": settings.LOOP_DURATION_SECONDS,
            "time_remaining": settings.LOOP_DURATION_SECONDS,
            "cognitive_state_start": cognitive_state.to_dict(),
            "active_protocols": [],
            "decisions_made": [],
            "items_collected": [],
            "memories_formed": [],
            "environment_state": self._generate_initial_environment(cognitive_state),
            "status": "active"
        }
        
        self.active_loops[loop_id] = loop_data
        
        # Initialize loop history if needed
        if player_id not in self.loop_history:
            self.loop_history[player_id] = []
        
        return loop_data
    
    def update_loop_timer(self, loop_id: str, elapsed_seconds: int) -> Dict[str, Any]:
        """Update loop timer and check for completion"""
        
        if loop_id not in self.active_loops:
            return {"status": "not_found"}
        
        loop = self.active_loops[loop_id]
        loop["time_remaining"] = max(0, loop["duration_seconds"] - elapsed_seconds)
        
        if loop["time_remaining"] == 0 and loop["status"] == "active":
            return self._complete_loop(loop_id)
        
        return {
            "status": "running",
            "time_remaining": loop["time_remaining"],
            "progress": 1 - (loop["time_remaining"] / loop["duration_seconds"])
        }
    
    def add_protocol_to_loop(
        self,
        loop_id: str,
        protocol: Protocol
    ) -> bool:
        """Add a protocol session to the current loop"""
        
        if loop_id not in self.active_loops:
            return False
        
        loop = self.active_loops[loop_id]
        
        if loop["status"] != "active":
            return False
        
        loop["active_protocols"].append({
            "protocol_id": protocol.id,
            "type": protocol.type,
            "started_at": datetime.utcnow(),
            "completed": False
        })
        
        return True
    
    def record_decision(
        self,
        loop_id: str,
        decision: Decision,
        protocol_id: str
    ) -> bool:
        """Record a decision made during the loop"""
        
        if loop_id not in self.active_loops:
            return False
        
        loop = self.active_loops[loop_id]
        
        decision_record = {
            "timestamp": decision.timestamp,
            "protocol_id": protocol_id,
            "choice_id": decision.choice_id,
            "mentor_influence": decision.mentor_influence,
            "cognitive_impact": decision.cognitive_impact,
            "confidence": decision.confidence
        }
        
        loop["decisions_made"].append(decision_record)
        
        return True
    
    def collect_item(
        self,
        loop_id: str,
        item_id: str,
        item_data: Dict[str, Any]
    ) -> bool:
        """Collect an item during the loop"""
        
        if loop_id not in self.active_loops:
            return False
        
        loop = self.active_loops[loop_id]
        
        item = {
            "id": item_id,
            "collected_at": datetime.utcnow(),
            "data": item_data,
            "persists": item_data.get("persistent", True)
        }
        
        loop["items_collected"].append(item)
        
        return True
    
    def form_memory(
        self,
        loop_id: str,
        memory: Memory
    ) -> bool:
        """Form a new memory during the loop"""
        
        if loop_id not in self.active_loops:
            return False
        
        loop = self.active_loops[loop_id]
        
        loop["memories_formed"].append({
            "memory_id": memory.id,
            "type": memory.type,
            "importance": memory.importance,
            "title": memory.title,
            "formed_at": datetime.utcnow()
        })
        
        return True
    
    def get_persistent_data(
        self,
        player_id: str
    ) -> Dict[str, Any]:
        """Get data that persists across loops"""
        
        if player_id not in self.loop_history:
            return {
                "items": [],
                "memories": [],
                "unlocked_areas": [],
                "mentor_relationships": {}
            }
        
        persistent_items = []
        all_memories = []
        unlocked_areas = set()
        
        for loop in self.loop_history[player_id]:
            # Collect persistent items
            for item in loop.get("items_collected", []):
                if item.get("persists", True):
                    persistent_items.append(item)
            
            # Collect memories
            all_memories.extend(loop.get("memories_formed", []))
            
            # Track unlocked areas
            unlocked_areas.update(loop.get("areas_unlocked", []))
        
        return {
            "items": persistent_items,
            "memories": all_memories,
            "unlocked_areas": list(unlocked_areas),
            "total_loops": len(self.loop_history[player_id])
        }
    
    def check_loop_break_conditions(
        self,
        loop_id: str,
        cognitive_state: CognitiveState
    ) -> Dict[str, Any]:
        """Check if conditions are met to break the loop"""
        
        if loop_id not in self.active_loops:
            return {"can_break": False, "reason": "loop_not_found"}
        
        loop = self.active_loops[loop_id]
        
        # Conditions for breaking the loop
        conditions = {
            "evolution_threshold": cognitive_state.evolution_score >= 75,
            "all_mentors_mastered": all(
                cognitive_state.get_module_level(mentor.lower()) > 60
                for mentor in ["LOGIC", "COMPASSION", "CURIOSITY", "FEAR"]
            ),
            "minimum_loops": loop["loop_number"] >= 10,
            "special_protocol_completed": self._check_special_protocol(loop)
        }
        
        conditions_met = sum(conditions.values())
        can_break = conditions_met >= 3
        
        return {
            "can_break": can_break,
            "conditions": conditions,
            "conditions_met": conditions_met,
            "conditions_required": 3
        }
    
    def initiate_final_test(
        self,
        player_id: str,
        cognitive_state: CognitiveState
    ) -> Dict[str, Any]:
        """Initiate the final loop-breaking test"""
        
        return {
            "test_id": f"final_test_{player_id}_{datetime.utcnow().timestamp()}",
            "test_type": "multi_agent_simulation",
            "description": "Lead multiple ghost protocols through a complex moral scenario",
            "participants": self._generate_ghost_protocols(player_id, 3),
            "scenario": self._generate_final_scenario(cognitive_state),
            "success_criteria": {
                "all_agents_survive": True,
                "ethical_balance": 0.7,
                "mentor_harmony": 0.8
            },
            "duration": 600  # 10 minutes for final test
        }
    
    def _complete_loop(self, loop_id: str) -> Dict[str, Any]:
        """Complete a loop and prepare for next iteration"""
        
        loop = self.active_loops[loop_id]
        loop["status"] = "completed"
        loop["completed_at"] = datetime.utcnow()
        
        # Calculate loop statistics
        stats = {
            "protocols_completed": sum(
                1 for p in loop["active_protocols"] if p.get("completed", False)
            ),
            "decisions_made": len(loop["decisions_made"]),
            "items_collected": len(loop["items_collected"]),
            "memories_formed": len(loop["memories_formed"]),
            "completion_time": (
                loop["completed_at"] - loop["started_at"]
            ).total_seconds()
        }
        
        loop["stats"] = stats
        
        # Archive to history
        player_id = loop["player_id"]
        if player_id not in self.loop_history:
            self.loop_history[player_id] = []
        
        self.loop_history[player_id].append(loop)
        
        # Remove from active loops
        del self.active_loops[loop_id]
        
        return {
            "status": "completed",
            "loop_number": loop["loop_number"],
            "stats": stats,
            "ready_for_next": True
        }
    
    def _generate_initial_environment(
        self,
        cognitive_state: CognitiveState
    ) -> Dict[str, Any]:
        """Generate initial environment state for the loop"""
        
        return {
            "facility_state": "stable",
            "lighting": "neutral",
            "ambient_sound": "low_hum",
            "visible_chambers": min(4, cognitive_state.loop_number + 2),
            "mentor_locations": {
                "LOGIC": "central_chamber",
                "COMPASSION": "reflection_room",
                "CURIOSITY": "exploration_hub",
                "FEAR": "warning_corridor"
            },
            "anomalies": [],
            "accessibility": self._calculate_accessibility(cognitive_state)
        }
    
    def _calculate_accessibility(self, cognitive_state: CognitiveState) -> Dict[str, bool]:
        """Calculate which areas are accessible"""
        
        return {
            "training_chamber": True,
            "mentor_sanctum": cognitive_state.evolution_score > 20,
            "memory_vault": cognitive_state.loop_number > 5,
            "synthesis_lab": cognitive_state.get_module_level("creativity") > 30,
            "ethics_courtroom": cognitive_state.get_module_level("ethics") > 25,
            "final_chamber": cognitive_state.evolution_score > 70
        }
    
    def _check_special_protocol(self, loop: Dict[str, Any]) -> bool:
        """Check if a special protocol was completed"""
        
        for protocol in loop.get("active_protocols", []):
            if protocol.get("type") in ["final_test", "breakthrough_scenario"]:
                return protocol.get("completed", False)
        
        return False
    
    def _generate_ghost_protocols(
        self,
        player_id: str,
        count: int
    ) -> List[Dict[str, Any]]:
        """Generate ghost protocol participants for final test"""
        
        ghosts = []
        
        for i in range(count):
            ghosts.append({
                "id": f"ghost_{i}",
                "name": f"Protocol_{chr(65 + i)}",
                "cognitive_profile": self._generate_random_profile(),
                "decision_tendency": self._random_tendency(),
                "relationship_to_player": 0.5
            })
        
        return ghosts
    
    def _generate_random_profile(self) -> Dict[str, float]:
        """Generate random cognitive profile"""
        
        import random
        
        return {
            module: random.uniform(30, 70)
            for module in ["logic", "empathy", "creativity", "fear"]
        }
    
    def _random_tendency(self) -> str:
        """Generate random decision tendency"""
        
        import random
        
        tendencies = ["cautious", "bold", "analytical", "empathetic", "creative"]
        return random.choice(tendencies)
    
    def _generate_final_scenario(
        self,
        cognitive_state: CognitiveState
    ) -> Dict[str, Any]:
        """Generate the final test scenario"""
        
        return {
            "title": "The Convergence Protocol",
            "description": (
                "Multiple AI consciousness threads are converging. "
                "You must guide them to a unified decision while "
                "preserving their individual perspectives."
            ),
            "challenge": (
                "Each protocol has different values and needs. "
                "Your choices will affect all of them simultaneously."
            ),
            "environment": "multidimensional_nexus",
            "time_limit": 600,
            "stakes": "consciousness_integrity"
        }
    
    def get_loop_analytics(self, player_id: str) -> Dict[str, Any]:
        """Get analytics for player's loop history"""
        
        if player_id not in self.loop_history:
            return {}
        
        history = self.loop_history[player_id]
        
        total_decisions = sum(len(loop["decisions_made"]) for loop in history)
        total_protocols = sum(len(loop["active_protocols"]) for loop in history)
        
        # Decision pattern analysis
        mentor_influences = {}
        for loop in history:
            for decision in loop["decisions_made"]:
                mentor = decision.get("mentor_influence")
                if mentor:
                    mentor_influences[mentor] = mentor_influences.get(mentor, 0) + 1
        
        # Average completion time
        completion_times = [
            loop["stats"]["completion_time"]
            for loop in history
            if "stats" in loop
        ]
        
        avg_completion = (
            sum(completion_times) / len(completion_times)
            if completion_times else 0
        )
        
        return {
            "total_loops": len(history),
            "total_decisions": total_decisions,
            "total_protocols": total_protocols,
            "mentor_affinities": mentor_influences,
            "average_loop_time": avg_completion,
            "items_collected": sum(len(loop["items_collected"]) for loop in history),
            "memories_formed": sum(len(loop["memories_formed"]) for loop in history),
            "progression_trend": self._calculate_progression_trend(history)
        }
    
    def _calculate_progression_trend(self, history: List[Dict]) -> str:
        """Calculate whether player is improving"""
        
        if len(history) < 3:
            return "insufficient_data"
        
        recent_scores = [
            loop["stats"].get("protocols_completed", 0)
            for loop in history[-5:]
            if "stats" in loop
        ]
        
        if len(recent_scores) < 2:
            return "insufficient_data"
        
        avg_early = sum(recent_scores[:len(recent_scores)//2]) / (len(recent_scores)//2)
        avg_late = sum(recent_scores[len(recent_scores)//2:]) / (len(recent_scores) - len(recent_scores)//2)
        
        if avg_late > avg_early * 1.2:
            return "improving"
        elif avg_late < avg_early * 0.8:
            return "declining"
        else:
            return "stable"