"""
AI Models Configuration
إعدادات نماذج الذكاء الاصطناعي
"""

from typing import Dict, List
from pydantic import BaseModel


class ModelConfig(BaseModel):
    """Configuration for a single AI model"""
    name: str
    provider: str
    max_tokens: int
    supports_arabic: bool = False
    supports_code: bool = False
    cost_per_1k_tokens: float = 0.0
    description: str = ""


# Arabic Language Models / نماذج اللغة العربية
ARABIC_MODELS = {
    "arabert": ModelConfig(
        name="arabert-base-v2",
        provider="huggingface",
        max_tokens=512,
        supports_arabic=True,
        cost_per_1k_tokens=0.0,
        description="Arabic BERT model for NLP tasks"
    ),
    "qwen-arabic": ModelConfig(
        name="qwen/qwen-2.5-72b-instruct",
        provider="openrouter",
        max_tokens=4096,
        supports_arabic=True,
        cost_per_1k_tokens=0.002,
        description="Qwen 2.5 with excellent Arabic support"
    ),
    "camelbert": ModelConfig(
        name="CAMeLBERT-Mix",
        provider="huggingface",
        max_tokens=512,
        supports_arabic=True,
        cost_per_1k_tokens=0.0,
        description="CAMeL Arabic BERT model"
    )
}

# General Purpose Models / النماذج العامة
GENERAL_MODELS = {
    "gpt-3.5-turbo": ModelConfig(
        name="gpt-3.5-turbo",
        provider="openai",
        max_tokens=4096,
        supports_arabic=True,
        supports_code=True,
        cost_per_1k_tokens=0.002,
        description="Fast and efficient general-purpose model"
    ),
    "gpt-4": ModelConfig(
        name="gpt-4",
        provider="openai",
        max_tokens=8192,
        supports_arabic=True,
        supports_code=True,
        cost_per_1k_tokens=0.03,
        description="Most capable OpenAI model"
    ),
    "claude-3": ModelConfig(
        name="claude-3-opus-20240229",
        provider="anthropic",
        max_tokens=4096,
        supports_arabic=True,
        supports_code=True,
        cost_per_1k_tokens=0.015,
        description="Advanced Claude 3 model"
    ),
    "llama-3": ModelConfig(
        name="meta-llama/llama-3-70b-instruct",
        provider="openrouter",
        max_tokens=8192,
        supports_arabic=True,
        supports_code=True,
        cost_per_1k_tokens=0.0008,
        description="Meta's powerful open-source model"
    ),
    "mistral-7b": ModelConfig(
        name="mistralai/mistral-7b-instruct",
        provider="openrouter",
        max_tokens=8192,
        supports_arabic=True,
        supports_code=True,
        cost_per_1k_tokens=0.0002,
        description="Efficient Mistral model"
    )
}

# Code Generation Models / نماذج توليد الأكواد
CODE_MODELS = {
    "deepseek-coder": ModelConfig(
        name="deepseek/deepseek-coder-33b-instruct",
        provider="openrouter",
        max_tokens=16384,
        supports_code=True,
        cost_per_1k_tokens=0.0006,
        description="Specialized code generation model"
    ),
    "codellama": ModelConfig(
        name="meta-llama/codellama-34b-instruct",
        provider="openrouter",
        max_tokens=16384,
        supports_code=True,
        cost_per_1k_tokens=0.0008,
        description="Meta's code-focused LLaMA"
    )
}

# Combine all models
ALL_MODELS = {
    **ARABIC_MODELS,
    **GENERAL_MODELS,
    **CODE_MODELS
}


def get_model_config(model_name: str) -> ModelConfig:
    """Get configuration for a specific model"""
    return ALL_MODELS.get(model_name, GENERAL_MODELS["gpt-3.5-turbo"])


def get_models_by_capability(arabic: bool = False, code: bool = False) -> List[str]:
    """Get list of models that support specific capabilities"""
    models = []
    for name, config in ALL_MODELS.items():
        if arabic and not config.supports_arabic:
            continue
        if code and not config.supports_code:
            continue
        models.append(name)
    return models
