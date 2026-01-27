# Deployment Guide

Complete guide for deploying NotebookLM Skills Suite in cloud environments and integrating with Claude Code.

## Table of Contents

1. [Quick Deployment](#quick-deployment)
2. [Cloud Deployment Options](#cloud-deployment-options)
3. [Claude Code Integration](#claude-code-integration)
4. [Environment Configuration](#environment-configuration)
5. [Docker Deployment](#docker-deployment)
6. [Serverless Deployment](#serverless-deployment)
7. [Production Considerations](#production-considerations)

---

## Quick Deployment

### For Claude Code Users

**One-Command Installation:**

```bash
git clone https://github.com/serenakeyitan/nblm-skills.git
cd nblm-skills
./install_all.sh
```

This automatically:
- ✅ Checks prerequisites (Python, FFmpeg)
- ✅ Installs all dependencies for 8 skills
- ✅ Creates .env templates
- ✅ Verifies installation

**Configure API Keys:**

```bash
# Option 1: Global environment variables (recommended for cloud)
export GEMINI_API_KEY="your_gemini_key"
export ANTHROPIC_API_KEY="your_anthropic_key"

# Option 2: Per-skill .env files
cd audio-overview
cp .env.example .env
# Edit .env with your keys
```

---

## Cloud Deployment Options

### Option 1: GitHub Repository (Recommended for Claude Code)

Skills are loaded directly from GitHub when users invoke them.

**Setup:**

1. Fork or clone the repository
2. Configure secrets in GitHub repository settings:
   - `GEMINI_API_KEY`
   - `ANTHROPIC_API_KEY`

3. Users install with:
   ```bash
   git clone https://github.com/YOUR_USERNAME/nblm-skills.git
   cd nblm-skills
   ./install_all.sh
   ```

**Advantages:**
- ✅ Easy updates via `git pull`
- ✅ Version control
- ✅ No server maintenance
- ✅ Works with Claude Code out of the box

---

### Option 2: Cloud VM (AWS, GCP, Azure)

Deploy on a persistent cloud instance for shared team access.

**AWS EC2 Example:**

```bash
# Launch Ubuntu instance (t3.medium or larger)
# SSH into instance

# Install prerequisites
sudo apt-get update
sudo apt-get install -y python3 python3-pip ffmpeg git

# Clone and install
git clone https://github.com/serenakeyitan/nblm-skills.git
cd nblm-skills
./install_all.sh

# Configure environment
export GEMINI_API_KEY="your_key"
export ANTHROPIC_API_KEY="your_key"

# Test
cd audio-overview && python main.py --test
```

**Cost Estimate:**
- t3.medium: ~$30-40/month
- Storage: ~$5/month
- Total: ~$35-45/month

---

### Option 3: Container Deployment

Containerize for portable, reproducible deployments.

**See Docker Deployment section below.**

---

### Option 4: Serverless (AWS Lambda, Google Cloud Functions)

Deploy individual skills as serverless functions.

**See Serverless Deployment section below.**

---

## Claude Code Integration

### How Claude Code Loads Skills

When you invoke a skill in Claude Code:

1. **Discovery**: Claude Code reads `SKILL.md` frontmatter
2. **Installation Check**: Runs `scripts/install.sh` if not installed
3. **Dependency Loading**: Imports Python modules
4. **Execution**: Calls `main.py` with user parameters

### Skill Registration

Each skill is registered via `skill.yaml`:

```yaml
name: audio-overview
description: Generate professional multi-speaker podcasts...
version: 1.0.0
type: project
gitignored: true

# Installation hook
install_script: scripts/install.sh

# Dependencies
requires:
  - python3
  - ffmpeg

# Configuration
env_template: .env.example

# Entry point
main: main.py
```

### Using Skills in Claude Code

**Method 1: Direct Invocation**

```
User: Generate a podcast from my research paper
Claude: I'll use the audio-overview skill...
[Automatically loads and runs audio-overview]
```

**Method 2: Explicit Skill Call**

```python
# Claude internally executes:
from audio_overview.main import generate_podcast

result = generate_podcast(
    content=user_research,
    num_speakers=2,
    duration_minutes=10
)
```

**Method 3: CLI Invocation**

```bash
# Claude can run as subprocess:
python audio-overview/main.py --input research.txt --output podcast.mp3
```

---

## Environment Configuration

### Required Environment Variables

All skills require:

```bash
GEMINI_API_KEY=your_gemini_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here  # Optional fallback
```

### Optional Variables

For enhanced features:

```bash
# Premium audio quality (audio-overview skill)
ELEVENLABS_API_KEY=your_elevenlabs_key

# Google Cloud TTS (audio-overview skill)
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
```

### Configuration Priority

Skills load configuration in this order:

1. Environment variables
2. `.env` file in skill directory
3. `.env.example` (with warnings if missing keys)

### Secrets Management

**Development:**
```bash
# Use .env files (gitignored)
cp .env.example .env
# Edit .env
```

**Production:**
```bash
# Use environment variables
export GEMINI_API_KEY="..."

# Or use secrets manager
aws secretsmanager get-secret-value --secret-id nblm-skills/api-keys
```

**Cloud Platforms:**
- AWS: AWS Secrets Manager, Systems Manager Parameter Store
- GCP: Secret Manager
- Azure: Key Vault
- Heroku: Config Vars
- Docker: Docker Secrets

---

## Docker Deployment

### Dockerfile for All Skills

Create `Dockerfile` in repository root:

```dockerfile
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Copy skills
COPY . /app/

# Install all skills
RUN chmod +x install_all.sh && ./install_all.sh

# Set environment variables (override at runtime)
ENV GEMINI_API_KEY=""
ENV ANTHROPIC_API_KEY=""

# Expose port if running as API (optional)
EXPOSE 8000

# Default command
CMD ["/bin/bash"]
```

### Build and Run

```bash
# Build image
docker build -t nblm-skills:latest .

# Run with environment variables
docker run -it \
  -e GEMINI_API_KEY="your_key" \
  -e ANTHROPIC_API_KEY="your_key" \
  -v $(pwd)/outputs:/app/outputs \
  nblm-skills:latest

# Test a skill
docker run --rm \
  -e GEMINI_API_KEY="your_key" \
  nblm-skills:latest \
  python audio-overview/main.py --test
```

### Docker Compose

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  nblm-skills:
    build: .
    environment:
      - GEMINI_API_KEY=${GEMINI_API_KEY}
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
    volumes:
      - ./outputs:/app/outputs
    command: /bin/bash

  # Optional: API service
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - GEMINI_API_KEY=${GEMINI_API_KEY}
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
    command: python api_server.py  # If you create API wrapper
```

Run:
```bash
docker-compose up
```

---

## Serverless Deployment

### AWS Lambda Example (Single Skill)

Deploy `audio-overview` as Lambda function:

**1. Create Lambda Package**

```bash
cd audio-overview
pip install -r requirements.txt -t package/
cp main.py config.py package/
cd package && zip -r ../audio-overview-lambda.zip . && cd ..
```

**2. Create Lambda Handler**

Create `lambda_handler.py`:

```python
import json
import os
from main import generate_podcast

def handler(event, context):
    """AWS Lambda handler for audio-overview skill"""

    # Parse input
    content = event.get('content', '')
    duration = event.get('duration_minutes', 10)
    num_speakers = event.get('num_speakers', 2)

    # Generate podcast
    output_path = '/tmp/podcast.mp3'
    result = generate_podcast(
        content=content,
        num_speakers=num_speakers,
        duration_minutes=duration,
        output_path=output_path
    )

    # Upload to S3 or return URL
    # ... S3 upload code ...

    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'Podcast generated',
            'output_path': result
        })
    }
```

**3. Deploy**

```bash
aws lambda create-function \
  --function-name audio-overview-skill \
  --runtime python3.11 \
  --handler lambda_handler.handler \
  --zip-file fileb://audio-overview-lambda.zip \
  --role arn:aws:iam::ACCOUNT:role/lambda-execution-role \
  --environment Variables="{GEMINI_API_KEY=your_key}" \
  --timeout 300 \
  --memory-size 2048
```

**4. Invoke**

```bash
aws lambda invoke \
  --function-name audio-overview-skill \
  --payload '{"content": "Your research...", "duration_minutes": 5}' \
  response.json
```

### Google Cloud Functions Example

```python
# main.py for Cloud Functions
from flask import Request
import functions_framework

@functions_framework.http
def generate_podcast_http(request: Request):
    """Cloud Functions entry point"""
    request_json = request.get_json()

    from audio_overview.main import generate_podcast

    result = generate_podcast(
        content=request_json.get('content'),
        duration_minutes=request_json.get('duration_minutes', 10)
    )

    return {'status': 'success', 'output': result}
```

Deploy:
```bash
gcloud functions deploy audio-overview \
  --runtime python311 \
  --trigger-http \
  --allow-unauthenticated \
  --set-env-vars GEMINI_API_KEY=your_key \
  --timeout 540s \
  --memory 2GB
```

---

## Production Considerations

### Performance Optimization

**1. Caching**
```python
# Cache AI responses
from functools import lru_cache

@lru_cache(maxsize=100)
def generate_dialogue_cached(content_hash, duration):
    # ... AI generation ...
```

**2. Concurrency**
```python
# Process multiple requests concurrently
import asyncio

async def generate_multiple_podcasts(requests):
    tasks = [generate_podcast_async(req) for req in requests]
    return await asyncio.gather(*tasks)
```

**3. Resource Limits**
- CPU: 2-4 cores recommended
- Memory: 2-4 GB for audio/video skills, 512MB-1GB for others
- Disk: 10-20 GB for temp storage
- Network: Good bandwidth for API calls

### Monitoring

**Logging:**
```python
# All skills use loguru
from loguru import logger

logger.add("logs/skill_{time}.log", rotation="1 day")
logger.info("Processing request", extra={"skill": "audio-overview"})
```

**Metrics to Track:**
- Request count per skill
- Average processing time
- Error rate
- API usage (tokens consumed)
- Cost per generation

**Tools:**
- CloudWatch (AWS)
- Stackdriver (GCP)
- Application Insights (Azure)
- Datadog, New Relic (multi-cloud)

### Cost Optimization

**API Usage:**
- Use Gemini 3 Pro (cost-effective)
- Implement caching for repeated requests
- Batch requests when possible

**Compute:**
- Use spot instances for batch processing
- Scale down during low usage
- Use serverless for sporadic workloads

**Storage:**
- Auto-delete old outputs
- Use object storage lifecycle policies
- Compress outputs (gzip for JSON/HTML)

### Security

**1. API Key Protection**
- Never commit keys to version control
- Use secrets managers in production
- Rotate keys regularly
- Implement key usage monitoring

**2. Input Validation**
```python
# Validate user inputs
def validate_input(content: str, max_length: int = 100000):
    if len(content) > max_length:
        raise ValueError("Input too long")
    # Additional validation...
```

**3. Rate Limiting**
```python
from time import time, sleep

class RateLimiter:
    def __init__(self, max_requests_per_minute=10):
        self.max_requests = max_requests_per_minute
        self.requests = []

    def check_rate_limit(self):
        now = time()
        self.requests = [r for r in self.requests if now - r < 60]
        if len(self.requests) >= self.max_requests:
            raise Exception("Rate limit exceeded")
        self.requests.append(now)
```

**4. Output Sanitization**
- Validate generated content
- Scan for malicious code in outputs
- Limit file sizes

### Scaling

**Horizontal Scaling:**
- Deploy multiple instances behind load balancer
- Use message queue for job distribution (RabbitMQ, SQS)
- Stateless design enables easy scaling

**Vertical Scaling:**
- Start with smaller instances
- Monitor resource usage
- Scale up as needed

**Auto-scaling:**
```yaml
# Kubernetes HPA example
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: nblm-skills-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: nblm-skills
  minReplicas: 1
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

---

## Troubleshooting

### Common Issues

**1. FFmpeg not found**
```bash
# Install FFmpeg in Docker
RUN apt-get install -y ffmpeg

# Install FFmpeg on VM
sudo apt-get install ffmpeg  # Linux
brew install ffmpeg          # macOS
```

**2. Out of memory**
```bash
# Increase container memory
docker run -m 4g nblm-skills:latest

# Increase Lambda memory
aws lambda update-function-configuration \
  --function-name audio-overview \
  --memory-size 3008
```

**3. Timeout errors**
```bash
# Increase timeouts
# Lambda: 15 minutes max
# Cloud Functions: 9 minutes max
# Consider splitting long-running tasks
```

**4. API rate limits**
```python
# Implement exponential backoff
import time
from google.api_core import retry

@retry.Retry(predicate=retry.if_exception_type(ResourceExhausted))
def call_api_with_retry():
    # ... API call ...
```

---

## Support

- **Documentation**: See README.md, QUICKSTART.md, TEST_GUIDE.md
- **Issues**: https://github.com/serenakeyitan/nblm-skills/issues
- **Repository**: https://github.com/serenakeyitan/nblm-skills

---

## Next Steps

1. Choose deployment method (GitHub, VM, Docker, Serverless)
2. Configure environment and secrets
3. Run `./install_all.sh`
4. Test with `./test_all_skills.sh`
5. Integrate with Claude Code
6. Monitor and optimize

Happy deploying! 🚀
