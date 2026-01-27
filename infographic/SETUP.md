# Infographic Skill Setup

## Quick Setup

**Good news!** If you're using the standalone package (`infographic_skill_standalone.zip`), the API keys are **already included** in the `.env` file. You can skip the API key setup and go straight to testing!

### Super Quick Start (Standalone Package)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Test it (API key already configured!)
python main.py --test

# 3. Generate your infographic
python main.py --input your_content.txt --output infographic.png
```

That's it! The `.env` file with API keys is already included.

---

## Manual API Key Setup (If Needed)

If you cloned the repo or the `.env` file is missing, you'll need to set up the API key manually:

### Option 1: Environment Variable (Claude Sandbox)

```bash
export GEMINI_API_KEY="your_actual_gemini_api_key_here"
python main.py --input your_content.txt --output infographic.png
```

### Option 2: .env File (Local Development)

```bash
echo "GEMINI_API_KEY=your_actual_gemini_api_key_here" > .env
python main.py --input your_content.txt --output infographic.png
```

### Getting Your Own API Key

1. Go to: https://aistudio.google.com/apikey
2. Click "Create API Key"
3. Copy your API key
4. Use it in one of the methods above

## Testing

```bash
# Set your API key first!
export GEMINI_API_KEY="your_key_here"

# Run test
python main.py --test
```

## Troubleshooting

### "GEMINI_API_KEY not found in environment"

**Solution**: You forgot to set the API key. See "Quick Setup" above.

### "ModuleNotFoundError"

**Solution**: Install dependencies first:

```bash
pip install -r requirements.txt
```

### "504 Deadline expired" or timeout errors

**Solution**: This is normal for the first run or slow connections. The skill has automatic retry logic (2 retries). Just wait, it can take 60-180 seconds total.

### Command fails in sandbox

**Solution**: Make sure you're passing the API key as an environment variable:

```bash
GEMINI_API_KEY="your_key" python main.py --input file.txt --output out.png
```

## File Structure

```
infographic/
├── main.py              # Main script
├── requirements.txt     # Python dependencies
├── SKILL.md            # Documentation
├── SETUP.md            # This file
├── .env.example        # Template for .env file
└── skill.yaml          # Skill configuration
```

## Dependencies

- Python 3.10+
- google-genai (Nano Banana Pro API)
- google-generativeai (Gemini API)
- pydantic (data validation)
- python-dotenv (environment variables)
- loguru (logging)

All dependencies install automatically via `pip install -r requirements.txt`
