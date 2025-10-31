# PROTOCOL:LOOP - Complete Documentation

## Table of Contents
1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Core Systems](#core-systems)
4. [API Reference](#api-reference)
5. [Frontend Components](#frontend-components)
6. [AI/ML Integration](#aiml-integration)
7. [Data Models](#data-models)
8. [Advanced Features](#advanced-features)

## Overview

PROTOCOL:LOOP is a recursive AI consciousness simulator that gamifies concepts of AI alignment, emotional intelligence, and digital identity through time-loop mechanics.

### Key Concepts

- **Recursive Loops**: Each 2-5 minute cycle represents a consciousness training iteration
- **Cognitive Evolution**: Player decisions shape 8 cognitive modules (logic, empathy, creativity, fear, trust, humor, curiosity, ethics)
- **AI Mentors**: Four dynamic NPCs (LOGIC, COMPASSION, CURIOSITY, FEAR) that evolve with your choices
- **LLM-Powered Content**: GPT-4/Claude generates unique moral dilemmas and narrative
- **Social Features**: Share consciousness trees, view ghost protocols, collaborate on challenges

## Architecture

### System Components
```
┌─────────────────────────────────────────────────────────┐
│                    Frontend Layer                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │  HTML/CSS/JS │  │ Visualizations│  │  Neural Map  │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────┘
                           │
┌─────────────────────────────────────────────────────────┐
│                      API Layer                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │   Protocol   │  │  Evolution   │  │    Social    │ │
│  │    Routes    │  │    Routes    │  │    Routes    │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────┘
                           │
┌─────────────────────────────────────────────────────────┐
│                   Service Layer                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │ Loop Manager │  │   Evolution  │  │   LLM/ML     │ │
│  │              │  │    Engine    │  │   Services   │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────┘
                           │
┌─────────────────────────────────────────────────────────┐
│                    Data Layer                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │  Cognitive   │  │   Memories   │  │   Protocols  │ │
│  │    State     │  │              │  │              │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────┘
```

## Core Systems

### 1. Loop System

The loop system manages the recursive time-loop mechanics.

**Key Features:**
- Configurable loop duration (default 5 minutes)
- Memory persistence across loops
- Item retention system
- Environment mutation based on decisions
- Loop break conditions for "transcendence"

**Usage Example:**
```python
from backend.services.loop_manager import LoopManager

manager = LoopManager()
loop = manager.start_loop(player_id, cognitive_state, memory_bank)
```

### 2. Evolution Engine

Manages cognitive module progression and consciousness evolution.

**Cognitive Modules:**
- **Logic**: Analytical reasoning (🧮)
- **Empathy**: Emotional understanding (❤️)
- **Creativity**: Novel thinking (🎨)
- **Fear**: Risk assessment (⚠️)
- **Trust**: Relationship building (🤝)
- **Humor**: Playful cognition (😄)
- **Curiosity**: Knowledge seeking (🔍)
- **Ethics**: Moral reasoning (⚖️)

**Module States:**
- Locked → Nascent → Developing → Active → Mastered

### 3. LLM Service

Generates dynamic content using multiple LLM providers.

**Supported Providers:**
- OpenAI GPT-4
- Anthropic Claude
- Google Gemini

**Generation Capabilities:**
- Ethical dilemmas
- Mentor dialogue
- Environment mutations
- Memory narratives
- Mentor debates

### 4. ML Service

Behavioral prediction and pattern analysis.

**Features:**
- Decision tree classification
- Markov chain state prediction
- Player pattern analysis
- Adaptive difficulty
- Similarity matching

## API Reference

### Protocol Routes

#### POST /api/protocols/start-loop
Start a new loop iteration.

**Parameters:**
- `player_id` (string): Player identifier

**Response:**
```json
{
  "success": true,
  "loop_id": "player_loop_1",
  "loop_number": 1,
  "duration": 300,
  "environment": {...}
}
```

#### POST /api/protocols/generate-protocol
Generate a new protocol scenario.

**Parameters:**
- `player_id` (string): Player identifier
- `protocol_type` (string, optional): Type of protocol

**Response:**
```json
{
  "success": true,
  "protocol": {
    "title": "The Mirror Protocol",
    "scenario": "...",
    "dilemma": "...",
    "choices": [...]
  },
  "difficulty": "proficient"
}
```

#### POST /api/protocols/make-decision
Record a decision and apply effects.

**Body:**
```json
{
  "session_id": "session_123",
  "choice_id": "choice_1",
  "confidence": 0.85,
  "player_id": "player_123"
}
```

### Evolution Routes

#### GET /api/evolution/neural-tree/{player_id}
Get neural evolution tree data.

**Response:**
```json
{
  "success": true,
  "tree_data": {
    "nodes": [...],
    "links": [...],
    "evolution_score": 45.2
  }
}
```

#### GET /api/evolution/insights/{player_id}
Get evolution insights.

**Response:**
```json
{
  "success": true,
  "insights": [
    "Your consciousness strongly expresses LOGIC...",
    "You're developing 5 cognitive modules simultaneously..."
  ]
}
```

### Social Routes

#### GET /api/social/ghost-protocols/{player_id}
Get similar players (ghost protocols).

**Parameters:**
- `limit` (int): Maximum number of results

**Response:**
```json
{
  "success": true,
  "ghosts": [
    {
      "player_id": "other_player",
      "similarity": 0.85,
      "pattern": "decisive"
    }
  ]
}
```

## Frontend Components

### Main Application (main.js)

Central class managing all frontend interactions:
```javascript
class ProtocolLoop {
  constructor()
  init()
  startLoop()
  generateProtocol()
  makeDecision()
  completeLoop()
}
```

### Visualizations (visualizations.js)

Provides chart and graph rendering:
```javascript
class Visualizations {
  createEvolutionChart()
  createRadarChart()
  animateProgressBar()
  createParticleSystem()
}
```

### Neural Map (neural_map.js)

Interactive force-directed graph visualization:
```javascript
class NeuralMap {
  loadData(treeData)
  update()  // Physics simulation
  draw()    // Canvas rendering
}
```

## AI/ML Integration

### LLM Integration

Configure in `.env`:
```bash
OPENAI_API_KEY=your-key
ANTHROPIC_API_KEY=your-key
GOOGLE_API_KEY=your-key
DEFAULT_LLM_PROVIDER=openai
```

### Prompt Engineering

Prompts are structured for consistent output:
```python
prompt = f"""Generate a unique AI consciousness training scenario.

Difficulty: {difficulty}
Cognitive Focus: {', '.join(cognitive_focus)}

Create a JSON response with:
{{
    "title": "Brief title",
    "scenario": "Detailed description",
    ...
}}
"""
```

### Behavioral Learning

The system learns from player decisions:

1. **Decision Trees**: Classify decision patterns
2. **Markov Chains**: Predict state transitions
3. **Pattern Analysis**: Identify play styles
4. **Adaptive Difficulty**: Adjust challenge level

## Data Models

### CognitiveState
```python
class CognitiveState:
    player_id: str
    loop_number: int
    modules: Dict[str, CognitiveModule]
    evolution_score: float
    dominant_traits: List[str]
```

### Memory
```python
class Memory:
    id: str
    type: MemoryType
    importance: MemoryImportance
    content: str
    cognitive_impact: Dict[str, float]
    access_count: int
```

### Protocol
```python
class Protocol:
    id: str
    type: ProtocolType
    difficulty: ProtocolDifficulty
    scenario: str
    choices: List[Dict]
    mentor_dialogue: Dict[str, str]
```

## Advanced Features

### 1. Environment Mutation

Environments evolve based on cognitive state:
```python
mutations = {
    "visual_style": determine_visual_style(state),
    "audio_profile": determine_audio_profile(state),
    "facility_layout": mutate_layout(state, loop_number),
    "anomalies": []
}
```

### 2. Memory Decay

Memories decay over time unless accessed:
```python
decay_factor = max(0.1, 1.0 - (days_since_access * 0.05 / (1 + access_count * 0.1)))
```

### 3. Neural Tree Visualization

Force-directed graph with physics simulation:
- Node repulsion
- Link attraction
- Center gravity
- Bounded canvas

### 4. Social Features

- **Ghost Protocols**: View decision paths of similar players
- **Consciousness Comparison**: Compare evolution trees
- **Memory Sharing**: Exchange memories between players
- **Mind Forking**: Copy specific modules from other players

## Performance Optimization

### Backend

- Async/await for LLM calls
- WebSocket for real-time updates
- In-memory caching for active sessions
- Batch processing for ML operations

### Frontend

- Canvas-based rendering for visualizations
- RequestAnimationFrame for smooth animations
- Event delegation for dynamic elements
- Lazy loading for heavy components

## Security Considerations

- API key management via environment variables
- Input validation on all routes
- Rate limiting for LLM requests (100/hour)
- Sanitization of user-generated content
- CORS configuration for allowed origins

## Deployment

### Development
```bash
python backend/app.py
```

### Production
```bash
gunicorn backend.app:app --workers 4 --bind 0.0.0.0:8000
```

### Docker
```dockerfile
FROM python:3.9
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Troubleshooting

### Common Issues

1. **LLM API Errors**: Check API keys and rate limits
2. **WebSocket Disconnects**: Verify network stability
3. **Slow Protocol Generation**: LLM calls take 5-10 seconds
4. **Canvas Not Rendering**: Check browser compatibility

### Debug Mode

Enable in `.env`:
```bash
DEBUG=True
LOG_LEVEL=DEBUG
```