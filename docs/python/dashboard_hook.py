import os
import re

def on_page_markdown(markdown, page, config, files):
    # Only run this logic on the homepage (index.md)
    if page.file.src_path != 'index.md':
        return markdown

    # --- 1. SETUP VARIABLES ---
    docs_dir = config['docs_dir']
    charts_html = []
    toc_lines = []
    
    # Sort files by path to ensure logical order (Analysis -> Solution -> Notes)
    # We filter out index.md itself to avoid self-reference loop
    sorted_files = sorted(files, key=lambda f: f.src_path)
    
    # --- 2. SCAN FILES ---
    for f in sorted_files:
        if f.src_path == 'index.md':
            continue
            
        # Read the file content
        file_path = os.path.join(docs_dir, f.src_path)
        with open(file_path, 'r', encoding='utf-8') as open_file:
            content = open_file.read()

        # --- A. BUILD GLOBAL TOC ---
        # Find H1 (#) and H2 (##)
        # We assume H1 is the Chapter Title
        lines = content.split('\n')
        for line in lines:
            if line.startswith('# '):
                title = line.replace('# ', '').strip()
                link = f.url
                toc_lines.append(f"- [{title}]({link})")
            elif line.startswith('## '):
                sub_title = line.replace('## ', '').strip()
                # Create anchor link (MkDocs default slugify logic is simple, usually lowercase + hyphens)
                # Note: This is a rough approximation. For perfect anchors, more logic is needed.
                anchor = sub_title.lower().replace(' ', '-').replace('?', '').replace(':', '')
                link = f"{f.url}#{anchor}"
                toc_lines.append(f"    - [{sub_title}]({link})")

        # --- B. EXTRACT CHARTS ---
        # Regex to find ```echarts block
        # We capture the content inside
        charts = re.findall(r'```echarts(.*?)```', content, re.DOTALL)
        
        for i, chart_json in enumerate(charts):
            # Create a card for the chart
            # We wrap it in a div that fits the grid
            chart_card = f"""
<div class="grid-item">
<div class="chart-container">

```echarts
{chart_json}
