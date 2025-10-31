"""
Protocol and loop management routes
"""

from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from typing import Dict, List, Any, Optional
from datetime import datetime
import json

from backend.models.protocol import Protocol, ProtocolSession, Decision, ProtocolType
from backend.models.cognitive_state import CognitiveState
from backend.services.loop_manager import LoopManager
from backend.services.llm_service import LLMService
from backend.services.evolution_engine import EvolutionEngine

router = APIRouter(prefix="/api/protocols", tags=["protocols"])

# Service instances
loop_manager = LoopManager()
llm_service = LLMService()
evolution_engine = EvolutionEngine()

# In-memory storage (replace with database in production)
active_sessions: Dict[str, ProtocolSession] = {}
player_states: Dict[str, CognitiveState] = {}


@router.post("/start-loop")
async def start_loop(player_id: str) -> Dict[str, Any]:
    """Start a new loop iteration"""
    
    # Get or create player state
    if player_id not in player_states:
        player_states[player_id] = evolution_engine.initialize_cognitive_state(player_id)
    
    cognitive_state = player_states[player_id]
    
    # Start loop
    loop_data = loop_manager.start_loop(
        player_id=player_id,
        cognitive_state=cognitive_state,
        memory_bank=None  # TODO: Add memory bank
    )
    
    return {
        "success": True,
        "loop_id": loop_data["loop_id"],
        "loop_number": loop_data["loop_number"],
        "duration": loop_data["duration_seconds"],
        "environment": loop_data["environment_state"]
    }


@router.post("/generate-protocol")
async def generate_protocol(
    player_id: str,
    protocol_type: Optional[str] = None
) -> Dict[str, Any]:
    """Generate a new protocol scenario"""
    
    if player_id not in player_states:
        raise HTTPException(status_code=404, detail="Player not found")
    
    cognitive_state = player_states[player_id]
    
    # Determine protocol type if not specified
    if not protocol_type:
        from backend.utils.decision_tree import DecisionTreeUtil
        recommendation = DecisionTreeUtil.get_protocol_recommendation(
            cognitive_state.to_dict(),
            [],
            cognitive_state.loop_number
        )
        protocol_type = recommendation["protocol_type"]
    
    # Determine difficulty
    difficulty = evolution_engine.calculate_protocol_difficulty(
        cognitive_state,
        protocol_type
    )
    
    # Generate scenario using LLM
    scenario_data = await llm_service.generate_ethical_dilemma(
        difficulty=difficulty,
        cognitive_focus=cognitive_state.dominant_traits,
        player_history={
            "dominant_traits": cognitive_state.dominant_traits,
            "evolution_score": cognitive_state.evolution_score
        }
    )
    
    return {
        "success": True,
        "protocol": scenario_data,
        "difficulty": difficulty,
        "estimated_duration": 180
    }


@router.post("/make-decision")
async def make_decision(
    session_id: str,
    choice_id: str,
    confidence: float,
    player_id: str
) -> Dict[str, Any]:
    """Record a decision and apply its effects"""
    
    if player_id not in player_states:
        raise HTTPException(status_code=404, detail="Player not found")
    
    cognitive_state = player_states[player_id]
    
    # Create decision object
    decision = Decision(
        choice_id=choice_id,
        choice_text="",  # TODO: Get from protocol data
        confidence=confidence,
        cognitive_impact={}  # TODO: Get from protocol data
    )
    
    # Apply decision impact
    # TODO: Get actual impact from protocol choice
    sample_impact = {"logic": 0.1, "empathy": 0.05}
    
    updated_state = evolution_engine.apply_decision_impact(
        cognitive_state,
        sample_impact,
        mentor_influence="LOGIC"
    )
    
    player_states[player_id] = updated_state
    
    return {
        "success": True,
        "new_state": updated_state.to_dict(),
        "evolution_score": updated_state.evolution_score,
        "insights": evolution_engine.generate_evolution_insights(updated_state, [])
    }


@router.get("/loop-status/{loop_id}")
async def get_loop_status(loop_id: str) -> Dict[str, Any]:
    """Get current loop status"""
    
    # TODO: Implement proper loop tracking
    return {
        "loop_id": loop_id,
        "status": "active",
        "time_remaining": 240,
        "protocols_completed": 2,
        "decisions_made": 5
    }


@router.post("/complete-loop")
async def complete_loop(loop_id: str, player_id: str) -> Dict[str, Any]:
    """Complete current loop and prepare for next"""
    
    if player_id not in player_states:
        raise HTTPException(status_code=404, detail="Player not found")
    
    cognitive_state = player_states[player_id]
    cognitive_state.loop_number += 1
    
    # Check for loop break conditions
    break_check = loop_manager.check_loop_break_conditions(loop_id, cognitive_state)
    
    analytics = loop_manager.get_loop_analytics(player_id)
    
    return {
        "success": True,
        "loop_completed": cognitive_state.loop_number - 1,
        "can_break_loop": break_check["can_break"],
        "break_conditions": break_check,
        "analytics": analytics,
        "ready_for_next": True
    }


@router.get("/cognitive-state/{player_id}")
async def get_cognitive_state(player_id: str) -> Dict[str, Any]:
    """Get player's current cognitive state"""
    
    if player_id not in player_states:
        raise HTTPException(status_code=404, detail="Player not found")
    
    state = player_states[player_id]
    
    return {
        "player_id": player_id,
        "loop_number": state.loop_number,
        "evolution_score": state.evolution_score,
        "modules": {
            name: {
                "level": module.level,
                "status": module.status.value,
                "experience": module.experience_points
            }
            for name, module in state.modules.items()
        },
        "dominant_traits": state.dominant_traits,
        "neural_tree": state.get_neural_tree_data()
    }


@router.websocket("/ws/loop/{player_id}")
async def websocket_loop(websocket: WebSocket, player_id: str):
    """WebSocket connection for real-time loop updates"""
    
    await websocket.accept()
    
    try:
        while True:
            # Receive messages from client
            data = await websocket.receive_text()
            message = json.loads(data)
            
            message_type = message.get("type")
            
            if message_type == "timer_update":
                elapsed = message.get("elapsed", 0)
                loop_id = message.get("loop_id")
                
                status = loop_manager.update_loop_timer(loop_id, elapsed)
                
                await websocket.send_json({
                    "type": "timer_status",
                    "data": status
                })
            
            elif message_type == "get_state":
                if player_id in player_states:
                    state = player_states[player_id]
                    await websocket.send_json({
                        "type": "state_update",
                        "data": state.to_dict()
                    })
            
    except WebSocketDisconnect:
        print(f"WebSocket disconnected for player {player_id}")