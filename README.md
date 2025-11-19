# AI Agent Platform - منصة الوكيل الذكي
# نظام الذكاء الاصطناعي المستقل

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)

## 🌟 مقدمة | Introduction

**AI Agent Platform** عبارة عن نظام ذكاء اصطناعي مستقل ومتطور يوفر بيئة قوية لبناء ونشر وإدارة الوكلاء الأذكياء (AI Agents) القادرين على التفكير المنطقي، واختيار الأدوات المناسبة، وتنفيذ المهام المعقدة بشكل ذاتي.

**AI Agent Platform** is an advanced autonomous artificial intelligence system that provides a powerful environment for building, deploying, and managing intelligent AI agents capable of logical reasoning, tool selection, and autonomous execution of complex tasks.

### ✨ لماذا هذا المشروع مميز؟ | Why This Project Stands Out?

- **🤖 استقلالية كاملة**: وكيل ذكي يعمل بدون تدخل بشري
- **🧠 تفكير منطقي متقدم**: يحلل المهام ويخطط للحلول
- **🛠️ اختيار أدوات ذكي**: ينتقي الأدوات المناسبة لكل مهمة
- **🇸🇦 دعم عربي أصلي**: معالجة متقدمة للغة العربية الفصحى

---

## 🚀 الميزات الرئيسية | Key Features

### 1. **التفكير المنطقي المتقدم** | Advanced Reasoning
نظام DL+ Intelligence Core يوفر قدرات تفكير متطورة:
- تحليل السياق والمعنى
- فهم النوايا من الأوامر العربية والإنجليزية
- التخطيط متعدد الخطوات
- اتخاذ القرارات الذكية

### 2. **اختيار الأدوات الذكي** | Intelligent Tool Selection
الوكيل يختار تلقائياً الأداة المناسبة من مجموعة شاملة:
- **`run_web_search`** - البحث على الإنترنت وجمع المعلومات
- **`code_generator`** - توليد الأكواد بلغات متعددة
- **`arabic_processor`** - معالجة متقدمة للغة العربية

### 3. **البحث على الويب** | Web Search
وكيل البحث على الويب (WebRetrievalAgent):
- البحث الذكي على الإنترنت
- جمع المعلومات من مصادر متعددة
- تحليل النتائج وترتيبها حسب الأهمية
- دعم الاستعلامات بالعربية والإنجليزية

### 4. **توليد الأكواد** | Code Generation
وكيل توليد الأكواد (CodeGeneratorAgent):
- توليد أكواد احترافية في 10+ لغات برمجة
- Python, JavaScript, Java, C++, Go, Rust, TypeScript
- إنشاء اختبارات وحدة تلقائياً
- توثيق الأكواد بالعربية والإنجليزية

### 5. **معالجة اللغة العربية** | Arabic Language Processing
نظام متقدم لمعالجة العربية:
- دعم العربية الفصحى
- تحليل النوايا من النصوص العربية
- توليد استجابات باللغة العربية السليمة
- فهم السياق العربي

---

## 📖 دليل البدء السريع | Quick Start Guide

### المتطلبات الأساسية | Prerequisites

- Python 3.9 أو أحدث
- pip (مدير حزم Python)

### الخطوة 1: استنساخ المشروع | Clone the Repository

```bash
git clone https://github.com/wasalstor-web/mobasaat.git
cd mobasaat
```

### الخطوة 2: تثبيت المتطلبات | Install Dependencies

```bash
pip install -r requirements.txt
```

### الخطوة 3: إعداد المتغيرات البيئية | Configure Environment Variables

أنشئ ملف `.env` في الجذر:

```env
# API Keys (optional)
OPENROUTER_API_KEY=your_api_key_here
OPENAI_API_KEY=your_openai_key_here

# Server Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG_MODE=False

# Model Configuration
DEFAULT_MODEL=gpt-3.5-turbo
DEFAULT_ARABIC_MODEL=qwen-arabic
```

### الخطوة 4: تشغيل الخادم | Run the Server

```bash
# Using Python
python -m dlplus.main

# Or using uvicorn directly
uvicorn dlplus.main:app --host 0.0.0.0 --port 8000 --reload
```

### الخطوة 5: الوصول للواجهة | Access the API

- **API Docs**: http://localhost:8000/api/docs
- **Health Check**: http://localhost:8000/health
- **Root**: http://localhost:8000/

---

## 💻 أمثلة الاستخدام | Usage Examples

### مثال 1: البحث على الويب
**Arabic Prompt:**
```python
import httpx
import asyncio

async def search_example():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/api/agent/execute",
            json={
                "prompt": "ابحث عن أحدث تطورات الذكاء الاصطناعي في 2024",
                "language": "ar"
            }
        )
        print(response.json())

asyncio.run(search_example())
```

### مثال 2: توليد كود Python
**English Prompt:**
```python
import httpx
import asyncio

async def code_generation_example():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/api/code/generate",
            json={
                "prompt": "Create a Python function that calculates fibonacci numbers",
                "language": "en"
            }
        )
        result = response.json()
        print(result['code'])

asyncio.run(code_generation_example())
```

### مثال 3: استخدام مباشر من Python
```python
from dlplus import IntelligenceCore
import asyncio

async def main():
    # Initialize intelligence core
    core = IntelligenceCore()
    
    # Process request
    result = await core.process_request(
        "ابحث عن معلومات عن الذكاء الاصطناعي"
    )
    
    print(f"Response: {result['response']}")
    print(f"Intent: {result['intent']}")
    print(f"Tools Used: {result['tools_used']}")

asyncio.run(main())
```

---

## 🧠 نظام DL+ للذكاء | DL+ Intelligence System

### المكونات الأساسية | Core Components

#### 1. **نواة الذكاء** | Intelligence Core
`dlplus/core/intelligence_core.py`
- محرك الذكاء الرئيسي
- تنسيق جميع النماذج والوكلاء
- إدارة السياق والذاكرة

#### 2. **معالج اللغة العربية** | Arabic Processor
`dlplus/core/arabic_processor.py`
- معالجة متقدمة للعربية الفصحى
- تحليل النوايا
- استخراج الكيانات

#### 3. **محلل السياق** | Context Analyzer
`dlplus/core/context_analyzer.py`
- فهم سياق المحادثة
- إدارة الذاكرة قصيرة وطويلة المدى
- تتبع العلاقات بين المهام

---

## 📚 البنية التنظيمية | Project Structure

```
mobasaat/
├── dlplus/                      # نظام DL+ الأساسي
│   ├── core/                    # النواة الذكية
│   │   ├── intelligence_core.py     # محرك الذكاء الرئيسي
│   │   ├── arabic_processor.py      # معالج العربية
│   │   └── context_analyzer.py      # محلل السياق
│   ├── agents/                  # الوكلاء الأذكياء
│   │   ├── base_agent.py            # الفئة الأساسية
│   │   ├── web_retrieval_agent.py   # وكيل البحث
│   │   └── code_generator_agent.py  # وكيل توليد الأكواد
│   ├── config/                  # الإعدادات
│   │   ├── settings.py              # إعدادات النظام
│   │   └── models_config.py         # إعدادات النماذج
│   └── main.py                  # تطبيق FastAPI
├── requirements.txt             # المتطلبات
├── mubasat                      # السكريبت الأصلي
└── README.md                    # هذا الملف
```

---

## 🔌 API Reference

### Execute Agent
```http
POST /api/agent/execute
Content-Type: application/json

{
  "prompt": "Your prompt here",
  "context": {},
  "language": "ar"
}
```

### Web Search
```http
POST /api/web/search?query=your+search+query
```

### Generate Code
```http
POST /api/code/generate
Content-Type: application/json

{
  "prompt": "Create a Python function...",
  "language": "en"
}
```

### Health Check
```http
GET /health
```

---

## 🛡️ الأمان وأفضل الممارسات | Security & Best Practices

### الأمان | Security
- ✅ عدم تخزين البيانات الحساسة في المستودع
- ✅ استخدام متغيرات البيئة للمفاتيح
- ✅ مصادقة API آمنة
- ✅ تشفير الاتصالات (HTTPS)

### أفضل الممارسات | Best Practices
- 📝 توثيق شامل للأكواد
- 🧪 اختبارات شاملة
- 🔄 التكامل المستمر
- 📊 مراقبة الأداء والسجلات

---

## 🤝 المساهمة | Contributing

نرحب بمساهماتكم! يرجى:
1. Fork المشروع
2. إنشاء branch للميزة (`git checkout -b feature/AmazingFeature`)
3. Commit التغييرات (`git commit -m 'Add some AmazingFeature'`)
4. Push إلى Branch (`git push origin feature/AmazingFeature`)
5. فتح Pull Request

---

## 📄 الترخيص | License

AI-Agent-Platform © 2025

---

## 📞 الدعم | Support

للأسئلة والدعم:
- افتح Issue في GitHub
- راجع الوثائق في مجلد `docs/`

---

<div align="center">

**صُنع بـ ❤️ للمجتمع العربي والعالمي**

**Made with ❤️ for the Arabic and Global Community**

</div>
