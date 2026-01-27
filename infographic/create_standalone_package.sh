#!/bin/bash
# Create a standalone infographic skill package

echo "Creating standalone infographic skill package..."

# Create temporary directory
TEMP_DIR="infographic_skill_package"
rm -rf "$TEMP_DIR"
mkdir -p "$TEMP_DIR"

# Copy necessary files
cp main.py "$TEMP_DIR/"
cp requirements.txt "$TEMP_DIR/"
cp SKILL.md "$TEMP_DIR/"
cp SETUP.md "$TEMP_DIR/"
cp .env.example "$TEMP_DIR/"
cp README.md "$TEMP_DIR/"
cp skill.yaml "$TEMP_DIR/"

# Copy actual .env file with API keys if it exists
if [ -f ".env" ]; then
    cp .env "$TEMP_DIR/"
    echo "✓ Including .env file with API keys (GEMINI_API_KEY configured)"
else
    echo "⚠️  Warning: .env file not found, users will need to add their own API key"
fi

# Create ready-to-use README
cat > "$TEMP_DIR/README_START_HERE.md" << 'EOFREADME'
# 🎨 Infographic Skill - Ready to Use!

## ✨ API Keys Already Included!

This package is **100% ready to use** - API keys are already configured in the `.env` file.

## Quick Start (3 Commands)

```bash
# 1. Install dependencies (one time only)
pip install -r requirements.txt

# 2. Test it
python main.py --test

# 3. Generate your infographic
python main.py --input your_content.txt --output infographic.png
```

## Expected Output

When you run `python main.py --test`, you should see:

```
============================================================
INFOGRAPHIC GENERATION STARTED
============================================================
Step 1/2: Analyzing content structure...
✓ Structure extracted: 'Quantum Computing Revolution'
Step 2/2: Generating infographic image with Nano Banana Pro...
✓ Infographic saved: test_infographic.png (245.3 KB)
============================================================
✓ INFOGRAPHIC GENERATION COMPLETED in 63.7s
============================================================
```

This takes 60-180 seconds (normal for AI image generation).

## Features

✅ Horizontal layout with 4-5 sections arranged left-to-right
✅ Minimal text (70% visual, 30% text)
✅ Professional diagrams and illustrations
✅ Color-coded sections
✅ Automatic retries on timeout
✅ Progress indicators

## Documentation

- **START HERE**: This file
- **SETUP.md**: Detailed setup and troubleshooting
- **SKILL.md**: Complete documentation and examples

## Troubleshooting

**Problem**: `ModuleNotFoundError: No module named 'pydantic'`
**Solution**: Run `pip install -r requirements.txt` first

**Problem**: Takes a long time (60-180 seconds)
**Solution**: This is normal! AI image generation is computationally intensive

**Problem**: `504 Deadline expired`
**Solution**: Wait for automatic retry (up to 2 retries built-in)

## Support

GitHub: https://github.com/serenakeyitan/nblm-skills
EOFREADME

# Create a setup script
cat > "$TEMP_DIR/setup.sh" << 'EOF'
#!/bin/bash
# Setup script for infographic skill

echo "Setting up Infographic Skill..."
echo ""

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed"
    exit 1
fi

echo "✓ Python 3 found"

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -q -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✓ Dependencies installed successfully"
else
    echo "❌ Error: Failed to install dependencies"
    exit 1
fi

# Check for API key
echo ""
if [ -z "$GEMINI_API_KEY" ] && [ ! -f ".env" ]; then
    echo "⚠️  WARNING: GEMINI_API_KEY not found!"
    echo ""
    echo "You need to set your Gemini API key before using this skill."
    echo ""
    echo "Option 1: Create .env file (recommended for local use)"
    echo "  echo 'GEMINI_API_KEY=your_key_here' > .env"
    echo ""
    echo "Option 2: Set environment variable (recommended for sandbox)"
    echo "  export GEMINI_API_KEY='your_key_here'"
    echo ""
    echo "Get your API key at: https://aistudio.google.com/apikey"
    echo ""
else
    echo "✓ API key configuration found"
fi

echo ""
echo "✓ Setup complete!"
echo ""
echo "To test:"
echo "  python main.py --test"
echo ""
echo "To generate an infographic:"
echo "  python main.py --input your_content.txt --output infographic.png"
echo ""
echo "For more information, see SETUP.md"
EOF

chmod +x "$TEMP_DIR/setup.sh"

# Create README for the package
cat > "$TEMP_DIR/README_PACKAGE.md" << 'EOF'
# Infographic Skill - Standalone Package

Generate professional horizontal infographics using Nano Banana Pro (Gemini 3 Pro Image).

## Quick Start

1. **Run setup script:**
   ```bash
   bash setup.sh
   ```

2. **Set your Gemini API key:**
   ```bash
   export GEMINI_API_KEY="your_actual_api_key_here"
   ```

   Or create a `.env` file:
   ```bash
   echo "GEMINI_API_KEY=your_actual_api_key_here" > .env
   ```

3. **Test it:**
   ```bash
   python main.py --test
   ```

4. **Generate infographic:**
   ```bash
   python main.py --input your_content.txt --output infographic.png
   ```

## Get API Key

Get your free Gemini API key at: https://aistudio.google.com/apikey

## Documentation

- `SETUP.md` - Detailed setup instructions and troubleshooting
- `SKILL.md` - Skill documentation and usage examples
- `README.md` - Original README

## Support

This is part of the NotebookLM Skills Suite.
Repository: https://github.com/serenakeyitan/nblm-skills
EOF

# Create ZIP archive
ZIP_NAME="infographic_skill_standalone.zip"
rm -f "$ZIP_NAME"
cd "$TEMP_DIR"
zip -r "../$ZIP_NAME" . > /dev/null
cd ..

# Cleanup
rm -rf "$TEMP_DIR"

echo "✓ Package created: $ZIP_NAME"
echo ""
echo "This package includes:"
echo "  - All Python code (main.py)"
echo "  - Dependencies list (requirements.txt)"
echo "  - Setup script (setup.sh)"
echo "  - Documentation (SETUP.md, SKILL.md, README.md)"
echo "  - Example .env file (.env.example)"
echo ""
echo "Users need to:"
echo "  1. Unzip the package"
echo "  2. Run: bash setup.sh"
echo "  3. Set their GEMINI_API_KEY"
echo "  4. Run: python main.py --test"
