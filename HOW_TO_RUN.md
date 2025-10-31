# PROTOCOL:LOOP - How to Run

## Quick Start

### 1. Start the Backend Server

**Standard Mode:**
```bash
python backend/app.py
```

**Development Mode (with auto-reload):**
```bash
uvicorn backend.app:app --reload --host 0.0.0.0 --port 8000
```

**Production Mode:**
```bash
uvicorn backend.app:app --workers 4 --host 0.0.0.0 --port 8000
```

### 2. Access the Application

Open your browser and navigate to:
- **Main Application**: http://localhost:8000
- **Interactive Demo**: http://localhost:8000/demo
- **Evolution Visualization**: http://localhost:8000/evolution
- **API Health Check**: http://localhost:8000/health
- **API Documentation**: http://localhost:8000/docs

## Running Different Components

### Interactive CLI Demo

Test all features from the command line:
```bash
python demo/interactive_demo.py
```

Or if installed:
```bash
protocol-demo
```

**Features:**
1. Initialize Player
2. Start New Loop
3. Generate Protocol (with LLM)
4. View Cognitive State
5. View Evolution Tree
6. Simulate Decision
7. Complete Loop
8. Run Full Simulation
9. Exit

### Run Tests

**All Tests:**
```bash
pytest
```

**Specific Test File:**
```bash
pytest tests/test_loop_system.py
```

**With Coverage:**
```bash
pytest --cov=backend --cov-report=html
```

**Verbose Output:**
```bash
pytest -v -s
```

### Jupyter Notebooks

For prototyping and experimentation:
```bash
jupyter notebook notebooks/
```

Open `prototype_testing.ipynb` or `ml_simulation.ipynb`

## Running with Docker

### Build Image
```bash
docker build -t protocol-loop .
```

### Run Container
```bash
docker run -p 8000:8000 --env-file .env protocol-loop
```

### Docker Compose
```yaml
# docker-compose.yml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "8000:8000"
    env_file:
      - .env
    volumes:
      - ./logs:/app/logs
      - ./models:/app/models
```
```bash
docker-compose up
```

## Development Workflow

### 1. Start Backend in Development Mode

Terminal 1:
```bash
source venv/bin/activate  # or venv\Scripts\activate on Windows
uvicorn backend.app:app --reload
```

### 2. Monitor Logs

Terminal 2:
```bash
tail -f logs/protocol_loop.log
```

### 3. Run Frontend Development

If using separate frontend framework:
```bash
npm run dev  # or your frontend command
```

### 4. Testing Changes
```bash
# Run specific test
pytest tests/test_evolution.py::TestEvolutionEngine::test_apply_decision_impact

# Run with print statements
pytest -s tests/test_loop_system.py
```

## API Testing

### Using cURL

**Start Loop:**
```bash
curl -X POST "http://localhost:8000/api/protocols/start-loop?player_id=test_user"
**Generate Protocol:**
```bash
curl -X POST "http://localhost:8000/api/protocols/generate-protocol?player_id=test_user"
```

**Get Cognitive State:**
```bash
curl "http://localhost:8000/api/protocols/cognitive-state/test_user"
```

### Using Python Requests
```python
import requests

# Start a loop
response = requests.post(
    "http://localhost:8000/api/protocols/start-loop",
    params={"player_id": "test_user"}
)
print(response.json())

# Generate protocol
response = requests.post(
    "http://localhost:8000/api/protocols/generate-protocol",
    params={"player_id": "test_user"}
)
print(response.json())
```

### Using HTTPie
```bash
# Install httpie
pip install httpie

# Test endpoints
http POST localhost:8000/api/protocols/start-loop player_id==test_user
http GET localhost:8000/api/protocols/cognitive-state/test_user
```

## Performance Monitoring

### Enable Debug Logging

In `.env`:
```bash
DEBUG=True
LOG_LEVEL=DEBUG
```

View logs:
```bash
tail -f logs/protocol_loop.log
```

### Monitor API Performance
```bash
# Check health endpoint
curl http://localhost:8000/health

# Response should be:
# {"status":"healthy","version":"1.0.0","service":"PROTOCOL:LOOP"}
```

### WebSocket Testing

Using `wscat`:
```bash
npm install -g wscat
wscat -c ws://localhost:8000/api/protocols/ws/loop/test_user
```

## Production Deployment

### Using Gunicorn
```bash
gunicorn backend.app:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --access-logfile logs/access.log \
  --error-logfile logs/error.log
```

### Using Systemd (Linux)

Create `/etc/systemd/system/protocol-loop.service`:
```ini
[Unit]
Description=PROTOCOL:LOOP Service
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/protocol-loop
Environment="PATH=/path/to/protocol-loop/venv/bin"
ExecStart=/path/to/protocol-loop/venv/bin/uvicorn backend.app:app --host 0.0.0.0 --port 8000

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable protocol-loop
sudo systemctl start protocol-loop
sudo systemctl status protocol-loop
```

### Nginx Reverse Proxy
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /ws/ {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

## Troubleshooting

### Server Won't Start

**Check if port is in use:**
```bash
# Windows
netstat -ano | findstr :8000

# macOS/Linux
lsof -i :8000
```

**Solution:**
```bash
# Change port
PORT=8001 python backend/app.py

# Or kill existing process
kill -9 <PID>
```

### LLM API Errors

**Check API key:**
```python
python -c "from backend.config import settings; print(f'Key configured: {bool(settings.OPENAI_API_KEY)}')"
```

**Test API connection:**
```python
import openai
openai.api_key = "your-key"
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Test"}]
)
print("Connection successful!")
```

### Database Errors

**Reset database:**
```bash
rm protocol_loop.db
python backend/app.py  # Will recreate
```

**For PostgreSQL:**
```bash
psql -U protocol_user -d protocol_loop
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
alembic upgrade head
```

### Import Errors

**Reinstall dependencies:**
```bash
pip install -r requirements.txt --force-reinstall
```

**Check Python path:**
```bash
python -c "import sys; print('\n'.join(sys.path))"
```

## Environment-Specific Commands

### Windows

**Activate virtual environment:**
```cmd
venv\Scripts\activate
```

**Run server:**
```cmd
python backend\app.py
```

**Set environment variable:**
```cmd
set PORT=8000
python backend\app.py
```

### macOS/Linux

**Activate virtual environment:**
```bash
source venv/bin/activate
```

**Run server:**
```bash
python3 backend/app.py
```

**Set environment variable:**
```bash
PORT=8000 python backend/app.py
```

## Demo Scenarios

### Quick Demo (No LLM Required)
```bash
# Start server
python backend/app.py

# In another terminal, run demo
python demo/interactive_demo.py

# Select options:
# 1 - Initialize Player
# 6 - Simulate Decision (repeat 3-5 times)
# 4 - View Cognitive State
```

### Full LLM Demo
```bash
# Ensure API key is configured in .env
python demo/interactive_demo.py

# Select options:
# 1 - Initialize Player
# 2 - Start New Loop
# 3 - Generate Protocol (wait 5-10 seconds)
# 6 - Simulate Decision
# 7 - Complete Loop
```

### Web Interface Demo
```bash
# Start server
python backend/app.py

# Open browser to http://localhost:8000/demo

# Click through:
# - Test Loop System
# - Test LLM Generation
# - Test Evolution Engine
# - Test Visualization
```

## Monitoring & Logs

### View Real-time Logs
```bash
# Application logs
tail -f logs/protocol_loop.log

# With grep filtering
tail -f logs/protocol_loop.log | grep ERROR

# Colorized output (if using ccze)
tail -f logs/protocol_loop.log | ccze -A
```

### Log Levels

Change in `.env`:
```bash
LOG_LEVEL=DEBUG   # Verbose
LOG_LEVEL=INFO    # Standard
LOG_LEVEL=WARNING # Minimal
LOG_LEVEL=ERROR   # Errors only
```

## Scaling

### Horizontal Scaling

Run multiple workers:
```bash
uvicorn backend.app:app --workers 4
```

### Load Balancing

Use Nginx or HAProxy to distribute across multiple instances:
```nginx
upstream protocol_loop {
    server 127.0.0.1:8000;
    server 127.0.0.1:8001;
    server 127.0.0.1:8002;
}

server {
    listen 80;
    location / {
        proxy_pass http://protocol_loop;
    }
}
```

### Caching

Enable Redis for session caching:
```bash
# Install Redis
brew install redis  # macOS
sudo apt-get install redis  # Ubuntu

# Start Redis
redis-server

# Update .env
REDIS_URL=redis://localhost:6379/0
```

## Backup & Restore

### Backup Database

**SQLite:**
```bash
cp protocol_loop.db protocol_loop_backup_$(date +%Y%m%d).db
```

**PostgreSQL:**
```bash
pg_dump protocol_loop > backup_$(date +%Y%m%d).sql
```

### Backup Models
```bash
tar -czf models_backup_$(date +%Y%m%d).tar.gz models/
```

### Restore

**SQLite:**
```bash
cp protocol_loop_backup_20240101.db protocol_loop.db
```

**PostgreSQL:**
```bash
psql protocol_loop < backup_20240101.sql
```

## Shutdown

### Graceful Shutdown

Press `Ctrl+C` in the terminal running the server.

### Force Kill
```bash
# Find process
ps aux | grep uvicorn

# Kill process
kill -9 <PID>

# Or use pkill
pkill -f uvicorn
```

### Cleanup
```bash
# Remove logs
rm -rf logs/*.log

# Clear cache
rm -rf __pycache__
find . -type d -name "__pycache__" -exec rm -rf {} +

# Remove database (caution!)
rm protocol_loop.db
```

## Common Workflows

### Daily Development
```bash
# 1. Activate environment
source venv/bin/activate

# 2. Pull latest changes
git pull origin main

# 3. Install any new dependencies
pip install -r requirements.txt

# 4. Run tests
pytest

# 5. Start server
uvicorn backend.app:app --reload

# 6. Code and test
# ...

# 7. Before committing
black backend/  # Format code
flake8 backend/  # Check style
pytest  # Run tests
```

### Testing New Features
```bash
# 1. Create feature branch
git checkout -b feature/new-protocol-type

# 2. Implement feature
# ...

# 3. Write tests
# tests/test_new_feature.py

# 4. Run specific tests
pytest tests/test_new_feature.py -v

# 5. Test in demo
python demo/interactive_demo.py

# 6. Test in browser
open http://localhost:8000/demo
```

### Debugging Issues
```bash
# 1. Enable debug mode
echo "DEBUG=True" >> .env
echo "LOG_LEVEL=DEBUG" >> .env

# 2. Tail logs
tail -f logs/protocol_loop.log &

# 3. Run with verbose output
python -u backend/app.py

# 4. Use debugger
python -m pdb backend/app.py

# 5. Check API docs
open http://localhost:8000/docs
```
