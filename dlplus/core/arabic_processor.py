"""
Arabic Language Processor
معالج اللغة العربية المتقدم
"""

import re
from typing import Dict, List, Optional, Tuple
from enum import Enum


class IntentType(Enum):
    """Types of user intents / أنواع النوايا"""
    SEARCH = "search"
    GENERATE_CODE = "generate_code"
    EXECUTE_COMMAND = "execute_command"
    CREATE_FILE = "create_file"
    READ_FILE = "read_file"
    ANALYZE = "analyze"
    TRANSLATE = "translate"
    SUMMARIZE = "summarize"
    UNKNOWN = "unknown"


class ArabicProcessor:
    """
    Advanced Arabic language processor
    معالج متقدم للغة العربية
    """
    
    def __init__(self):
        # Arabic intent keywords / كلمات مفتاحية للنوايا
        self.intent_keywords = {
            IntentType.SEARCH: [
                "ابحث", "بحث", "ابحث عن", "جد", "ايجاد", "أبحث"
            ],
            IntentType.GENERATE_CODE: [
                "اكتب كود", "كود", "برمجة", "انشئ برنامج", "اكتب برنامج",
                "كود برمجي", "سكريبت"
            ],
            IntentType.EXECUTE_COMMAND: [
                "نفذ", "شغل", "قم بتنفيذ", "تنفيذ", "تشغيل"
            ],
            IntentType.CREATE_FILE: [
                "انشئ ملف", "اكتب ملف", "احفظ في ملف", "اصنع ملف"
            ],
            IntentType.READ_FILE: [
                "اقرأ ملف", "افتح ملف", "اعرض محتوى", "محتوى الملف"
            ],
            IntentType.ANALYZE: [
                "حلل", "تحليل", "قم بتحليل", "افحص"
            ],
            IntentType.TRANSLATE: [
                "ترجم", "ترجمة", "قم بالترجمة"
            ],
            IntentType.SUMMARIZE: [
                "لخص", "تلخيص", "اختصر", "خلاصة"
            ]
        }
        
        # Arabic diacritics / التشكيل العربي
        self.arabic_diacritics = re.compile(r'[\u0617-\u061A\u064B-\u0652]')
        
        # Arabic letters range
        self.arabic_range = re.compile(r'[\u0600-\u06FF]')
    
    def is_arabic(self, text: str) -> bool:
        """Check if text contains Arabic characters"""
        return bool(self.arabic_range.search(text))
    
    def remove_diacritics(self, text: str) -> str:
        """Remove Arabic diacritics/تشكيل"""
        return self.arabic_diacritics.sub('', text)
    
    def normalize_text(self, text: str) -> str:
        """Normalize Arabic text"""
        # Remove diacritics
        text = self.remove_diacritics(text)
        
        # Normalize Alef variations
        text = re.sub(r'[إأآا]', 'ا', text)
        
        # Normalize Teh Marbuta
        text = re.sub(r'ة', 'ه', text)
        
        # Remove extra spaces
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def detect_intent(self, text: str) -> IntentType:
        """
        Detect user intent from Arabic or English text
        كشف نية المستخدم من النص
        """
        text_normalized = self.normalize_text(text.lower())
        
        # Check Arabic keywords
        for intent, keywords in self.intent_keywords.items():
            for keyword in keywords:
                if keyword in text_normalized:
                    return intent
        
        # Check English keywords
        if any(word in text.lower() for word in ['search', 'find', 'look for']):
            return IntentType.SEARCH
        elif any(word in text.lower() for word in ['code', 'program', 'script', 'generate']):
            return IntentType.GENERATE_CODE
        elif any(word in text.lower() for word in ['execute', 'run', 'command']):
            return IntentType.EXECUTE_COMMAND
        elif any(word in text.lower() for word in ['create file', 'write file', 'save to']):
            return IntentType.CREATE_FILE
        elif any(word in text.lower() for word in ['read file', 'open file', 'file content']):
            return IntentType.READ_FILE
        elif any(word in text.lower() for word in ['analyze', 'analysis', 'examine']):
            return IntentType.ANALYZE
        
        return IntentType.UNKNOWN
    
    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """
        Extract entities from text (file names, URLs, commands, etc.)
        استخراج الكيانات من النص
        """
        entities = {
            "files": [],
            "urls": [],
            "commands": [],
            "keywords": []
        }
        
        # Extract file names (with extensions)
        file_pattern = r'\b[\w\-]+\.(py|js|txt|md|json|html|css|sh|yml|yaml|env)\b'
        entities["files"] = re.findall(file_pattern, text, re.IGNORECASE)
        
        # Extract URLs
        url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
        entities["urls"] = re.findall(url_pattern, text)
        
        # Extract quoted strings (potential commands or keywords)
        quoted_pattern = r'["\']([^"\']+)["\']'
        entities["keywords"] = re.findall(quoted_pattern, text)
        
        return entities
    
    def generate_response(self, intent: IntentType, context: Dict) -> str:
        """
        Generate Arabic response based on intent
        توليد استجابة عربية بناءً على النية
        """
        responses = {
            IntentType.SEARCH: "سأقوم بالبحث عن المعلومات المطلوبة...",
            IntentType.GENERATE_CODE: "سأقوم بتوليد الكود البرمجي المطلوب...",
            IntentType.EXECUTE_COMMAND: "سأقوم بتنفيذ الأمر المطلوب...",
            IntentType.CREATE_FILE: "سأقوم بإنشاء الملف المطلوب...",
            IntentType.READ_FILE: "سأقوم بقراءة محتوى الملف...",
            IntentType.ANALYZE: "سأقوم بتحليل المعلومات...",
            IntentType.TRANSLATE: "سأقوم بالترجمة...",
            IntentType.SUMMARIZE: "سأقوم بتلخيص المحتوى...",
            IntentType.UNKNOWN: "لم أتمكن من فهم الطلب. يرجى إعادة صياغته."
        }
        
        return responses.get(intent, responses[IntentType.UNKNOWN])
    
    def format_arabic_text(self, text: str) -> str:
        """Format Arabic text properly with correct spacing and punctuation"""
        # Fix spacing around Arabic punctuation
        text = re.sub(r'\s*([،؛؟])\s*', r'\1 ', text)
        text = re.sub(r'\s*([.])\s*', r'. ', text)
        
        # Ensure space after numbers
        text = re.sub(r'(\d)([ء-ي])', r'\1 \2', text)
        
        return text.strip()
