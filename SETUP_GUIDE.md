# PROTOCOL:LOOP - Setup Guide

## Prerequisites

### System Requirements
- Python 3.9 or higher
- 4GB RAM minimum (8GB recommended)
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Internet connection for LLM API calls

### Required Accounts
- OpenAI API key (recommended) OR
- Anthropic API key OR
- Google AI API key

## Installation Steps

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/protocol-loop.git
cd protocol-loop
```

### 2. Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

**Optional: Install development dependencies**
```bash
pip install -r requirements.txt[dev]
```

### 4. Configure Environment Variables

Copy the example environment file:
```bash
cp .env.example .env
```

Edit `.env` with your preferred text editor and add your API keys:
```bash
# OpenAI (recommended)
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-4-turbo-preview

# OR Anthropic Claude
ANTHROPIC_API_KEY=sk-ant-your-key-here
ANTHROPIC_MODEL=claude-3-opus-20240229

# OR Google Gemini
GOOGLE_API_KEY=your-google-key-here
GEMINI_MODEL=gemini-pro

# Set your default provider
DEFAULT_LLM_PROVIDER=openai  # or anthropic, gemini
```

### 5. Create Required Directories
```bash
mkdir -p logs models
```

### 6. Install Package (Optional)

For system-wide access to command-line tools:
```bash
pip install -e .
```

## Database Setup

### Development (SQLite)

No additional setup required. Database will be created automatically.

### Production (PostgreSQL)

1. Install PostgreSQL
2. Create database:
```sql
CREATE DATABASE protocol_loop;
CREATE USER protocol_user WITH PASSWORD 'your-password';
GRANT ALL PRIVILEGES ON DATABASE protocol_loop TO protocol_user;
```

3. Update `.env`:
```bash
DATABASE_URL=postgresql://protocol_user:your-password@localhost/protocol_loop
```

4. Run migrations:
```bash
alembic upgrade head
```

## Verification

### 1. Test Installation
```bash
python -c "import backend; print('✓ Backend imported successfully')"
```

### 2. Check Dependencies
```bash
pip list | grep -E "fastapi|torch|transformers|openai"
```

### 3. Verify API Keys
```bash
python -c "from backend.config import settings; print('API Keys configured:', bool(settings.OPENAI_API_KEY or settings.ANTHROPIC_API_KEY))"
```

## Optional Components

### Redis (for production scaling)

**Install Redis:**

**macOS:**
```bash
brew install redis
brew services start redis
```

**Ubuntu/Debian:**
```bash
sudo apt-get install redis-server
sudo systemctl start redis
```

**Update `.env`:**
```bash
REDIS_URL=redis://localhost:6379/0
```

### SpaCy Language Model

For advanced NLP features:
```bash
python -m spacy download en_core_web_sm
```

## Troubleshooting

### Issue: Module not found

**Solution:**
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### Issue: API key errors

**Solution:**
- Verify key is correct in `.env`
- Check API key has credits/permissions
- Ensure no extra spaces in `.env` file

### Issue: Port already in use

**Solution:**
```bash
# Change port in .env
PORT=8001

# Or kill process using port
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux
lsof -ti:8000 | xargs kill -9
```

### Issue: Torch installation fails

**Solution:**
```bash
# Install CPU-only version (lighter)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

## Next Steps

Once setup is complete:

1. Read [HOW_TO_RUN.md](HOW_TO_RUN.md) for running instructions
2. Check [DOCUMENTATION.md](DOCUMENTATION.md) for detailed API docs
3. Try the interactive demo: `python demo/interactive_demo.py`

## Getting Help

- **GitHub Issues**: https://github.com/yourusername/protocol-loop/issues
- **Documentation**: See DOCUMENTATION.md
- **Discord**: [Join our community]

## Common Configurations

### Minimal Setup (Testing)
```bash
# .env for testing without LLM
DEBUG=True
OPENAI_API_KEY=  # Leave empty
DEFAULT_LLM_PROVIDER=openai
ENABLE_ANALYTICS=False
```

### Production Setup
```bash
# .env for production
DEBUG=False
DATABASE_URL=postgresql://user:pass@localhost/protocol_loop
REDIS_URL=redis://localhost:6379/0
LOG_LEVEL=INFO
ENABLE_ANALYTICS=True
```

### Local Development
```bash
# .env for local development
DEBUG=True
LOG_LEVEL=DEBUG
CORS_ORIGINS=["http://localhost:3000", "http://localhost:8000"]
```