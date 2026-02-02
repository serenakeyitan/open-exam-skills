"""
Mind Map Skill - Convert Markdown to interactive mind maps using Markmap
Pure frontend conversion - no LLM required
"""

import argparse
import os
import subprocess
import sys
import re
import shutil
from pathlib import Path
from loguru import logger

logger.remove()
logger.add(sys.stderr, level="INFO")


def inject_custom_features(html_path: str) -> None:
    """Inject custom JavaScript for default collapse and export functionality."""

    logger.info("Injecting custom features...")

    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Custom JavaScript to add features
    custom_script = """
<style>
  #control-panel {
    position: fixed;
    top: 20px;
    right: 20px;
    z-index: 1000;
    background: white;
    padding: 12px 16px;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.15);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    display: flex;
    flex-direction: column;
    gap: 8px;
  }

  #control-panel button {
    background: #4285f4;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 14px;
    font-weight: 500;
    transition: background 0.2s;
    white-space: nowrap;
  }

  #control-panel button:hover {
    background: #3367d6;
  }

  #control-panel button:active {
    background: #2851a3;
  }

  #control-panel button:disabled {
    background: #ccc;
    cursor: not-allowed;
  }

  .node-circle {
    cursor: pointer;
  }

  #prompt-display {
    position: fixed;
    bottom: 20px;
    left: 20px;
    right: 20px;
    max-width: 600px;
    background: #f8f9fa;
    border: 1px solid #dadce0;
    border-radius: 8px;
    padding: 16px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.15);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    display: none;
    z-index: 1000;
  }

  #prompt-display.show {
    display: block;
  }

  #prompt-text {
    margin: 8px 0;
    padding: 12px;
    background: white;
    border-radius: 4px;
    font-size: 14px;
    line-height: 1.5;
    color: #202124;
  }

  #prompt-actions {
    display: flex;
    gap: 8px;
    margin-top: 12px;
  }

  #prompt-actions button {
    background: #4285f4;
    color: white;
    border: none;
    padding: 6px 12px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 13px;
    font-weight: 500;
  }

  #prompt-actions button:hover {
    background: #3367d6;
  }

  #prompt-actions .close-btn {
    background: #5f6368;
  }

  #prompt-actions .close-btn:hover {
    background: #3c4043;
  }
</style>

<div id="control-panel">
  <button id="export-png-btn">Export PNG</button>
  <button id="export-html-btn">Export HTML</button>
</div>

<div id="prompt-display">
  <div style="font-weight: 600; color: #5f6368; font-size: 12px; text-transform: uppercase;">Generated Prompt</div>
  <div id="prompt-text"></div>
  <div id="prompt-actions">
    <button id="copy-prompt-btn">Copy to Clipboard</button>
    <button class="close-btn" id="close-prompt-btn">Close</button>
  </div>
</div>

<script>
(function() {
  // Set up export functions immediately - they'll wait for dependencies when called
  const mm = window.markmap;

    function collectInlineStyles() {
      const styles = [];
      document.querySelectorAll('style').forEach(style => {
        if (style.textContent) {
          styles.push(style.textContent);
        }
      });
      return styles.join('\\n');
    }

    function downloadDataUrl(dataUrl, filename) {
      const link = document.createElement('a');
      link.href = dataUrl;
      link.download = filename;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }

    // Collapse to first level only on load
    function collapseToFirstLevel() {
      const svg = document.querySelector('svg');
      if (!svg) return;

      const allNodes = svg.querySelectorAll('g[data-depth]');
      allNodes.forEach(node => {
        const depth = parseInt(node.getAttribute('data-depth'));
        // Collapse everything except root (depth 0) and first level (depth 1)
        if (depth > 1) {
          const circle = node.querySelector('circle');
          if (circle && circle.classList.contains('markmap-node')) {
            // Trigger collapse by simulating click
            const nodeData = node.__data__;
            if (nodeData && nodeData.children && nodeData.p) {
              nodeData.p = nodeData.children;
              delete nodeData.children;
            }
          }
        }
      });

      // Force redraw if markmap instance is available
      if (mm && mm.Markmap) {
        const svg = document.querySelector('svg');
        if (svg && svg.__markmap) {
          svg.__markmap.fit();
        }
      }
    }

    function svgToDataUrl(svgString) {
      const encoded = btoa(unescape(encodeURIComponent(svgString)));
      return `data:image/svg+xml;base64,${encoded}`;
    }

    // Export as PNG - Render SVG to canvas
    async function exportPNG() {
      const btn = document.getElementById('export-png-btn');
      if (!btn) {
        console.error('Export PNG button not found');
        return;
      }
      
      const originalText = btn.textContent;
      btn.disabled = true;
      btn.textContent = 'Exporting...';

      try {
        const svg = document.querySelector('svg');
        if (!svg) {
          throw new Error('SVG not found. Please wait for the mindmap to load.');
        }

        const clonedSvg = svg.cloneNode(true);
        const inlineStyles = collectInlineStyles();
        if (inlineStyles) {
          const styleEl = document.createElementNS('http://www.w3.org/2000/svg', 'style');
          styleEl.textContent = inlineStyles;
          clonedSvg.insertBefore(styleEl, clonedSvg.firstChild);
        }

        let bbox;
        try {
          bbox = svg.getBBox();
        } catch (e) {
          const viewBox = svg.getAttribute('viewBox');
          if (viewBox) {
            const parts = viewBox.split(/\\s+/);
            bbox = {
              x: parseFloat(parts[0]) || 0,
              y: parseFloat(parts[1]) || 0,
              width: parseFloat(parts[2]) || svg.clientWidth || 800,
              height: parseFloat(parts[3]) || svg.clientHeight || 600
            };
          } else {
            bbox = {
              x: 0,
              y: 0,
              width: svg.clientWidth || 800,
              height: svg.clientHeight || 600
            };
          }
        }

        clonedSvg.setAttribute('viewBox', `${bbox.x} ${bbox.y} ${bbox.width} ${bbox.height}`);
        clonedSvg.setAttribute('width', bbox.width);
        clonedSvg.setAttribute('height', bbox.height);
        if (!clonedSvg.getAttribute('xmlns')) {
          clonedSvg.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
        }
        if (!clonedSvg.getAttribute('xmlns:xlink')) {
          clonedSvg.setAttribute('xmlns:xlink', 'http://www.w3.org/1999/xlink');
        }

        const serializer = new XMLSerializer();
        const svgString = serializer.serializeToString(clonedSvg);
        const svgDataUrl = svgToDataUrl(svgString);

        const img = new Image();
        await new Promise((resolve, reject) => {
          img.onload = resolve;
          img.onerror = () => reject(new Error('Failed to load SVG image'));
          img.src = svgDataUrl;
        });

        const scale = 2;
        const canvas = document.createElement('canvas');
        canvas.width = Math.ceil(bbox.width * scale);
        canvas.height = Math.ceil(bbox.height * scale);
        const ctx = canvas.getContext('2d');
        ctx.fillStyle = '#ffffff';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.scale(scale, scale);
        ctx.drawImage(img, 0, 0, bbox.width, bbox.height);

        let dataUrl;
        try {
          dataUrl = canvas.toDataURL('image/png');
        } catch (canvasError) {
          const msg = String(canvasError || '');
          if (msg.toLowerCase().includes('insecure')) {
            throw new Error('PNG export blocked by browser security. Please open the HTML via a local web server (e.g. python -m http.server) and try again.');
          }
          throw canvasError;
        }

        downloadDataUrl(dataUrl, 'mindmap.png');

        btn.textContent = 'Exported!';
        setTimeout(function() {
          btn.textContent = originalText;
          btn.disabled = false;
        }, 2000);
      } catch (error) {
        console.error('PNG export error:', error);
        const errorMsg = error && error.message ? error.message : (typeof error === 'string' ? error : 'Unknown error occurred');
        alert('Export failed: ' + errorMsg);
        btn.textContent = 'Error';
        setTimeout(function() {
          btn.textContent = originalText;
          btn.disabled = false;
        }, 2000);
      }
    }

    // Export as HTML - Save current page as HTML file
    function exportHTML() {
      const btn = document.getElementById('export-html-btn');
      if (!btn) {
        console.error('Export HTML button not found');
        return;
      }
      
      const originalText = btn.textContent;
      btn.disabled = true;
      btn.textContent = 'Exporting...';

      try {
        const html = '<!DOCTYPE html>\\n' + document.documentElement.outerHTML;
        const dataUrl = 'data:text/html;charset=utf-8,' + encodeURIComponent(html);
        downloadDataUrl(dataUrl, 'mindmap.html');

        btn.textContent = 'Exported!';
        setTimeout(function() {
          btn.textContent = originalText;
          btn.disabled = false;
        }, 2000);
      } catch (error) {
        console.error('HTML export error:', error);
        const errorMsg = error && error.message ? error.message : (typeof error === 'string' ? error : 'Unknown error occurred');
        alert('Export failed: ' + errorMsg);
        btn.textContent = 'Error';
        setTimeout(function() {
          btn.textContent = originalText;
          btn.disabled = false;
        }, 2000);
      }
    }

    // Add click handlers for export buttons - attach immediately
    function attachExportHandlers() {
      const pngBtn = document.getElementById('export-png-btn');
      const htmlBtn = document.getElementById('export-html-btn');
      
      if (pngBtn && !pngBtn.dataset.listenerAttached) {
        pngBtn.addEventListener('click', exportPNG);
        pngBtn.dataset.listenerAttached = 'true';
      }
      
      if (htmlBtn && !htmlBtn.dataset.listenerAttached) {
        htmlBtn.addEventListener('click', exportHTML);
        htmlBtn.dataset.listenerAttached = 'true';
      }
    }
    
    // Try to attach immediately
    attachExportHandlers();
    
    // Also try after a short delay in case buttons aren't ready yet
    setTimeout(attachExportHandlers, 100);
    setTimeout(attachExportHandlers, 500);

    // Node click handler to show prompt
    const promptDisplay = document.getElementById('prompt-display');
    const promptText = document.getElementById('prompt-text');

    function showPrompt(nodeText) {
      const prompt = `讨论这些来源关于「${nodeText}」相关的内容`;
      promptText.textContent = prompt;
      promptDisplay.classList.add('show');

      // Store prompt for copying
      promptDisplay.dataset.prompt = prompt;
    }

    // Copy to clipboard
    document.getElementById('copy-prompt-btn').addEventListener('click', function() {
      const prompt = promptDisplay.dataset.prompt;
      navigator.clipboard.writeText(prompt).then(function() {
        const btn = document.getElementById('copy-prompt-btn');
        const originalText = btn.textContent;
        btn.textContent = 'Copied!';
        setTimeout(function() {
          btn.textContent = originalText;
        }, 2000);
      });
    });

    // Close prompt display
    document.getElementById('close-prompt-btn').addEventListener('click', function() {
      promptDisplay.classList.remove('show');
    });

    // Add click listeners to node text (not the expand/collapse circles)
    setTimeout(function() {
      const svg = document.querySelector('svg');
      if (!svg) return;

      // Listen for clicks on text elements
      svg.addEventListener('click', function(e) {
        // Check if click is on text, not on circle
        if (e.target.tagName === 'text' || e.target.tagName === 'tspan') {
          const textElement = e.target.tagName === 'text' ? e.target : e.target.parentElement;
          const nodeText = textElement.textContent.trim();

          // Don't show prompt for root node (usually at depth 0)
          const nodeGroup = textElement.closest('g[data-depth]');
          if (nodeGroup) {
            const depth = parseInt(nodeGroup.getAttribute('data-depth'));
            if (depth > 0) {
              showPrompt(nodeText);
              e.stopPropagation();
            }
          }
        }
      });
    }, 500);

    // Initial collapse to first level - wait for SVG to be ready
    function tryCollapse() {
      const svg = document.querySelector('svg');
      if (svg) {
        collapseToFirstLevel();
      } else {
        setTimeout(tryCollapse, 100);
      }
    }
    setTimeout(tryCollapse, 100);

})(); // End of IIFE
</script>
"""

    # Insert custom script before closing body tag
    html_content = html_content.replace('</body>', f'{custom_script}</body>')

    # Write modified HTML back
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    logger.info("✓ Custom features injected")


def get_markmap_command() -> list[str]:
    """Find a local markmap-cli command or fall back to npx."""

    markmap_bin = shutil.which("markmap")
    if markmap_bin:
        return [markmap_bin]

    npm_cache = Path.home() / '.npm' / '_npx'
    if npm_cache.exists():
        candidates = list(npm_cache.glob('*/node_modules/markmap-cli/bin/cli.js'))
        if candidates:
            latest = max(candidates, key=lambda path: path.stat().st_mtime)
            node_bin = shutil.which('node') or 'node'
            return [node_bin, str(latest)]

    return ['npx', '-y', 'markmap-cli']


def ensure_katex_fonts(html_path: str) -> None:
    """Copy KaTeX fonts next to the output HTML if needed."""

    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    if 'katex' not in html_content or 'fonts/KaTeX_' not in html_content:
        return

    output_dir = Path(html_path).resolve().parent
    fonts_dir = output_dir / 'fonts'

    npm_cache = Path.home() / '.npm' / '_npx'
    if not npm_cache.exists():
        logger.warning("KaTeX fonts not copied: npm cache not found")
        return

    font_paths = list(npm_cache.glob('*/node_modules/markmap-cli/dist/assets/katex@*/dist/fonts'))
    if not font_paths:
        logger.warning("KaTeX fonts not copied: markmap-cli assets not found")
        return

    source_fonts = max(font_paths, key=lambda path: path.stat().st_mtime)
    fonts_dir.mkdir(parents=True, exist_ok=True)

    for font_file in source_fonts.glob('*'):
        if font_file.is_file():
            shutil.copy2(font_file, fonts_dir / font_file.name)

    logger.info(f"✓ KaTeX fonts copied to: {fonts_dir}")


def convert_markdown_to_mindmap(markdown_path: str, output_path: str) -> str:
    """Convert Markdown file to interactive HTML mind map using markmap-cli."""

    logger.info("=" * 60)
    logger.info("MIND MAP CONVERSION STARTED")
    logger.info("=" * 60)

    # Verify input file exists
    if not os.path.exists(markdown_path):
        raise FileNotFoundError(f"Input file not found: {markdown_path}")

    # Read markdown to verify it's not empty
    with open(markdown_path, 'r', encoding='utf-8') as f:
        markdown_content = f.read()

    if not markdown_content.strip():
        raise ValueError(f"Input file is empty: {markdown_path}")

    logger.info(f"Input: {markdown_path} ({len(markdown_content)} chars)")
    logger.info(f"Output: {output_path}")
    logger.info("Converting Markdown to interactive HTML using Markmap...")

    try:
        markmap_cmd = get_markmap_command()
        cmd = [
            *markmap_cmd,
            '--offline',  # Include all assets for offline viewing
            markdown_path,
            '-o', output_path
        ]

        logger.info(f"Running: {' '.join(cmd)}")

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60
        )

        if result.returncode != 0:
            logger.error(f"markmap-cli error: {result.stderr}")
            raise RuntimeError(f"Failed to generate HTML: {result.stderr}")

        if not os.path.exists(output_path):
            raise FileNotFoundError(f"Output file not created: {output_path}")

        # Inject custom features
        inject_custom_features(output_path)
        ensure_katex_fonts(output_path)

        file_size = os.path.getsize(output_path) / 1024

        logger.info("=" * 60)
        logger.info(f"✓ CONVERSION COMPLETED")
        logger.info(f"✓ Interactive mind map saved: {output_path} ({file_size:.1f} KB)")
        logger.info("=" * 60)

        return output_path

    except subprocess.TimeoutExpired:
        logger.error("Conversion timed out after 60 seconds")
        raise RuntimeError("Conversion timed out")
    except Exception as e:
        logger.error("=" * 60)
        logger.error("✗ CONVERSION FAILED")
        logger.error(f"Error: {type(e).__name__}: {str(e)}")
        logger.error("=" * 60)
        raise


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Convert Markdown to interactive mind maps using Markmap"
    )
    parser.add_argument(
        "--input", "-i",
        required=True,
        help="Input Markdown file path"
    )
    parser.add_argument(
        "--output", "-o",
        default="mindmap.html",
        help="Output HTML file path (default: mindmap.html)"
    )

    args = parser.parse_args()

    try:
        result = convert_markdown_to_mindmap(args.input, args.output)

        if os.path.exists(result):
            size = os.path.getsize(result) / 1024
            print(f"✓ Mind map created: {result} ({size:.1f} KB)")
            print(f"✓ Open in browser: file://{os.path.abspath(result)}")
            print()
            print("Features:")
            print("  • Export as PNG or HTML using buttons in top-right")
            print("  • Click node text to generate discussion prompt")
            print("  • Click branch circles to expand/collapse")
        else:
            print(f"✗ Error: File not created at {result}")
            sys.exit(1)

    except KeyboardInterrupt:
        print("\n✗ Conversion cancelled by user")
        sys.exit(130)
    except Exception as e:
        print(f"✗ Error: {type(e).__name__}: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
