# Infographic Skill - Ready to Use!

## 🎉 No Configuration Needed!

This package includes everything you need, including API keys. Just install and run!

## Quick Start (3 Steps)

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

Or use the setup script:

```bash
bash setup.sh
```

### 2. Test It

```bash
python main.py --test
```

You should see:
```
============================================================
INFOGRAPHIC GENERATION STARTED
============================================================
Step 1/2: Analyzing content structure...
Content analysis completed in 18.5s
✓ Structure extracted: 'Quantum Computing Revolution'
✓ Sections: 5
Step 2/2: Generating infographic image with Nano Banana Pro...
Image generation completed in 45.2s
✓ Infographic saved: test_infographic.png (245.3 KB)
============================================================
✓ INFOGRAPHIC GENERATION COMPLETED in 63.7s
============================================================
```

### 3. Generate Your Infographic

```bash
python main.py --input your_content.txt --output infographic.png
```

## That's It! 🚀

The `.env` file with API keys is already included in this package, so you don't need to configure anything.

## Examples

### Generate from text file
```bash
python main.py --input research.txt --output research_infographic.png
```

### Generate from clipboard (if you have a file)
```bash
echo "Your content here..." > content.txt
python main.py --input content.txt --output output.png
```

## Features

- ✅ **Horizontal Layout**: Professional landscape-oriented infographics
- ✅ **Minimal Text**: 70% visual, 30% text for maximum impact
- ✅ **AI-Powered**: Uses Nano Banana Pro (Gemini 3 Pro Image)
- ✅ **Automatic Retries**: Built-in retry logic for reliability
- ✅ **Progress Indicators**: Clear step-by-step progress
- ✅ **Professional Design**: Educational/scientific style with color-coded sections

## Troubleshooting

### "ModuleNotFoundError"
**Solution**: Install dependencies first:
```bash
pip install -r requirements.txt
```

### Generation takes long (60-180 seconds)
**Solution**: This is normal! The skill makes two AI calls (analysis + image generation). Be patient, it has automatic retries.

### "504 Deadline expired"
**Solution**: The automatic retry will kick in. Just wait, it will retry up to 2 times.

## Files Included

- `main.py` - Main script
- `requirements.txt` - Python dependencies
- `.env` - **API keys (already configured!)**
- `SETUP.md` - Detailed setup guide
- `SKILL.md` - Full documentation
- `setup.sh` - Automated setup script

## Support

Part of the NotebookLM Skills Suite
- GitHub: https://github.com/serenakeyitan/nblm-skills
- Issues: https://github.com/serenakeyitan/nblm-skills/issues
