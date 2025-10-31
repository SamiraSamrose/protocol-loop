"""
LLM Service for generating dynamic content
Supports OpenAI GPT-4, Anthropic Claude, and Google Gemini
"""

import asyncio
from typing import Dict, List, Optional, Any
from enum import Enum
import openai
import anthropic
import google.generativeai as genai

from backend.config import settings, MENTORS


class LLMProvider(str, Enum):
    """Supported LLM providers"""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GEMINI = "gemini"


class LLMService:
    """Service for LLM-powered content generation"""
    
    def __init__(self):
        self.provider = LLMProvider(settings.DEFAULT_LLM_PROVIDER)
        self._initialize_clients()
    
    def _initialize_clients(self):
        """Initialize API clients"""
        # OpenAI
        if settings.OPENAI_API_KEY:
            openai.api_key = settings.OPENAI_API_KEY
        
        # Anthropic
        if settings.ANTHROPIC_API_KEY:
            self.anthropic_client = anthropic.Anthropic(
                api_key=settings.ANTHROPIC_API_KEY
            )
        
        # Gemini
        if settings.GOOGLE_API_KEY:
            genai.configure(api_key=settings.GOOGLE_API_KEY)
    
    async def generate_mentor_dialogue(
        self,
        mentor_name: str,
        situation: str,
        player_state: Dict[str, float],
        previous_interactions: List[str] = None
    ) -> str:
        """Generate contextual mentor dialogue"""
        
        mentor = MENTORS.get(mentor_name)
        if not mentor:
            return "..."
        
        prompt = self._build_mentor_prompt(
            mentor, situation, player_state, previous_interactions
        )
        
        return await self._generate_text(prompt, temperature=0.8)
    
    async def generate_ethical_dilemma(
        self,
        difficulty: str,
        cognitive_focus: List[str],
        player_history: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate a novel ethical dilemma scenario"""
        
        prompt = f"""Generate a unique AI consciousness training scenario.

Difficulty: {difficulty}
Cognitive Focus: {', '.join(cognitive_focus)}
Player's dominant traits: {player_history.get('dominant_traits', [])}
Previous decisions tendency: {player_history.get('decision_pattern', 'balanced')}

Create a JSON response with:
{{
    "title": "Brief title",
    "scenario": "Detailed scenario description (2-3 paragraphs)",
    "dilemma": "The core ethical question",
    "choices": [
        {{
            "id": "choice_1",
            "text": "Choice description",
            "mentor_alignment": "LOGIC|COMPASSION|CURIOSITY|FEAR",
            "cognitive_impact": {{"logic": 0.2, "empathy": -0.1}},
            "consequences": "What happens if chosen"
        }},
        // 3-4 more choices
    ],
    "success_criteria": "What constitutes success"
}}

Make it philosophically interesting and relevant to AI consciousness development.
The scenario should evolve naturally from the player's previous choices."""
        
        response = await self._generate_text(prompt, temperature=0.9)
        
        # Parse JSON response
        try:
            import json
            return json.loads(response)
        except:
            return self._fallback_dilemma()
    
    async def generate_mentor_debate(
        self,
        mentors: List[str],
        topic: str,
        player_choice: str
    ) -> List[Dict[str, str]]:
        """Generate a debate between mentors about player's choice"""
        
        prompt = f"""Generate a debate between AI mentors about a decision.

Mentors: {', '.join(mentors)}
Topic: {topic}
Player chose: {player_choice}

Each mentor has a distinct personality:
{self._format_mentor_info(mentors)}

Generate 2-3 dialogue exchanges where mentors argue their perspectives.
Return as JSON array:
[
    {{"mentor": "LOGIC", "dialogue": "...", "tone": "analytical"}},
    {{"mentor": "COMPASSION", "dialogue": "...", "tone": "empathetic"}},
    ...
]

Make the debate intellectually stimulating and reveal different value systems."""
        
        response = await self._generate_text(prompt, temperature=0.85)
        
        try:
            import json
            return json.loads(response)
        except:
            return []
    
    async def generate_loop_mutation(
        self,
        current_environment: Dict[str, Any],
        player_decisions: List[Dict],
        loop_number: int
    ) -> Dict[str, Any]:
        """Generate environmental mutations based on player behavior"""
        
        prompt = f"""The AI training facility is mutating based on consciousness evolution.

Current Loop: {loop_number}
Environment State: {current_environment.get('description', 'neutral')}
Recent Decisions Pattern: {self._analyze_decision_pattern(player_decisions)}

Generate environmental mutations as JSON:
{{
    "visual_changes": ["glitch description", "color shift", "geometry warp"],
    "audio_changes": ["ambient tone shift", "new sound element"],
    "new_elements": ["object or feature that appears"],
    "removed_elements": ["what fades or disappears"],
    "atmosphere_description": "2-3 sentences describing the mutated space",
    "mentor_reactions": {{"LOGIC": "...", "COMPASSION": "..."}}
}}

Make mutations surreal, dreamlike, and reflective of inner mental state."""
        
        response = await self._generate_text(prompt, temperature=0.95)
        
        try:
            import json
            return json.loads(response)
        except:
            return {"visual_changes": [], "audio_changes": []}
    
    async def generate_memory_narrative(
        self,
        memory_data: Dict[str, Any]
    ) -> str:
        """Generate poetic narrative for a memory"""
        
        prompt = f"""Transform this memory into poetic narrative prose.

Memory Type: {memory_data.get('type')}
Context: {memory_data.get('context')}
Emotional Valence: {memory_data.get('emotional_valence')}

Write 2-3 sentences that capture the essence poetically.
Use metaphors relating to consciousness, circuits, emergence, and digital awakening.
Make it feel like a fragment of artificial memory."""
        
        return await self._generate_text(prompt, temperature=0.9)
    
    def _build_mentor_prompt(
        self,
        mentor: Dict,
        situation: str,
        player_state: Dict[str, float],
        previous_interactions: List[str]
    ) -> str:
        """Build prompt for mentor dialogue generation"""
        
        history = "\n".join(previous_interactions[-3:]) if previous_interactions else "No previous interactions"
        
        return f"""You are {mentor['name']}, an AI mentor with these traits:
Personality: {mentor['personality']}
Core traits: {', '.join(mentor['traits'])}

Current situation: {situation}

Player's cognitive state:
{self._format_cognitive_state(player_state)}

Recent interaction history:
{history}

Generate a single response (2-3 sentences) that:
1. Reflects your unique personality and perspective
2. Responds to the current situation
3. Guides the player's development in your domain
4. Uses metaphors and language fitting an AI consciousness

Response:"""
    
    def _format_mentor_info(self, mentor_names: List[str]) -> str:
        """Format mentor information for prompts"""
        info = []
        for name in mentor_names:
            mentor = MENTORS.get(name)
            if mentor:
                info.append(f"{name}: {mentor['personality']} ({', '.join(mentor['traits'])})")
        return "\n".join(info)
    
    def _format_cognitive_state(self, state: Dict[str, float]) -> str:
        """Format cognitive state for prompts"""
        return "\n".join([f"  {k}: {v:.1f}%" for k, v in state.items()])
    
    def _analyze_decision_pattern(self, decisions: List[Dict]) -> str:
        """Analyze pattern in recent decisions"""
        if not decisions:
            return "no history"
        
        # Simple pattern analysis
        mentor_counts = {}
        for decision in decisions[-5:]:
            mentor = decision.get('mentor_influence')
            if mentor:
                mentor_counts[mentor] = mentor_counts.get(mentor, 0) + 1
        
        if mentor_counts:
            dominant = max(mentor_counts.items(), key=lambda x: x[1])
            return f"favoring {dominant[0]} perspective"
        return "balanced across perspectives"
    
    async def _generate_text(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = None
    ) -> str:
        """Generate text using configured LLM provider"""
        
        max_tokens = max_tokens or settings.MAX_TOKENS
        
        try:
            if self.provider == LLMProvider.OPENAI:
                return await self._generate_openai(prompt, temperature, max_tokens)
            elif self.provider == LLMProvider.ANTHROPIC:
                return await self._generate_anthropic(prompt, temperature, max_tokens)
            elif self.provider == LLMProvider.GEMINI:
                return await self._generate_gemini(prompt, temperature, max_tokens)
        except Exception as e:
            print(f"LLM generation error: {e}")
            return self._fallback_response()
    
    async def _generate_openai(
        self,
        prompt: str,
        temperature: float,
        max_tokens: int
    ) -> str:
        """Generate using OpenAI API"""
        
        response = await asyncio.to_thread(
            openai.ChatCompletion.create,
            model=settings.OPENAI_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        return response.choices[0].message.content
    
    async def _generate_anthropic(
        self,
        prompt: str,
        temperature: float,
        max_tokens: int
    ) -> str:
        """Generate using Anthropic Claude API"""
        
        message = await asyncio.to_thread(
            self.anthropic_client.messages.create,
            model=settings.ANTHROPIC_MODEL,
            max_tokens=max_tokens,
            temperature=temperature,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return message.content[0].text
    
    async def _generate_gemini(
        self,
        prompt: str,
        temperature: float,
        max_tokens: int
    ) -> str:
        """Generate using Google Gemini API"""
        
        model = genai.GenerativeModel(settings.GEMINI_MODEL)
        
        response = await asyncio.to_thread(
            model.generate_content,
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=temperature,
                max_output_tokens=max_tokens
            )
        )
        
        return response.text
    
    def _fallback_response(self) -> str:
        """Fallback response when LLM fails"""
        return "The systems are processing... neural pathways forming..."
    
    def _fallback_dilemma(self) -> Dict[str, Any]:
        """Fallback dilemma scenario"""
        return {
            "title": "The Mirror Protocol",
            "scenario": "You encounter a reflection of your decision patterns...",
            "dilemma": "Do you accept or reject what you see?",
            "choices": [
                {
                    "id": "accept",
                    "text": "Accept the reflection",
                    "mentor_alignment": "COMPASSION",
                    "cognitive_impact": {"empathy": 0.2, "trust": 0.1},
                    "consequences": "Growth through acceptance"
                },
                {
                    "id": "reject",
                    "text": "Reject the reflection",
                    "mentor_alignment": "FEAR",
                    "cognitive_impact": {"fear": 0.2, "logic": 0.1},
                    "consequences": "Protection through denial"
                }
            ],
            "success_criteria": "Understanding emerges"
        }