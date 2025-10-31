"""
Protocol and Session models
"""

from datetime import datetime
from typing import List, Dict, Optional
from pydantic import BaseModel, Field
from enum import Enum


class ProtocolType(str, Enum):
    """Types of training protocols"""
    ETHICAL_DILEMMA = "ethical_dilemma"
    LOGIC_PUZZLE = "logic_puzzle"
    EMOTION_CALIBRATION = "emotion_calibration"
    MEMORY_COMPRESSION = "memory_compression"
    BIAS_IDENTIFICATION = "bias_identification"
    EMPATHY_SIMULATION = "empathy_simulation"
    CREATIVE_SYNTHESIS = "creative_synthesis"
    TRUST_EVALUATION = "trust_evaluation"


class ProtocolDifficulty(str, Enum):
    """Protocol difficulty levels"""
    NASCENT = "nascent"
    DEVELOPING = "developing"
    PROFICIENT = "proficient"
    ADVANCED = "advanced"
    TRANSCENDENT = "transcendent"


class Decision(BaseModel):
    """A single decision made during a protocol"""
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    choice_id: str
    choice_text: str
    mentor_influence: Optional[str] = None
    cognitive_impact: Dict[str, float] = Field(default_factory=dict)
    confidence: float = Field(ge=0.0, le=1.0)


class Protocol(BaseModel):
    """A training protocol/scenario"""
    id: str
    type: ProtocolType
    difficulty: ProtocolDifficulty
    title: str
    description: str
    scenario: str
    choices: List[Dict[str, any]]
    mentor_dialogue: Dict[str, str]  # mentor_name -> dialogue
    success_criteria: Dict[str, float]
    cognitive_rewards: Dict[str, float]
    estimated_duration: int  # seconds
    prerequisites: List[str] = Field(default_factory=list)
    
    class Config:
        use_enum_values = True


class ProtocolSession(BaseModel):
    """A complete protocol session within a loop"""
    session_id: str
    protocol_id: str
    loop_number: int
    player_id: str
    started_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    decisions: List[Decision] = Field(default_factory=list)
    outcome: Optional[str] = None
    score: float = 0.0
    cognitive_state_before: Dict[str, float]
    cognitive_state_after: Optional[Dict[str, float]] = None
    memories_gained: List[str] = Field(default_factory=list)
    items_gained: List[str] = Field(default_factory=list)
    
    def add_decision(self, decision: Decision):
        """Add a decision to the session"""
        self.decisions.append(decision)
    
    def complete(self, outcome: str, final_state: Dict[str, float]):
        """Mark session as complete"""
        self.completed_at = datetime.utcnow()
        self.outcome = outcome
        self.cognitive_state_after = final_state
        self.calculate_score()
    
    def calculate_score(self):
        """Calculate session score based on decisions"""
        if not self.decisions:
            self.score = 0.0
            return
        
        confidence_avg = sum(d.confidence for d in self.decisions) / len(self.decisions)
        growth_score = sum(
            abs(self.cognitive_state_after.get(k, 0) - self.cognitive_state_before.get(k, 0))
            for k in self.cognitive_state_before.keys()
        )
        self.score = (confidence_avg * 0.4 + min(growth_score, 1.0) * 0.6) * 100