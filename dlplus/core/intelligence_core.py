"""
DL+ Intelligence Core
نواة الذكاء DL+
"""

import asyncio
from typing import Dict, List, Optional, Any
from datetime import datetime

from ..config.settings import settings
from ..config.models_config import get_model_config, get_models_by_capability
from .arabic_processor import ArabicProcessor, IntentType
from .context_analyzer import ContextAnalyzer


class IntelligenceCore:
    """
    Main intelligence system that coordinates all AI agents and tools
    النظام الذكي الرئيسي الذي ينسق جميع الوكلاء والأدوات
    """
    
    def __init__(self):
        self.arabic_processor = ArabicProcessor()
        self.context_analyzer = ContextAnalyzer()
        self.tools_registry = {}
        self.agents_registry = {}
        
        # Initialize logging
        self.execution_logs = []
    
    def register_tool(self, name: str, tool_func: callable, description: str):
        """Register a tool function"""
        self.tools_registry[name] = {
            "function": tool_func,
            "description": description
        }
        self._log(f"Tool registered: {name}")
    
    def register_agent(self, name: str, agent_instance: Any):
        """Register an AI agent"""
        self.agents_registry[name] = agent_instance
        self._log(f"Agent registered: {name}")
    
    async def process_request(
        self,
        user_input: str,
        context: Optional[Dict] = None
    ) -> Dict:
        """
        Main entry point for processing user requests
        نقطة الدخول الرئيسية لمعالجة طلبات المستخدم
        """
        start_time = datetime.now()
        self._log(f"Processing request: {user_input[:50]}...")
        
        # Step 1: Detect language and intent
        is_arabic = self.arabic_processor.is_arabic(user_input)
        intent = self.arabic_processor.detect_intent(user_input)
        entities = self.arabic_processor.extract_entities(user_input)
        
        self._log(f"Detected - Language: {'Arabic' if is_arabic else 'English'}, Intent: {intent.value}")
        
        # Step 2: Get context
        context_summary = self.context_analyzer.get_context_summary()
        context_switch = self.context_analyzer.detect_context_switch(intent.value)
        
        if context_switch:
            self._log("Context switch detected")
        
        # Step 3: Select appropriate model and tools
        model_name = self._select_model(intent, is_arabic)
        tools_to_use = self._select_tools(intent, entities)
        
        self._log(f"Selected model: {model_name}, Tools: {tools_to_use}")
        
        # Step 4: Plan execution steps
        execution_plan = self._create_execution_plan(
            intent, entities, tools_to_use, context_summary
        )
        
        # Step 5: Execute plan
        result = await self._execute_plan(
            execution_plan,
            user_input,
            model_name,
            is_arabic
        )
        
        # Step 6: Update context
        self.context_analyzer.add_turn(
            user_message=user_input,
            agent_response=result.get("response", ""),
            intent=intent.value,
            entities=entities,
            tools_used=tools_to_use
        )
        
        # Calculate execution time
        execution_time = (datetime.now() - start_time).total_seconds()
        
        return {
            "success": True,
            "response": result.get("response", ""),
            "intent": intent.value,
            "entities": entities,
            "tools_used": tools_to_use,
            "model_used": model_name,
            "execution_time": execution_time,
            "logs": self.execution_logs[-10:],  # Last 10 logs
            "context": context_summary
        }
    
    def _select_model(self, intent: IntentType, is_arabic: bool) -> str:
        """Select the best model based on intent and language"""
        # For code generation, use code-specialized models
        if intent == IntentType.GENERATE_CODE:
            return "deepseek-coder"
        
        # For Arabic tasks, prefer Arabic models
        if is_arabic:
            return settings.default_arabic_model or "qwen-arabic"
        
        # Default model
        return settings.default_model
    
    def _select_tools(self, intent: IntentType, entities: Dict) -> List[str]:
        """Select tools needed based on intent and entities"""
        tools = []
        
        if intent == IntentType.GREETING:
            # Greetings don't need any special tools
            pass
        
        elif intent == IntentType.SEARCH:
            tools.append("run_web_search")
        
        elif intent == IntentType.GENERATE_CODE:
            tools.append("code_generator")
            if entities.get("files"):
                tools.append("write_to_file")
        
        elif intent == IntentType.EXECUTE_COMMAND:
            tools.append("run_shell")
        
        elif intent == IntentType.CREATE_FILE:
            tools.append("write_to_file")
        
        elif intent == IntentType.READ_FILE:
            tools.append("read_from_file")
        
        elif intent == IntentType.ANALYZE:
            if entities.get("files"):
                tools.append("read_from_file")
            if entities.get("urls"):
                tools.append("run_web_search")
        
        return tools
    
    def _create_execution_plan(
        self,
        intent: IntentType,
        entities: Dict,
        tools: List[str],
        context: Dict
    ) -> Dict:
        """Create a step-by-step execution plan"""
        plan = {
            "intent": intent.value,
            "steps": [],
            "expected_output": ""
        }
        
        # Build steps based on intent
        if intent == IntentType.GREETING:
            plan["steps"] = [
                {"action": "generate_greeting", "tool": "arabic_processor"}
            ]
            plan["expected_output"] = "Friendly greeting response"
        
        elif intent == IntentType.SEARCH:
            plan["steps"] = [
                {"action": "web_search", "tool": "run_web_search"},
                {"action": "analyze_results", "tool": "intelligence_core"},
                {"action": "format_response", "tool": "arabic_processor"}
            ]
            plan["expected_output"] = "Search results with analysis"
        
        elif intent == IntentType.GENERATE_CODE:
            plan["steps"] = [
                {"action": "understand_requirements", "tool": "intelligence_core"},
                {"action": "generate_code", "tool": "code_generator"},
                {"action": "save_to_file", "tool": "write_to_file"}
            ]
            plan["expected_output"] = "Generated code file"
        
        elif intent == IntentType.EXECUTE_COMMAND:
            plan["steps"] = [
                {"action": "validate_command", "tool": "intelligence_core"},
                {"action": "execute", "tool": "run_shell"},
                {"action": "format_results", "tool": "intelligence_core"}
            ]
            plan["expected_output"] = "Command execution results"
        
        return plan
    
    async def _execute_plan(
        self,
        plan: Dict,
        user_input: str,
        model_name: str,
        is_arabic: bool
    ) -> Dict:
        """Execute the planned steps"""
        results = {
            "response": "",
            "steps_completed": [],
            "outputs": {}
        }
        
        # For now, generate a simple response
        # In full implementation, this would execute each step
        intent = plan["intent"]
        
        if is_arabic:
            response = self.arabic_processor.generate_response(
                IntentType(intent),
                {}
            )
        else:
            # English responses
            if intent == IntentType.GREETING.value:
                response = "Hello! I'm an intelligent AI agent ready to assist you. How can I help you today?"
            else:
                response = f"Processing your request with intent: {intent}"
        
        results["response"] = response
        results["steps_completed"] = [step["action"] for step in plan["steps"]]
        
        return results
    
    def _log(self, message: str):
        """Add log entry"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "message": message
        }
        self.execution_logs.append(log_entry)
        
        # Keep only recent logs
        if len(self.execution_logs) > 100:
            self.execution_logs = self.execution_logs[-100:]
    
    def get_status(self) -> Dict:
        """Get system status"""
        return {
            "tools_registered": len(self.tools_registry),
            "agents_registered": len(self.agents_registry),
            "conversation_turns": len(self.context_analyzer.conversation_history),
            "context_memory_keys": list(self.context_analyzer.context_memory.keys()),
            "recent_logs": self.execution_logs[-5:]
        }
