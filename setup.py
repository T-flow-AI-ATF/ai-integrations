#!/usr/bin/env python3

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="t-flow-ai-triage",
    version="1.0.0",
    author="T-Flow AI Team",
    author_email="contact@t-flow-ai.com",
    description="AI-powered medical triage system using Groq's llama-3.3-70b-versatile with Supabase integration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/T-flow-AI-ATF/ai-integrations",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Healthcare Industry",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "groq>=0.9.0",
        "supabase>=2.1.0", 
        "python-dotenv>=1.0.0",
        "websockets>=11.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "triage-test=test:main",
        ],
    },
)
