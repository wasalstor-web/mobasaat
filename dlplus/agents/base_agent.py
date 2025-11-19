"""
Base Agent Class
الفئة الأساسية للوكلاء
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from datetime import datetime


class BaseAgent(ABC):
    """
    Abstract base class for all AI agents
    الفئة الأساسية المجردة لجميع الوكلاء الأذكياء
    """
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.capabilities = []
        self.execution_history = []
    
    @abstractmethod
    async def execute(self, task: str, context: Optional[Dict] = None) -> Dict:
        """
        Execute the agent's main task
        Must be implemented by subclasses
        """
        pass
    
    def add_capability(self, capability: str):
        """Add a capability to the agent"""
        if capability not in self.capabilities:
            self.capabilities.append(capability)
    
    def _log_execution(self, task: str, result: Any, success: bool = True):
        """Log execution for tracking"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "task": task,
            "success": success,
            "result_preview": str(result)[:100] if result else None
        }
        self.execution_history.append(log_entry)
        
        # Keep only recent history
        if len(self.execution_history) > 50:
            self.execution_history = self.execution_history[-50:]
    
    def get_info(self) -> Dict:
        """Get agent information"""
        return {
            "name": self.name,
            "description": self.description,
            "capabilities": self.capabilities,
            "executions_count": len(self.execution_history),
            "recent_executions": self.execution_history[-5:]
        }
    
    def can_handle(self, task_type: str) -> bool:
        """Check if agent can handle a specific task type"""
        return task_type in self.capabilities
