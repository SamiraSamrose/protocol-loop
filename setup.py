from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="protocol-loop",
    version="1.0.0",
    author="Protocol Team",
    author_email="team@protocol-loop.ai",
    description="Recursive AI Consciousness Simulator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/protocol-loop",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.9",
    install_requires=[
        "fastapi>=0.104.1",
        "uvicorn[standard]>=0.24.0",
        "torch>=2.1.0",
        "transformers>=4.35.0",
        "langchain>=0.0.335",
        "openai>=1.3.0",
        "anthropic>=0.7.1",
        "scikit-learn>=1.3.2",
        "networkx>=3.2.1",
        "numpy>=1.26.2",
        "pandas>=2.1.3",
        "sqlalchemy>=2.0.23",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.3",
            "black>=23.11.0",
            "flake8>=6.1.0",
            "mypy>=1.7.1",
        ],
    },
    entry_points={
        "console_scripts": [
            "protocol-loop=backend.app:main",
            "protocol-demo=demo.interactive_demo:main",
        ],
    },
)