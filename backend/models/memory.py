"""
Memory system models
"""

from datetime import datetime
from typing import Optional, List, Dict
from pydantic import BaseModel, Field
from enum import Enum


class MemoryType(str, Enum):
    """Types of memories that can be retained"""
    DECISION = "decision"
    LESSON = "lesson"
    MENTOR_WISDOM = "mentor_wisdom"
    EMOTIONAL_MOMENT = "emotional_moment"
    DISCOVERY = "discovery"
    FAILURE = "failure"
    BREAKTHROUGH = "breakthrough"
    SOCIAL_INTERACTION = "social_interaction"


class MemoryImportance(str, Enum):
    """Importance levels for memory retention"""
    TRIVIAL = "trivial"
    MINOR = "minor"
    SIGNIFICANT = "significant"
    CRITICAL = "critical"
    CORE = "core"


class Memory(BaseModel):
    """A retained memory from a loop"""
    id: str
    player_id: str
    loop_number: int
    type: MemoryType
    importance: MemoryImportance
    title: str
    content: str
    context: Dict[str, any] = Field(default_factory=dict)
    cognitive_impact: Dict[str, float] = Field(default_factory=dict)
    related_protocol: Optional[str] = None
    mentor_source: Optional[str] = None
    emotional_valence: float = Field(default=0.0, ge=-1.0, le=1.0)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    access_count: int = 0
    last_accessed: Optional[datetime] = None
    tags: List[str] = Field(default_factory=list)
    
    def access(self):
        """Record memory access"""
        self.access_count += 1
        self.last_accessed = datetime.utcnow()
    
    def get_decay_factor(self) -> float:
        """Calculate memory decay based on age and access"""
        if not self.last_accessed:
            return 1.0
        
        days_since_access = (datetime.utcnow() - self.last_accessed).days
        importance_multiplier = {
            MemoryImportance.TRIVIAL: 0.5,
            MemoryImportance.MINOR: 0.7,
            MemoryImportance.SIGNIFICANT: 0.9,
            MemoryImportance.CRITICAL: 0.95,
            MemoryImportance.CORE: 1.0
        }[self.importance]
        
        # Memories decay slower if accessed frequently and are important
        decay = max(0.1, 1.0 - (days_since_access * 0.05 / (1 + self.access_count * 0.1)))
        return decay * importance_multiplier
    
    class Config:
        use_enum_values = True


class MemoryBank(BaseModel):
    """Collection of memories for a player"""
    player_id: str
    memories: List[Memory] = Field(default_factory=list)
    total_memories: int = 0
    capacity: int = 100
    
    def add_memory(self, memory: Memory):
        """Add a new memory, removing least important if at capacity"""
        if len(self.memories) >= self.capacity:
            self.consolidate_memories()
        
        self.memories.append(memory)
        self.total_memories += 1
    
    def consolidate_memories(self):
        """Remove or merge least important memories"""
        # Calculate retention score for each memory
        scored_memories = [
            (m, m.get_decay_factor() * m.access_count * (1 + len(m.tags) * 0.1))
            for m in self.memories
        ]
        
        # Keep top memories by score
        scored_memories.sort(key=lambda x: x[1], reverse=True)
        self.memories = [m[0] for m in scored_memories[:self.capacity]]
    
    def get_memories_by_type(self, memory_type: MemoryType) -> List[Memory]:
        """Retrieve memories of a specific type"""
        return [m for m in self.memories if m.type == memory_type]
    
    def get_relevant_memories(self, context: Dict[str, any], limit: int = 5) -> List[Memory]:
        """Get most relevant memories for current context"""
        scored = []
        
        for memory in self.memories:
            score = memory.get_decay_factor()
            
            # Boost score if context matches
            if memory.related_protocol == context.get("protocol_id"):
                score += 0.5
            
            # Boost for matching tags
            matching_tags = set(memory.tags) & set(context.get("tags", []))
            score += len(matching_tags) * 0.2
            
            scored.append((memory, score))
        
        scored.sort(key=lambda x: x[1], reverse=True)
        return [m[0] for m in scored[:limit]]
    
    def export_for_sharing(self) -> Dict:
        """Export memories for social sharing"""
        return {
            "player_id": self.player_id,
            "total_memories": self.total_memories,
            "significant_memories": [
                {
                    "title": m.title,
                    "type": m.type.value,
                    "loop": m.loop_number,
                    "importance": m.importance.value,
                    "emotional_valence": m.emotional_valence
                }
                for m in self.memories
                if m.importance in [MemoryImportance.CRITICAL, MemoryImportance.CORE]
            ]
        }