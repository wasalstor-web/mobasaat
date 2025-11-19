#!/usr/bin/env python3
"""
Simple example of using DL+ Intelligence System
مثال بسيط لاستخدام نظام DL+ الذكي
"""

import asyncio
import sys
sys.path.insert(0, '..')

from dlplus import IntelligenceCore
from dlplus.agents import WebRetrievalAgent, CodeGeneratorAgent


async def example_1_arabic_search():
    """Example 1: Arabic web search"""
    print("=" * 50)
    print("مثال 1: البحث بالعربية")
    print("Example 1: Arabic Search")
    print("=" * 50)
    
    core = IntelligenceCore()
    
    # Register agents
    web_agent = WebRetrievalAgent()
    core.register_agent("web_retrieval", web_agent)
    
    # Process Arabic request
    result = await core.process_request(
        "ابحث عن معلومات عن الذكاء الاصطناعي"
    )
    
    print(f"\nResponse: {result['response']}")
    print(f"Intent: {result['intent']}")
    print(f"Tools Used: {result['tools_used']}")
    print(f"Execution Time: {result['execution_time']:.2f}s")
    print()


async def example_2_code_generation():
    """Example 2: Code generation"""
    print("=" * 50)
    print("مثال 2: توليد كود برمجي")
    print("Example 2: Code Generation")
    print("=" * 50)
    
    core = IntelligenceCore()
    
    # Register agents
    code_agent = CodeGeneratorAgent()
    core.register_agent("code_generator", code_agent)
    
    # Process code generation request
    result = await core.process_request(
        "اكتب كود Python لحساب أرقام فيبوناتشي"
    )
    
    print(f"\nResponse: {result['response']}")
    print(f"Intent: {result['intent']}")
    print(f"Tools Used: {result['tools_used']}")
    print()


async def example_3_english_request():
    """Example 3: English request"""
    print("=" * 50)
    print("Example 3: English Request")
    print("=" * 50)
    
    core = IntelligenceCore()
    
    # Process English request
    result = await core.process_request(
        "Search for information about machine learning"
    )
    
    print(f"\nResponse: {result['response']}")
    print(f"Intent: {result['intent']}")
    print(f"Language: {'English' if not result.get('is_arabic') else 'Arabic'}")
    print()


async def example_4_context_management():
    """Example 4: Context management"""
    print("=" * 50)
    print("مثال 4: إدارة السياق")
    print("Example 4: Context Management")
    print("=" * 50)
    
    core = IntelligenceCore()
    
    # First request
    await core.process_request("ابحث عن معلومات عن Python")
    
    # Second related request
    await core.process_request("اكتب كود بايثون بسيط")
    
    # Get context summary
    context = core.context_analyzer.get_context_summary()
    
    print(f"\nConversation Length: {context['conversation_length']}")
    print(f"Recent Intents: {context['recent_intents']}")
    print(f"Tools Used: {context['tools_used']}")
    print()


async def main():
    """Run all examples"""
    print("\n" + "=" * 50)
    print("DL+ Intelligence System Examples")
    print("أمثلة نظام DL+ الذكي")
    print("=" * 50 + "\n")
    
    try:
        await example_1_arabic_search()
        await example_2_code_generation()
        await example_3_english_request()
        await example_4_context_management()
        
        print("=" * 50)
        print("✅ All examples completed successfully!")
        print("✅ جميع الأمثلة تم تنفيذها بنجاح!")
        print("=" * 50)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
