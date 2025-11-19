"""
Web Retrieval Agent
وكيل البحث على الويب
"""

import asyncio
import httpx
from typing import Dict, List, Optional
from bs4 import BeautifulSoup

from .base_agent import BaseAgent


class WebRetrievalAgent(BaseAgent):
    """
    Agent for web search and information retrieval
    وكيل البحث وجمع المعلومات من الويب
    """
    
    def __init__(self):
        super().__init__(
            name="WebRetrievalAgent",
            description="Searches the web and retrieves information from various sources"
        )
        self.add_capability("web_search")
        self.add_capability("url_fetch")
        self.add_capability("content_extraction")
        
        # Search engines (for demo purposes, using DuckDuckGo HTML)
        self.search_engines = {
            "duckduckgo": "https://html.duckduckgo.com/html/?q={query}"
        }
    
    async def execute(self, task: str, context: Optional[Dict] = None) -> Dict:
        """
        Execute web search task
        تنفيذ مهمة البحث على الويب
        """
        try:
            # Extract search query
            query = self._extract_query(task, context)
            
            # Perform search
            results = await self._search_web(query)
            
            # Analyze and rank results
            analyzed_results = self._analyze_results(results, query)
            
            self._log_execution(task, analyzed_results, success=True)
            
            return {
                "success": True,
                "query": query,
                "results_count": len(analyzed_results),
                "results": analyzed_results[:10],  # Top 10 results
                "summary": self._create_summary(analyzed_results)
            }
            
        except Exception as e:
            self._log_execution(task, str(e), success=False)
            return {
                "success": False,
                "error": str(e),
                "query": task
            }
    
    def _extract_query(self, task: str, context: Optional[Dict]) -> str:
        """Extract search query from task"""
        # Remove common prefixes
        query = task
        prefixes = [
            "ابحث عن", "ابحث", "search for", "find", "look for",
            "بحث عن", "جد"
        ]
        
        for prefix in prefixes:
            if query.lower().startswith(prefix):
                query = query[len(prefix):].strip()
                break
        
        return query
    
    async def _search_web(self, query: str) -> List[Dict]:
        """
        Perform web search
        (In production, would use proper search API)
        """
        results = []
        
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                # Mock search results for demo
                # In production, use actual search API (Google Custom Search, Bing, etc.)
                results = [
                    {
                        "title": f"Result for: {query}",
                        "url": f"https://example.com/result1",
                        "snippet": f"Information about {query}...",
                        "relevance": 0.95
                    },
                    {
                        "title": f"More about {query}",
                        "url": f"https://example.com/result2",
                        "snippet": f"Detailed information regarding {query}...",
                        "relevance": 0.85
                    }
                ]
                
        except Exception as e:
            print(f"Search error: {e}")
        
        return results
    
    async def fetch_url(self, url: str) -> Dict:
        """Fetch content from a URL"""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(url)
                response.raise_for_status()
                
                # Parse HTML
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Extract text content
                # Remove script and style elements
                for script in soup(["script", "style"]):
                    script.decompose()
                
                text = soup.get_text()
                lines = (line.strip() for line in text.splitlines())
                chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                text = ' '.join(chunk for chunk in chunks if chunk)
                
                return {
                    "success": True,
                    "url": url,
                    "content": text[:5000],  # First 5000 chars
                    "title": soup.title.string if soup.title else ""
                }
                
        except Exception as e:
            return {
                "success": False,
                "url": url,
                "error": str(e)
            }
    
    def _analyze_results(self, results: List[Dict], query: str) -> List[Dict]:
        """Analyze and rank search results"""
        # In production, would use ML model for relevance scoring
        # For now, just return results as-is
        return sorted(results, key=lambda x: x.get("relevance", 0), reverse=True)
    
    def _create_summary(self, results: List[Dict]) -> str:
        """Create summary of search results"""
        if not results:
            return "No results found / لم يتم العثور على نتائج"
        
        summary_parts = [
            f"Found {len(results)} results / تم العثور على {len(results)} نتيجة",
            ""
        ]
        
        for i, result in enumerate(results[:5], 1):
            summary_parts.append(
                f"{i}. {result.get('title', 'Untitled')}\n"
                f"   {result.get('snippet', '')[:100]}..."
            )
        
        return "\n".join(summary_parts)
