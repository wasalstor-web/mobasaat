"""
FastAPI Main Application
تطبيق FastAPI الرئيسي
"""

from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict
import uvicorn

from dlplus.core import IntelligenceCore
from dlplus.agents import WebRetrievalAgent, CodeGeneratorAgent
from dlplus.config import settings

# Initialize FastAPI app
app = FastAPI(
    title="DL+ AI Agent Platform",
    description="Advanced AI Agent Platform with Arabic Support",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize intelligence core
intelligence_core = IntelligenceCore()

# Register agents
web_agent = WebRetrievalAgent()
code_agent = CodeGeneratorAgent()

intelligence_core.register_agent("web_retrieval", web_agent)
intelligence_core.register_agent("code_generator", code_agent)


# Request/Response Models
class AgentRequest(BaseModel):
    """Request model for agent execution"""
    prompt: str
    context: Optional[Dict] = None
    language: Optional[str] = "auto"


class AgentResponse(BaseModel):
    """Response model for agent execution"""
    success: bool
    response: str
    intent: Optional[str] = None
    tools_used: Optional[list] = None
    execution_time: Optional[float] = None


# API Endpoints
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "DL+ AI Agent Platform",
        "message_ar": "منصة الوكلاء الأذكياء DL+",
        "version": "1.0.0",
        "status": "running",
        "docs": "/api/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    system_status = intelligence_core.get_status()
    return {
        "status": "healthy",
        "system": system_status
    }


@app.post("/api/agent/execute", response_model=AgentResponse)
async def execute_agent(request: AgentRequest):
    """
    Execute AI agent with given prompt
    تنفيذ الوكيل الذكي مع الأمر المعطى
    """
    try:
        result = await intelligence_core.process_request(
            user_input=request.prompt,
            context=request.context
        )
        
        return AgentResponse(
            success=result["success"],
            response=result["response"],
            intent=result.get("intent"),
            tools_used=result.get("tools_used"),
            execution_time=result.get("execution_time")
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/agents/list")
async def list_agents():
    """List all registered agents"""
    agents = []
    for name, agent in intelligence_core.agents_registry.items():
        agents.append(agent.get_info())
    
    return {
        "count": len(agents),
        "agents": agents
    }


@app.get("/api/tools/list")
async def list_tools():
    """List all registered tools"""
    tools = []
    for name, tool_info in intelligence_core.tools_registry.items():
        tools.append({
            "name": name,
            "description": tool_info["description"]
        })
    
    return {
        "count": len(tools),
        "tools": tools
    }


@app.post("/api/web/search")
async def web_search(query: str):
    """
    Perform web search
    تنفيذ بحث على الويب
    """
    try:
        result = await web_agent.execute(query)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/code/generate")
async def generate_code(request: AgentRequest):
    """
    Generate code based on requirements
    توليد كود برمجي بناءً على المتطلبات
    """
    try:
        result = await code_agent.execute(request.prompt, request.context)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/context/summary")
async def get_context_summary():
    """Get current context summary"""
    return intelligence_core.context_analyzer.get_context_summary()


@app.post("/api/context/clear")
async def clear_context():
    """Clear conversation context"""
    intelligence_core.context_analyzer.clear_context()
    return {"message": "Context cleared successfully"}


@app.get("/api/status")
async def get_status():
    """Get detailed system status"""
    return intelligence_core.get_status()


# Main entry point
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug_mode
    )
