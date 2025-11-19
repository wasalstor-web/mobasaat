"""
DL+ Intelligence System
نظام DL+ الذكي

An advanced AI agent platform with Arabic language support
منصة وكلاء ذكاء اصطناعي متقدمة مع دعم اللغة العربية
"""

__version__ = "1.0.0"

from .core import IntelligenceCore, ArabicProcessor, ContextAnalyzer
from .agents import BaseAgent, WebRetrievalAgent, CodeGeneratorAgent
from .config import settings

__all__ = [
    'IntelligenceCore',
    'ArabicProcessor',
    'ContextAnalyzer',
    'BaseAgent',
    'WebRetrievalAgent',
    'CodeGeneratorAgent',
    'settings'
]
