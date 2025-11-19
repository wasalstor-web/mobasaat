# Quick Start Guide | دليل البدء السريع

## English Version

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/wasalstor-web/mobasaat.git
cd mobasaat
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Configure environment (optional):**
```bash
cp .env.example .env
# Edit .env with your API keys if needed
```

4. **Start the server:**
```bash
# Using the startup script
./start.sh

# Or manually
python -m uvicorn dlplus.main:app --host 0.0.0.0 --port 8000
```

5. **Access the API:**
- API Documentation: http://localhost:8000/api/docs
- Health Check: http://localhost:8000/health

### Quick Examples

#### Example 1: Web Search (Python)
```python
import asyncio
from dlplus import IntelligenceCore

async def main():
    core = IntelligenceCore()
    result = await core.process_request("Search for AI trends")
    print(result['response'])

asyncio.run(main())
```

#### Example 2: Code Generation
```python
import asyncio
from dlplus import IntelligenceCore
from dlplus.agents import CodeGeneratorAgent

async def main():
    core = IntelligenceCore()
    code_agent = CodeGeneratorAgent()
    core.register_agent("code_gen", code_agent)
    
    result = await core.process_request(
        "Create a Python function to calculate fibonacci"
    )
    print(result['response'])

asyncio.run(main())
```

#### Example 3: Using the API (curl)
```bash
# Execute agent
curl -X POST "http://localhost:8000/api/agent/execute" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Search for Python tutorials"}'

# Web search
curl -X POST "http://localhost:8000/api/web/search?query=artificial+intelligence"

# Generate code
curl -X POST "http://localhost:8000/api/code/generate" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Create a hello world function"}'
```

---

## النسخة العربية

### التثبيت

1. **استنساخ المستودع:**
```bash
git clone https://github.com/wasalstor-web/mobasaat.git
cd mobasaat
```

2. **تثبيت المتطلبات:**
```bash
pip install -r requirements.txt
```

3. **إعداد البيئة (اختياري):**
```bash
cp .env.example .env
# عدّل ملف .env بمفاتيح API الخاصة بك إذا لزم الأمر
```

4. **تشغيل الخادم:**
```bash
# باستخدام سكريبت البدء
./start.sh

# أو يدوياً
python -m uvicorn dlplus.main:app --host 0.0.0.0 --port 8000
```

5. **الوصول للـ API:**
- توثيق API: http://localhost:8000/api/docs
- فحص الحالة: http://localhost:8000/health

### أمثلة سريعة

#### مثال 1: البحث على الويب (Python)
```python
import asyncio
from dlplus import IntelligenceCore

async def main():
    core = IntelligenceCore()
    result = await core.process_request("ابحث عن تطورات الذكاء الاصطناعي")
    print(result['response'])

asyncio.run(main())
```

#### مثال 2: توليد الأكواد
```python
import asyncio
from dlplus import IntelligenceCore
from dlplus.agents import CodeGeneratorAgent

async def main():
    core = IntelligenceCore()
    code_agent = CodeGeneratorAgent()
    core.register_agent("code_gen", code_agent)
    
    result = await core.process_request(
        "اكتب دالة بايثون لحساب فيبوناتشي"
    )
    print(result['response'])

asyncio.run(main())
```

#### مثال 3: استخدام API (curl)
```bash
# تنفيذ الوكيل
curl -X POST "http://localhost:8000/api/agent/execute" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "ابحث عن دروس بايثون"}'

# البحث على الويب
curl -X POST "http://localhost:8000/api/web/search?query=ذكاء+اصطناعي"

# توليد كود
curl -X POST "http://localhost:8000/api/code/generate" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "اكتب دالة Hello World"}'
```

---

## Using GitHub Actions

You can also execute the AI agent directly through GitHub Actions:

1. Go to your repository on GitHub
2. Click on "Actions" tab
3. Select "DL+ AI Agent Execution" workflow
4. Click "Run workflow"
5. Enter your prompt (in Arabic or English)
6. View results in the workflow logs

---

## Troubleshooting

### Port already in use
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Or use a different port
python -m uvicorn dlplus.main:app --port 8001
```

### Module not found
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Import errors
```bash
# Make sure you're in the correct directory
cd /path/to/mobasaat
python -c "import dlplus; print(dlplus.__version__)"
```

---

## Next Steps

- Read the [full documentation](README.md)
- Check out [examples](examples/)
- Run [tests](tests/)
- Explore the [API documentation](http://localhost:8000/api/docs)
