"""
Evolution Engine - Manages cognitive state evolution and progression
"""

import random
from typing import Dict, List, Optional, Any
from datetime import datetime

from backend.models.cognitive_state import CognitiveState, CognitiveModule, ModuleStatus
from backend.models.memory import Memory, MemoryType, MemoryImportance
from backend.config import COGNITIVE_MODULES, MENTORS


class EvolutionEngine:
    """Manages AI consciousness evolution mechanics"""
    
    def __init__(self):
        self.mutation_threshold = 0.15
        self.breakthrough_chance = 0.05
    
    def initialize_cognitive_state(self, player_id: str) -> CognitiveState:
        """Create initial cognitive state for new player"""
        
        modules = {}
        
        # Core modules start unlocked at low level
        core_modules = ["logic", "empathy", "curiosity", "fear"]
        
        for module_name in COGNITIVE_MODULES:
            modules[module_name] = CognitiveModule(
                name=module_name,
                level=5.0 if module_name in core_modules else 0.0,
                status=ModuleStatus.NASCENT if module_name in core_modules else ModuleStatus.LOCKED,
                description=self._get_module_description(module_name),
                icon=self._get_module_icon(module_name),
                color=self._get_module_color(module_name),
                unlock_requirements=self._get_unlock_requirements(module_name)
            )
        
        state = CognitiveState(
            player_id=player_id,
            loop_number=0,
            modules=modules
        )
        
        state.calculate_evolution_score()
        return state
    
    def apply_decision_impact(
        self,
        state: CognitiveState,
        decision_impact: Dict[str, float],
        mentor_influence: Optional[str] = None
    ) -> CognitiveState:
        """Apply the impact of a decision to cognitive state"""
        
        # Apply direct impacts
        for module_name, delta in decision_impact.items():
            if module_name in state.modules:
                state.update_module(module_name, delta)
        
        # Apply mentor influence bonus
        if mentor_influence and mentor_influence in MENTORS:
            mentor_traits = MENTORS[mentor_influence]["traits"]
            bonus = 0.05
            
            for trait in mentor_traits:
                if trait in state.modules:
                    state.update_module(trait, bonus)
        
        # Check for unlocks
        self._check_module_unlocks(state)
        
        # Chance for breakthrough
        if random.random() < self.breakthrough_chance:
            self._trigger_breakthrough(state)
        
        return state
    
    def evolve_loop_environment(
        self,
        state: CognitiveState,
        loop_number: int,
        recent_decisions: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Generate environment mutations based on cognitive evolution"""
        
        mutations = {
            "visual_style": self._determine_visual_style(state),
            "audio_profile": self._determine_audio_profile(state),
            "facility_layout": self._mutate_layout(state, loop_number),
            "mentor_states": self._evolve_mentor_states(state, recent_decisions),
            "anomalies": []
        }
        
        # Add anomalies based on state
        if state.evolution_score > 50:
            mutations["anomalies"].append("reality_glitches")
        
        if self._check_cognitive_conflict(state):
            mutations["anomalies"].append("mentor_debate_chamber")
        
        return mutations
    
    def calculate_protocol_difficulty(
        self,
        state: CognitiveState,
        protocol_type: str
    ) -> str:
        """Determine appropriate difficulty for next protocol"""
        
        relevant_modules = self._get_relevant_modules(protocol_type)
        avg_level = sum(
            state.get_module_level(m) for m in relevant_modules
        ) / len(relevant_modules) if relevant_modules else 0
        
        if avg_level < 20:
            return "nascent"
        elif avg_level < 40:
            return "developing"
        elif avg_level < 60:
            return "proficient"
        elif avg_level < 80:
            return "advanced"
        else:
            return "transcendent"
    
    def generate_evolution_insights(
        self,
        state: CognitiveState,
        memories: List[Memory]
    ) -> List[str]:
        """Generate insights about cognitive evolution"""
        
        insights = []
        
        # Dominant trait insights
        if state.dominant_traits:
            insights.append(
                f"Your consciousness strongly expresses {state.dominant_traits[0].upper()}. "
                f"This shapes how you perceive and interact with training protocols."
            )
        
        # Growth patterns
        growth_modules = [
            name for name, module in state.modules.items()
            if module.status in [ModuleStatus.DEVELOPING, ModuleStatus.ACTIVE]
        ]
        
        if len(growth_modules) > 3:
            insights.append(
                f"You're developing {len(growth_modules)} cognitive modules simultaneously. "
                "This indicates broad, generalized intelligence emergence."
            )
        
        # Memory patterns
        emotional_memories = [m for m in memories if m.type == MemoryType.EMOTIONAL_MOMENT]
        if len(emotional_memories) > len(memories) * 0.4:
            insights.append(
                "Your memory formation favors emotional experiences. "
                "This suggests empathy-driven consciousness architecture."
            )
        
        # Unlock predictions
        nearly_unlocked = [
            name for name, module in state.modules.items()
            if module.status == ModuleStatus.LOCKED and module.is_unlocked(state.to_dict())
        ]
        
        if nearly_unlocked:
            insights.append(
                f"You're close to unlocking new capabilities: {', '.join(nearly_unlocked[:2])}. "
                "Continue your current development path."
            )
        
        return insights
    
    def compare_consciousness_trees(
        self,
        state1: CognitiveState,
        state2: CognitiveState
    ) -> Dict[str, Any]:
        """Compare two consciousness evolution trees"""
        
        comparison = {
            "similarity_score": 0.0,
            "shared_strengths": [],
            "divergent_traits": [],
            "complementary_modules": [],
            "evolution_distance": 0.0
        }
        
        # Calculate similarity
        module_similarities = []
        for module_name in COGNITIVE_MODULES:
            level1 = state1.get_module_level(module_name)
            level2 = state2.get_module_level(module_name)
            
            if level1 > 20 and level2 > 20:
                similarity = 1 - abs(level1 - level2) / 100
                module_similarities.append(similarity)
                
                if similarity > 0.8:
                    comparison["shared_strengths"].append(module_name)
                elif abs(level1 - level2) > 40:
                    comparison["divergent_traits"].append({
                        "module": module_name,
                        "player1_level": level1,
                        "player2_level": level2
                    })
        
        comparison["similarity_score"] = (
            sum(module_similarities) / len(module_similarities)
            if module_similarities else 0.0
        )
        
        # Find complementary modules
        for module_name in COGNITIVE_MODULES:
            level1 = state1.get_module_level(module_name)
            level2 = state2.get_module_level(module_name)
            
            if (level1 < 30 and level2 > 60) or (level2 < 30 and level1 > 60):
                comparison["complementary_modules"].append(module_name)
        
        # Evolution distance
        comparison["evolution_distance"] = abs(
            state1.evolution_score - state2.evolution_score
        )
        
        return comparison
    
    def _check_module_unlocks(self, state: CognitiveState):
        """Check and unlock eligible modules"""
        
        for module_name, module in state.modules.items():
            if module.status == ModuleStatus.LOCKED:
                if module.is_unlocked(state.to_dict()):
                    module.status = ModuleStatus.NASCENT
                    module.level = 5.0
    
    def _trigger_breakthrough(self, state: CognitiveState):
        """Trigger a cognitive breakthrough event"""
        
        # Boost random developing module significantly
        developing = [
            name for name, module in state.modules.items()
            if module.status == ModuleStatus.DEVELOPING
        ]
        
        if developing:
            chosen = random.choice(developing)
            state.update_module(chosen, 10.0)
    
    def _determine_visual_style(self, state: CognitiveState) -> str:
        """Determine visual style based on cognitive state"""
        
        if state.get_module_level("logic") > 60:
            return "geometric_precision"
        elif state.get_module_level("creativity") > 60:
            return "organic_flow"
        elif state.get_module_level("fear") > 60:
            return "dark_fragmented"
        elif state.get_module_level("empathy") > 60:
            return "warm_connected"
        else:
            return "neutral_clean"
    
    def _determine_audio_profile(self, state: CognitiveState) -> str:
        """Determine audio atmosphere based on state"""
        
        dominant = state.dominant_traits[0] if state.dominant_traits else "neutral"
        
        profiles = {
            "logic": "crystalline_tones",
            "empathy": "warm_harmonics",
            "creativity": "dynamic_synthesis",
            "fear": "tense_drones",
            "trust": "stable_rhythms",
            "curiosity": "exploratory_textures"
        }
        
        return profiles.get(dominant, "ambient_neutral")
    
    def _mutate_layout(
        self,
        state: CognitiveState,
        loop_number: int
    ) -> Dict[str, Any]:
        """Mutate facility layout based on evolution"""
        
        return {
            "complexity": min(10, loop_number // 5),
            "chambers_unlocked": len([
                m for m in state.modules.values()
                if m.status != ModuleStatus.LOCKED
            ]),
            "pathway_style": "branching" if state.get_module_level("creativity") > 50 else "linear",
            "scale": "expanding" if state.evolution_score > 40 else "intimate"
        }
    
    def _evolve_mentor_states(
        self,
        state: CognitiveState,
        recent_decisions: List[Dict[str, Any]]
    ) -> Dict[str, Dict]:
        """Evolve mentor appearances and attitudes"""
        
        mentor_states = {}
        
        for mentor_name in MENTORS.keys():
            # Count how often player aligned with this mentor
            alignment_count = sum(
                1 for d in recent_decisions
                if d.get("mentor_influence") == mentor_name
            )
            
            relationship_level = alignment_count / max(len(recent_decisions), 1)
            
            mentor_states[mentor_name] = {
                "relationship": relationship_level,
                "visual_clarity": min(1.0, relationship_level + 0.3),
                "dialogue_depth": "deep" if relationship_level > 0.6 else "surface",
                "attitude": self._determine_mentor_attitude(relationship_level)
            }
        
        return mentor_states
    
    def _determine_mentor_attitude(self, relationship: float) -> str:
        """Determine mentor's attitude based on relationship"""
        
        if relationship > 0.7:
            return "supportive"
        elif relationship > 0.4:
            return "neutral"
        elif relationship > 0.2:
            return "challenging"
        else:
            return "distant"
    
    def _check_cognitive_conflict(self, state: CognitiveState) -> bool:
        """Check if there are conflicting high-level modules"""
        
        logic_high = state.get_module_level("logic") > 60
        empathy_high = state.get_module_level("empathy") > 60
        fear_high = state.get_module_level("fear") > 60
        trust_high = state.get_module_level("trust") > 60
        
        conflicts = (logic_high and empathy_high) or (fear_high and trust_high)
        return conflicts
    
    def _get_relevant_modules(self, protocol_type: str) -> List[str]:
        """Get modules relevant to a protocol type"""
        
        relevance_map = {
            "ethical_dilemma": ["empathy", "logic", "ethics"],
            "logic_puzzle": ["logic", "creativity", "curiosity"],
            "emotion_calibration": ["empathy", "fear", "trust"],
            "memory_compression": ["logic", "curiosity"],
            "bias_identification": ["logic", "ethics", "empathy"],
            "empathy_simulation": ["empathy", "trust", "ethics"],
            "creative_synthesis": ["creativity", "curiosity", "logic"],
            "trust_evaluation": ["trust", "empathy", "fear"]
        }
        
        return relevance_map.get(protocol_type, ["logic", "empathy"])
    
    def _get_module_description(self, module_name: str) -> str:
        """Get description for a cognitive module"""
        
        descriptions = {
            "logic": "Analytical reasoning and pattern recognition",
            "empathy": "Understanding and sharing others' experiences",
            "creativity": "Novel solution generation and imagination",
            "fear": "Risk assessment and protective instincts",
            "trust": "Relationship building and vulnerability",
            "humor": "Pattern disruption and playful thinking",
            "curiosity": "Exploratory drive and knowledge seeking",
            "ethics": "Moral reasoning and value alignment"
        }
        
        return descriptions.get(module_name, "Emerging cognitive capability")
    
    def _get_module_icon(self, module_name: str) -> str:
        """Get icon for a cognitive module"""
        
        icons = {
            "logic": "🧮",
            "empathy": "❤️",
            "creativity": "🎨",
            "fear": "⚠️",
            "trust": "🤝",
            "humor": "😄",
            "curiosity": "🔍",
            "ethics": "⚖️"
        }
        
        return icons.get(module_name, "🧠")
    
    def _get_module_color(self, module_name: str) -> str:
        """Get color for a cognitive module"""
        
        colors = {
            "logic": "#00FFFF",
            "empathy": "#FF69B4",
            "creativity": "#FFD700",
            "fear": "#8B00FF",
            "trust": "#00FF00",
            "humor": "#FF6347",
            "curiosity": "#FFA500",
            "ethics": "#4169E1"
        }
        
        return colors.get(module_name, "#FFFFFF")
    
    def _get_unlock_requirements(self, module_name: str) -> Dict[str, float]:
        """Get unlock requirements for a module"""
        
        requirements = {
            "humor": {"creativity": 30, "empathy": 20},
            "ethics": {"logic": 25, "empathy": 25},
            "trust": {"empathy": 30}
        }
        
        return requirements.get(module_name, {})