---
name: mindmap
description: Create interactive mind maps from notes or outlines.
---

# Mind Map

Convert Markdown files to interactive HTML mind maps with enhanced features. Uses official Markmap frontend with custom controls.

## What This Skill Does

**Input**: Markdown file with heading hierarchy (# ## ### ####)
**Output**: Interactive HTML with enhanced features

This is a **pure converter** - no LLM required. Agent generates Markdown → this skill converts to interactive HTML.

## Output Contract

- Produces a self-contained HTML file with the interactive mind map.
- Export controls allow users to download PNG and HTML versions from the UI.

## Enhanced Features

### 1. Smart Default Collapse
- Opens with **only first level visible** (minimalist view)
- Users can manually expand nodes one-by-one
- Reduces cognitive load on complex maps

### 2. Export Functionality
- **Export PNG** button: Export mindmap as high-quality PNG image
- **Export HTML** button: Export the current page as a standalone HTML file
- Both buttons located in top-right control panel
- Downloads automatically to your default download folder

### 3. Click-to-Discuss
- Click any node's **text** (not the branch circle)
- Generates discussion prompt: "讨论这些来源关于「[node title]」相关的内容"
- Appears in bottom panel with:
  - **Copy to Clipboard** button
  - **Close** button
- Clicking branch circles only expands/collapses (no prompt)

### 4. Markmap Standard Features
- Zoom with mouse wheel
- Pan by dragging
- Click circles to expand/collapse
- Responsive design
- Offline support (all assets embedded)

## Workflow

```
1. Ask Claude: "Generate a mind map about X in Markdown format"
2. Claude creates Markdown with # ## ### #### hierarchy
3. Save to file (e.g., mindmap.md)
4. Run from `skills/mindmap`: `python main.py -i mindmap.md -o mindmap.html`
5. Open HTML → interact with enhanced mind map
```

## Usage

```bash
cd skills/mindmap
python main.py --input mindmap.md --output mindmap.html
```

Parameters:
- `--input`, `-i`: Input Markdown file (required)
- `--output`, `-o`: Output HTML file (default: mindmap.html)

## Example Markdown Format

```markdown
# Main Topic

## First Branch

### Subtopic 1.1

#### Detail 1.1.1

#### Detail 1.1.2

### Subtopic 1.2

## Second Branch

### Subtopic 2.1
```

## User Interactions

| Action | Behavior |
|--------|----------|
| Click "Export PNG" button | Downloads mindmap as PNG image |
| Click "Export HTML" button | Downloads current mindmap page as HTML |
| Click node **text** | Shows discussion prompt at bottom |
| Click node **circle** | Expands/collapses that branch only |
| Mouse wheel | Zoom in/out |
| Drag background | Pan the view |
| Click "Copy" in prompt panel | Copies prompt to clipboard |

## Generated HTML Structure

```html
<!DOCTYPE html>
<html>
  <head>
    <!-- Markmap CSS/JS (embedded) -->
  </head>
  <body>
    <!-- SVG mind map -->
    <!-- Export buttons (top-right) -->
    <!-- Prompt panel (bottom, hidden by default) -->
    <!-- Custom JavaScript for features -->
  </body>
</html>
```

## Technical Details

- **No LLM/AI**: Pure Markdown → HTML conversion
- **No API Keys**: No external API calls
- **Frontend**: Official Markmap library + custom enhancements
- **Default State**: Collapsed to level 1
- **Export**: PNG (SVG render via canvg) and HTML (full page)
- **Prompt Format**: Chinese template (customizable in code)

## Dependencies

### Python
```bash
pip install -r requirements.txt
```
Only requires: `loguru` (logging)

### System
- **Node.js/npx**: For markmap-cli
- Auto-downloads on first use: `npx -y markmap-cli`

## Customization

To change the prompt format, edit `main.py` line 204:
```python
const prompt = `Discuss what these sources say about「${nodeText}`, in hte larger context of the upper node of the ${nodeText}`;
```

Replace with your preferred template, e.g.:
```python
const prompt = `Discuss content from sources about "${nodeText}"`;
```

## Integration with Agent

When asking Agent to generate mind maps:
1. Request heading-only format (# ## ### ####)
2. No bullet points or numbered lists
3. Keep headings concise (3-8 words)

Then convert:
```bash
cd skills/mindmap
python main.py -i agent_output.md -o mindmap.html
```

Open `mindmap.html` in any browser for full interaction.
