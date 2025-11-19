"""
DL+ Intelligence System Configuration
إعدادات نظام DL+ الذكي
"""

import os
from typing import Dict, List, Optional
from pathlib import Path
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Main system settings / الإعدادات الرئيسية للنظام"""
    
    # API Keys
    openrouter_api_key: str = Field(default="", env="OPENROUTER_API_KEY")
    openai_api_key: str = Field(default="", env="OPENAI_API_KEY")
    anthropic_api_key: str = Field(default="", env="ANTHROPIC_API_KEY")
    
    # Server Configuration
    api_host: str = Field(default="0.0.0.0", env="API_HOST")
    api_port: int = Field(default=8000, env="API_PORT")
    debug_mode: bool = Field(default=False, env="DEBUG_MODE")
    
    # VPS/Hostinger Configuration
    vps_host: Optional[str] = Field(default=None, env="VPS_HOST")
    vps_user: Optional[str] = Field(default=None, env="VPS_USER")
    vps_key: Optional[str] = Field(default=None, env="VPS_KEY")
    vps_port: int = Field(default=22, env="VPS_PORT")
    
    # Model Configuration
    default_model: str = Field(default="gpt-3.5-turbo", env="DEFAULT_MODEL")
    default_arabic_model: str = Field(default="qwen-2.5-arabic", env="DEFAULT_ARABIC_MODEL")
    max_tokens: int = Field(default=2000, env="MAX_TOKENS")
    temperature: float = Field(default=0.7, env="TEMPERATURE")
    
    # Agent Configuration
    max_reasoning_steps: int = Field(default=5, env="MAX_REASONING_STEPS")
    enable_web_search: bool = Field(default=True, env="ENABLE_WEB_SEARCH")
    enable_code_generation: bool = Field(default=True, env="ENABLE_CODE_GENERATION")
    enable_shell_execution: bool = Field(default=False, env="ENABLE_SHELL_EXECUTION")
    
    # Paths
    base_dir: Path = Path(__file__).parent.parent.parent
    logs_dir: Path = base_dir / "logs"
    cache_dir: Path = base_dir / "cache"
    output_dir: Path = base_dir / "output"
    
    # Security
    allowed_commands: List[str] = [
        'ls', 'pwd', 'whoami', 'date', 'uptime',
        'df -h', 'free -m', 'node --version',
        'npm --version', 'python --version'
    ]
    api_key_header: str = "X-API-Key"
    
    # Language Support
    supported_languages: List[str] = ["ar", "en"]
    default_language: str = "ar"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Create necessary directories
        for directory in [self.logs_dir, self.cache_dir, self.output_dir]:
            directory.mkdir(parents=True, exist_ok=True)


# Global settings instance
settings = Settings()
