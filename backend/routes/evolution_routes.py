"""
Evolution and progression routes
"""

from fastapi import APIRouter, HTTPException
from typing import Dict, List, Any

from backend.services.evolution_engine import EvolutionEngine
from backend.services.ml_service import MLService

router = APIRouter(prefix="/api/evolution", tags=["evolution"])

evolution_engine = EvolutionEngine()
ml_service = MLService()


@router.get("/neural-tree/{player_id}")
async def get_neural_tree(player_id: str) -> Dict[str, Any]:
    """Get neural evolution tree visualization data"""
    
    # TODO: Get from database
    from backend.routes.protocol_routes import player_states
    
    if player_id not in player_states:
        raise HTTPException(status_code=404, detail="Player not found")
    
    state = player_states[player_id]
    tree_data = state.get_neural_tree_data()
    
    return {
        "success": True,
        "tree_data": tree_data,
        "visualization_type": "force_directed_graph"
    }


@router.get("/insights/{player_id}")
async def get_evolution_insights(player_id: str) -> Dict[str, Any]:
    """Get insights about cognitive evolution"""
    
    from backend.routes.protocol_routes import player_states
    
    if player_id not in player_states:
        raise HTTPException(status_code=404, detail="Player not found")
    
    state = player_states[player_id]
    insights = evolution_engine.generate_evolution_insights(state, [])
    
    return {
        "success": True,
        "insights": insights,
        "evolution_score": state.evolution_score,
        "dominant_traits": state.dominant_traits
    }


@router.get("/progression/{player_id}")
async def get_progression_data(player_id: str) -> Dict[str, Any]:
    """Get progression history and trends"""
    
    # TODO: Get historical data from database
    
    return {
        "success": True,
        "progression": {
            "loops_completed": 15,
            "total_experience": 5000,
            "modules_unlocked": 6,
            "modules_mastered": 2,
            "trend": "improving"
        }
    }


@router.post("/predict-path")
async def predict_evolution_path(
    player_id: str,
    hypothetical_choices: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """Predict future evolution path based on hypothetical choices"""
    
    from backend.routes.protocol_routes import player_states
    
    if player_id not in player_states:
        raise HTTPException(status_code=404, detail="Player not found")
    
    # Simulate future state
    current_state = player_states[player_id]
    simulated_state = current_state.model_copy(deep=True)
    
    for choice in hypothetical_choices:
        impact = choice.get("cognitive_impact", {})
        simulated_state = evolution_engine.apply_decision_impact(
            simulated_state,
            impact,
            choice.get("mentor_influence")
        )
    
    return {
        "success": True,
        "predicted_state": simulated_state.to_dict(),
        "predicted_score": simulated_state.evolution_score,
        "predicted_traits": simulated_state.dominant_traits,
        "new_unlocks": [
            name for name, module in simulated_state.modules.items()
            if module.status.value != current_state.modules[name].status.value
        ]
    }


@router.get("/behavior-analysis/{player_id}")
async def analyze_behavior(player_id: str) -> Dict[str, Any]:
    """Analyze player behavior patterns"""
    
    # TODO: Get decision history from database
    decision_history = []
    
    pattern = ml_service.analyze_player_pattern(player_id, decision_history)
    
    return {
        "success": True,
        "pattern": pattern,
        "recommendations": [
            "Try exploring COMPASSION-aligned choices",
            "Consider protocols that challenge your creativity module",
            "Your decision speed is optimal for your pattern type"
        ]
    }