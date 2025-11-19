"""
Tests for DL+ Intelligence System
اختبارات نظام DL+ الذكي
"""

import pytest
import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dlplus.core import IntelligenceCore, ArabicProcessor, IntentType
from dlplus.agents import WebRetrievalAgent, CodeGeneratorAgent


class TestArabicProcessor:
    """Test Arabic language processor"""
    
    def setup_method(self):
        self.processor = ArabicProcessor()
    
    def test_is_arabic(self):
        """Test Arabic detection"""
        assert self.processor.is_arabic("مرحبا") == True
        assert self.processor.is_arabic("Hello") == False
        assert self.processor.is_arabic("مرحبا Hello") == True
    
    def test_remove_diacritics(self):
        """Test diacritics removal"""
        text_with_diacritics = "مَرْحَبًا"
        text_without = self.processor.remove_diacritics(text_with_diacritics)
        assert "َ" not in text_without
        assert "ْ" not in text_without
    
    def test_detect_intent_arabic(self):
        """Test intent detection for Arabic"""
        assert self.processor.detect_intent("ابحث عن معلومات") == IntentType.SEARCH
        assert self.processor.detect_intent("اكتب كود بايثون") == IntentType.GENERATE_CODE
        assert self.processor.detect_intent("نفذ الأمر") == IntentType.EXECUTE_COMMAND
    
    def test_detect_intent_english(self):
        """Test intent detection for English"""
        assert self.processor.detect_intent("search for info") == IntentType.SEARCH
        assert self.processor.detect_intent("generate code") == IntentType.GENERATE_CODE
        assert self.processor.detect_intent("run command") == IntentType.EXECUTE_COMMAND
    
    def test_extract_entities(self):
        """Test entity extraction"""
        text = "Read file test.py and search https://example.com"
        entities = self.processor.extract_entities(text)
        
        assert "files" in entities
        assert "urls" in entities
        assert len(entities["urls"]) > 0


class TestIntelligenceCore:
    """Test Intelligence Core"""
    
    def setup_method(self):
        self.core = IntelligenceCore()
    
    def test_initialization(self):
        """Test core initialization"""
        assert self.core is not None
        assert self.core.arabic_processor is not None
        assert self.core.context_analyzer is not None
    
    def test_register_agent(self):
        """Test agent registration"""
        web_agent = WebRetrievalAgent()
        self.core.register_agent("test_agent", web_agent)
        
        assert "test_agent" in self.core.agents_registry
    
    @pytest.mark.asyncio
    async def test_process_request_arabic(self):
        """Test processing Arabic request"""
        result = await self.core.process_request("ابحث عن معلومات")
        
        assert result["success"] == True
        assert result["intent"] is not None
        assert "response" in result
    
    @pytest.mark.asyncio
    async def test_process_request_english(self):
        """Test processing English request"""
        result = await self.core.process_request("search for information")
        
        assert result["success"] == True
        assert result["intent"] is not None
    
    def test_get_status(self):
        """Test status retrieval"""
        status = self.core.get_status()
        
        assert "tools_registered" in status
        assert "agents_registered" in status
        assert isinstance(status["tools_registered"], int)


class TestWebRetrievalAgent:
    """Test Web Retrieval Agent"""
    
    def setup_method(self):
        self.agent = WebRetrievalAgent()
    
    def test_initialization(self):
        """Test agent initialization"""
        assert self.agent.name == "WebRetrievalAgent"
        assert "web_search" in self.agent.capabilities
    
    @pytest.mark.asyncio
    async def test_execute_search(self):
        """Test web search execution"""
        result = await self.agent.execute("search for AI")
        
        assert "success" in result
        assert "query" in result
        assert "results" in result


class TestCodeGeneratorAgent:
    """Test Code Generator Agent"""
    
    def setup_method(self):
        self.agent = CodeGeneratorAgent()
    
    def test_initialization(self):
        """Test agent initialization"""
        assert self.agent.name == "CodeGeneratorAgent"
        assert "code_generation" in self.agent.capabilities
    
    @pytest.mark.asyncio
    async def test_execute_python(self):
        """Test Python code generation"""
        result = await self.agent.execute("create a Python function")
        
        assert "success" in result
        assert result["success"] == True
        assert "code" in result
        assert "language" in result
    
    def test_detect_language(self):
        """Test language detection"""
        lang = self.agent._detect_language("write Python code", {})
        assert lang == "python"
        
        lang = self.agent._detect_language("write JavaScript code", {})
        assert lang == "javascript"


# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
