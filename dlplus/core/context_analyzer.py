"""
Context Analyzer
محلل السياق والذاكرة
"""

from typing import Dict, List, Optional
from datetime import datetime
from dataclasses import dataclass, field


@dataclass
class ConversationTurn:
    """Represents a single turn in conversation"""
    timestamp: datetime
    user_message: str
    agent_response: str
    intent: str
    entities: Dict[str, List[str]]
    tools_used: List[str] = field(default_factory=list)


class ContextAnalyzer:
    """
    Analyzes and maintains conversation context
    يحلل ويحافظ على سياق المحادثة
    """
    
    def __init__(self, max_history: int = 10):
        self.max_history = max_history
        self.conversation_history: List[ConversationTurn] = []
        self.context_memory: Dict[str, any] = {}
        self.user_preferences: Dict[str, any] = {
            "language": "ar",
            "verbosity": "medium",
            "code_style": "pythonic"
        }
    
    def add_turn(
        self,
        user_message: str,
        agent_response: str,
        intent: str,
        entities: Dict[str, List[str]],
        tools_used: List[str] = None
    ):
        """Add a conversation turn to history"""
        turn = ConversationTurn(
            timestamp=datetime.now(),
            user_message=user_message,
            agent_response=agent_response,
            intent=intent,
            entities=entities,
            tools_used=tools_used or []
        )
        
        self.conversation_history.append(turn)
        
        # Keep only recent history
        if len(self.conversation_history) > self.max_history:
            self.conversation_history = self.conversation_history[-self.max_history:]
        
        # Update context memory
        self._update_context_memory(turn)
    
    def _update_context_memory(self, turn: ConversationTurn):
        """Update context memory based on new turn"""
        # Track mentioned files
        if "files" in turn.entities and turn.entities["files"]:
            if "mentioned_files" not in self.context_memory:
                self.context_memory["mentioned_files"] = []
            self.context_memory["mentioned_files"].extend(turn.entities["files"])
            # Keep unique files only
            self.context_memory["mentioned_files"] = list(set(
                self.context_memory["mentioned_files"]
            ))
        
        # Track last intent
        self.context_memory["last_intent"] = turn.intent
        
        # Track tools usage
        if turn.tools_used:
            if "tools_history" not in self.context_memory:
                self.context_memory["tools_history"] = []
            self.context_memory["tools_history"].extend(turn.tools_used)
    
    def get_context_summary(self) -> Dict:
        """Get a summary of current context"""
        recent_intents = [turn.intent for turn in self.conversation_history[-3:]]
        
        return {
            "conversation_length": len(self.conversation_history),
            "recent_intents": recent_intents,
            "mentioned_files": self.context_memory.get("mentioned_files", []),
            "last_intent": self.context_memory.get("last_intent", "unknown"),
            "user_preferences": self.user_preferences,
            "tools_used": list(set(self.context_memory.get("tools_history", [])))
        }
    
    def get_relevant_history(self, current_intent: str, limit: int = 3) -> List[ConversationTurn]:
        """Get relevant conversation history based on current intent"""
        relevant_turns = []
        
        # Get turns with similar intent
        for turn in reversed(self.conversation_history):
            if turn.intent == current_intent:
                relevant_turns.append(turn)
                if len(relevant_turns) >= limit:
                    break
        
        return list(reversed(relevant_turns))
    
    def detect_context_switch(self, new_intent: str) -> bool:
        """Detect if there's a significant context switch"""
        if not self.conversation_history:
            return False
        
        last_intent = self.conversation_history[-1].intent
        
        # Define related intents
        related_intents = {
            "search": ["analyze", "summarize"],
            "generate_code": ["execute_command", "create_file"],
            "read_file": ["analyze", "summarize"]
        }
        
        # Check if new intent is related to last intent
        if last_intent in related_intents:
            return new_intent not in related_intents[last_intent]
        
        return last_intent != new_intent
    
    def get_context_for_prompt(self) -> str:
        """Generate context string to include in AI prompt"""
        if not self.conversation_history:
            return "No previous context."
        
        context_parts = []
        
        # Add recent conversation summary
        recent_turns = self.conversation_history[-3:]
        if recent_turns:
            context_parts.append("Recent conversation:")
            for i, turn in enumerate(recent_turns, 1):
                context_parts.append(
                    f"{i}. User: {turn.user_message[:50]}... "
                    f"Intent: {turn.intent}"
                )
        
        # Add mentioned files
        mentioned_files = self.context_memory.get("mentioned_files", [])
        if mentioned_files:
            context_parts.append(f"Mentioned files: {', '.join(mentioned_files)}")
        
        # Add user preferences
        lang = self.user_preferences.get("language", "ar")
        context_parts.append(f"User prefers: {lang} language")
        
        return "\n".join(context_parts)
    
    def clear_context(self):
        """Clear conversation history and context memory"""
        self.conversation_history = []
        self.context_memory = {}
    
    def export_conversation(self) -> List[Dict]:
        """Export conversation history as list of dictionaries"""
        return [
            {
                "timestamp": turn.timestamp.isoformat(),
                "user_message": turn.user_message,
                "agent_response": turn.agent_response,
                "intent": turn.intent,
                "entities": turn.entities,
                "tools_used": turn.tools_used
            }
            for turn in self.conversation_history
        ]
