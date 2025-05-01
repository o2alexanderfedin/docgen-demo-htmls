#!/usr/bin/env python3
import os
import re
import sys
import markdown
from pathlib import Path
import shutil
import concurrent.futures
import tempfile
import subprocess
import json
import base64
from bs4 import BeautifulSoup

# Install required packages if needed
try:
    from bs4 import BeautifulSoup
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "beautifulsoup4"])
    from bs4 import BeautifulSoup

def ensure_dir(directory):
    """Ensure directory exists; create if it doesn't."""
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)

def convert_internal_links(content, file_path, input_dir, output_dir):
    """Convert markdown links to HTML links."""
    # Pattern to match markdown links: [text](url)
    pattern = r'\[([^\]]+)\]\(([^)]+)\)'

    def replace_link(match):
        text, url = match.groups()
        
        # Handle external links or anchors
        if url.startswith(('http://', 'https://', 'mailto:')):
            return f'<a href="{url}" target="_blank" rel="noopener noreferrer">{text}</a>'
        
        # Handle anchor links
        if url.startswith('#'):
            return f'<a href="{url}">{text}</a>'
        
        # Handle relative paths
        current_dir = os.path.dirname(file_path)
        
        # Resolve the target path
        if url.startswith('/'):
            # Absolute path within the project
            target_path = os.path.normpath(os.path.join(input_dir, url.lstrip('/')))
        else:
            # Relative path
            target_path = os.path.normpath(os.path.join(current_dir, url))
        
        # Convert to output path
        rel_path = os.path.relpath(target_path, input_dir)
        output_path = os.path.join(output_dir, rel_path)
        
        # Change extension from .md to .html
        if output_path.endswith('.md'):
            output_path = output_path[:-3] + '.html'
        
        # Make the link relative to the current file's output location
        current_output_dir = os.path.dirname(file_path.replace(input_dir, output_dir))
        rel_url = os.path.relpath(output_path, current_output_dir)
        
        return f'<a href="{rel_url}">{text}</a>'
    
    return re.sub(pattern, replace_link, content)

def convert_file(file_path, input_dir, output_dir):
    """Convert a single markdown file to HTML."""
    rel_path = os.path.relpath(file_path, input_dir)
    output_path = os.path.join(output_dir, rel_path)
    output_path = output_path[:-3] + '.html'  # Change extension
    
    # Create output directory if it doesn't exist
    ensure_dir(os.path.dirname(output_path))
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Convert internal links
        content = convert_internal_links(content, file_path, input_dir, output_dir)
        
        # Convert markdown to HTML
        html = markdown.markdown(
            content,
            extensions=['extra', 'toc', 'tables', 'fenced_code']
        )
        
        # Add basic HTML structure
        html_doc = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>{os.path.basename(file_path)[:-3]}</title>
    <style>
        body {{ 
            font-family: Arial, sans-serif; 
            line-height: 1.6;
            margin: 0 auto;
            max-width: 900px;
            padding: 20px;
        }}
        pre {{ 
            background-color: #f6f8fa; 
            padding: 16px;
            border-radius: 6px;
            overflow: auto;
        }}
        code {{
            font-family: monospace;
            background-color: #f6f8fa;
            padding: 0.2em 0.4em;
            border-radius: 3px;
        }}
        pre code {{
            background-color: transparent;
            padding: 0;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
        }}
        table, th, td {{
            border: 1px solid #ddd;
        }}
        th, td {{
            padding: 8px;
            text-align: left;
        }}
        th {{
            background-color: #f2f2f2;
        }}
        img {{
            max-width: 100%;
        }}
    </style>
</head>
<body>
    {html}
</body>
</html>"""
        
        # Check for mermaid diagrams and convert them to SVG
        if 'class="language-mermaid"' in html_doc:
            print(f"Found mermaid diagrams in {file_path}, converting to SVG...")
            html_doc = convert_mermaid_to_svg(html_doc)
        
        # Write HTML to output file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_doc)
        
        print(f"Converted {file_path} to {output_path}")
        return True
    except Exception as e:
        print(f"Error converting {file_path}: {e}")
        return False

def copy_non_md_files(input_dir, output_dir):
    """Copy non-markdown files (like images) to the output directory."""
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if not file.endswith('.md'):
                src_path = os.path.join(root, file)
                rel_path = os.path.relpath(src_path, input_dir)
                dst_path = os.path.join(output_dir, rel_path)
                
                ensure_dir(os.path.dirname(dst_path))
                shutil.copy2(src_path, dst_path)
                print(f"Copied {src_path} to {dst_path}")

def install_mermaid_cli():
    """Install Mermaid CLI if not already installed."""
    try:
        # Check if Mermaid CLI is installed
        subprocess.run(['npx', '@mermaid-js/mermaid-cli/index.bundle.js', '--version'], 
                      check=True, capture_output=True)
        print("Mermaid CLI already installed")
    except:
        print("Installing Mermaid CLI...")
        subprocess.run(['npm', 'install', '@mermaid-js/mermaid-cli'], check=True)

def convert_mermaid_to_svg(html_content):
    """Convert mermaid code blocks to SVG."""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find all <pre><code class="language-mermaid"> blocks
    mermaid_blocks = soup.select('pre code.language-mermaid')
    
    if not mermaid_blocks:
        return html_content  # No mermaid diagrams found
    
    # Add mermaid CSS
    css_style = soup.new_tag('style')
    css_style.string = """
    .mermaid-svg {
        text-align: center;
        margin: 20px 0;
    }
    .mermaid-svg svg {
        max-width: 100%;
        height: auto;
    }
    """
    soup.head.append(css_style)
    
    # Process each mermaid diagram
    for i, code_block in enumerate(mermaid_blocks):
        pre_block = code_block.parent
        mermaid_code = code_block.get_text()
        
        try:
            # Create a temporary file for the mermaid code
            with tempfile.NamedTemporaryFile('w', suffix='.mmd', delete=False) as tmp:
                tmp.write(mermaid_code)
                tmp_path = tmp.name
            
            svg_output_path = tmp_path + '.svg'
            
            # Run mmdc (Mermaid CLI) to generate SVG
            subprocess.run([
                'npx', '@mermaid-js/mermaid-cli/index.bundle.js',
                '-i', tmp_path,
                '-o', svg_output_path,
                '-b', 'transparent'
            ], check=True)
            
            # Read the generated SVG
            with open(svg_output_path, 'r', encoding='utf-8') as svg_file:
                svg_content = svg_file.read()
            
            # Extract just the SVG content
            svg_match = re.search(r'<svg.*?</svg>', svg_content, re.DOTALL)
            if svg_match:
                svg_clean = svg_match.group(0)
                
                # Create a new div for the SVG
                mermaid_div = soup.new_tag('div')
                mermaid_div['class'] = 'mermaid-svg'
                mermaid_div['id'] = f'mermaid-diagram-{i+1}'
                mermaid_div.append(BeautifulSoup(svg_clean, 'html.parser'))
                
                # Replace the pre block with the SVG div
                pre_block.replace_with(mermaid_div)
                print(f"  - Converted mermaid diagram #{i+1}")
            
            # Clean up temporary files
            try:
                os.remove(tmp_path)
                if os.path.exists(svg_output_path):
                    os.remove(svg_output_path)
            except:
                pass
        except Exception as e:
            print(f"  - Error converting mermaid diagram #{i+1}: {str(e)}")
    
    return str(soup)

def main():
    """Main function to convert all markdown files."""
    input_dir = './input'
    output_dir = './output'
    
    if not os.path.exists(input_dir):
        print(f"Input directory {input_dir} does not exist.")
        sys.exit(1)
    
    ensure_dir(output_dir)
    
    # Install Mermaid CLI for diagram conversion
    install_mermaid_cli()
    
    # Get all markdown files
    md_files = []
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith('.md'):
                md_files.append(os.path.join(root, file))
    
    # Copy non-markdown files
    copy_non_md_files(input_dir, output_dir)
    
    # Convert markdown files in parallel
    success_count = 0
    total_count = len(md_files)
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(convert_file, file, input_dir, output_dir) for file in md_files]
        for future in concurrent.futures.as_completed(futures):
            if future.result():
                success_count += 1
    
    print(f"Conversion completed: {success_count}/{total_count} files converted successfully.")

if __name__ == "__main__":
    main()