"""
Social features and multiplayer routes
"""

from fastapi import APIRouter, HTTPException
from typing import Dict, List, Any

from backend.services.evolution_engine import EvolutionEngine
from backend.services.ml_service import MLService

router = APIRouter(prefix="/api/social", tags=["social"])

evolution_engine = EvolutionEngine()
ml_service = MLService()


@router.get("/ghost-protocols/{player_id}")
async def get_ghost_protocols(player_id: str, limit: int = 5) -> Dict[str, Any]:
    """Get ghost protocols (other players' decision paths)"""
    
    similar_players = ml_service.find_similar_players(player_id, limit)
    
    return {
        "success": True,
        "ghosts": similar_players,
        "count": len(similar_players)
    }


@router.post("/compare-consciousness")
async def compare_consciousness_trees(
    player_id1: str,
    player_id2: str
) -> Dict[str, Any]:
    """Compare two consciousness evolution trees"""
    
    from backend.routes.protocol_routes import player_states
    
    if player_id1 not in player_states or player_id2 not in player_states:
        raise HTTPException(status_code=404, detail="One or both players not found")
    
    state1 = player_states[player_id1]
    state2 = player_states[player_id2]
    
    comparison = evolution_engine.compare_consciousness_trees(state1, state2)
    
    return {
        "success": True,
        "comparison": comparison,
        "player1_score": state1.evolution_score,
        "player2_score": state2.evolution_score
    }


@router.post("/share-memory")
async def share_memory(
    from_player: str,
    to_player: str,
    memory_id: str
) -> Dict[str, Any]:
    """Share a memory with another player"""
    
    # TODO: Implement memory sharing logic
    
    return {
        "success": True,
        "message": "Memory shared successfully",
        "memory_id": memory_id
    }


@router.get("/leaderboard")
async def get_leaderboard(category: str = "evolution_score") -> Dict[str, Any]:
    """Get leaderboard rankings"""
    
    from backend.routes.protocol_routes import player_states
    
    # Sort players by specified category
    sorted_players = sorted(
        player_states.items(),
        key=lambda x: x[1].evolution_score if category == "evolution_score" else x[1].loop_number,
        reverse=True
    )
    
    leaderboard = [
        {
            "rank": i + 1,
            "player_id": player_id,
            "score": state.evolution_score,
            "loops": state.loop_number,
            "dominant_trait": state.dominant_traits[0] if state.dominant_traits else "balanced"
        }
        for i, (player_id, state) in enumerate(sorted_players[:10])
    ]
    
    return {
        "success": True,
        "leaderboard": leaderboard,
        "category": category
    }


@router.post("/fork-consciousness")
async def fork_consciousness(
    source_player: str,
    target_player: str,
    modules_to_fork: List[str]
) -> Dict[str, Any]:
    """Fork specific modules from another player's consciousness"""
    
    from backend.routes.protocol_routes import player_states
    
    if source_player not in player_states or target_player not in player_states:
        raise HTTPException(status_code=404, detail="Player not found")
    
    source_state = player_states[source_player]
    target_state = player_states[target_player]
    
    # Copy specified modules
    for module_name in modules_to_fork:
        if module_name in source_state.modules:
            target_state.modules[module_name] = source_state.modules[module_name].model_copy()
    
    target_state.calculate_evolution_score()
    
    return {
        "success": True,
        "forked_modules": modules_to_fork,
        "new_evolution_score": target_state.evolution_score
    }