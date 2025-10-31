"""
Cognitive state and module models
"""

from datetime import datetime
from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from enum import Enum


class ModuleStatus(str, Enum):
    """Status of a cognitive module"""
    LOCKED = "locked"
    NASCENT = "nascent"
    DEVELOPING = "developing"
    ACTIVE = "active"
    MASTERED = "mastered"


class CognitiveModule(BaseModel):
    """A single cognitive capability module"""
    name: str
    level: float = Field(default=0.0, ge=0.0, le=100.0)
    status: ModuleStatus = ModuleStatus.LOCKED
    experience_points: int = 0
    unlock_requirements: Dict[str, float] = Field(default_factory=dict)
    description: str
    icon: str
    color: str
    
    def gain_experience(self, amount: float):
        """Add experience and potentially level up"""
        self.experience_points += int(amount * 100)
        self.level = min(100.0, self.level + amount)
        self.update_status()
    
    def update_status(self):
        """Update module status based on level"""
        if self.level == 0:
            self.status = ModuleStatus.LOCKED
        elif self.level < 20:
            self.status = ModuleStatus.NASCENT
        elif self.level < 50:
            self.status = ModuleStatus.DEVELOPING
        elif self.level < 90:
            self.status = ModuleStatus.ACTIVE
        else:
            self.status = ModuleStatus.MASTERED
    
    def is_unlocked(self, current_state: Dict[str, float]) -> bool:
        """Check if module can be unlocked"""
        for req_module, req_level in self.unlock_requirements.items():
            if current_state.get(req_module, 0) < req_level:
                return False
        return True


class CognitiveState(BaseModel):
    """Complete cognitive state of a Protocol AI"""
    player_id: str
    loop_number: int = 0
    modules: Dict[str, CognitiveModule] = Field(default_factory=dict)
    total_experience: int = 0
    evolution_score: float = 0.0
    personality_vector: Dict[str, float] = Field(default_factory=dict)
    dominant_traits: List[str] = Field(default_factory=list)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    def get_module_level(self, module_name: str) -> float:
        """Get level of a specific module"""
        return self.modules.get(module_name, CognitiveModule(
            name=module_name,
            description="",
            icon="",
            color=""
        )).level
    
    def update_module(self, module_name: str, delta: float):
        """Update a cognitive module"""
        if module_name not in self.modules:
            return
        
        self.modules[module_name].gain_experience(delta)
        self.total_experience += int(delta * 100)
        self.calculate_evolution_score()
        self.update_dominant_traits()
    
    def calculate_evolution_score(self):
        """Calculate overall evolution score"""
        if not self.modules:
            self.evolution_score = 0.0
            return
        
        total_level = sum(m.level for m in self.modules.values())
        max_possible = len(self.modules) * 100
        self.evolution_score = (total_level / max_possible) * 100 if max_possible > 0 else 0
    
    def update_dominant_traits(self):
        """Identify top 3 dominant traits"""
        sorted_modules = sorted(
            self.modules.items(),
            key=lambda x: x[1].level,
            reverse=True
        )
        self.dominant_traits = [m[0] for m in sorted_modules[:3]]
    
    def to_dict(self) -> Dict[str, float]:
        """Convert to simple dict for serialization"""
        return {name: module.level for name, module in self.modules.items()}
    
    def get_neural_tree_data(self) -> Dict:
        """Generate data for neural tree visualization"""
        nodes = []
        links = []
        
        for name, module in self.modules.items():
            nodes.append({
                "id": name,
                "level": module.level,
                "status": module.status.value,
                "color": module.color,
                "icon": module.icon
            })
            
            # Create links based on dependencies
            for req_module in module.unlock_requirements.keys():
                if req_module in self.modules:
                    links.append({
                        "source": req_module,
                        "target": name,
                        "strength": module.level / 100
                    })
        
        return {
            "nodes": nodes,
            "links": links,
            "evolution_score": self.evolution_score,
            "loop_number": self.loop_number
        }