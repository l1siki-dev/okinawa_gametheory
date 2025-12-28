import os
import re

# Global variable to store the file list
# (because on_page_read_source doesn't provide it)
STORED_FILES = []

def on_files(files, config):
    """
    Step 1: Capture all files before processing starts.
    """
    global STORED_FILES
    STORED_FILES = files
    return files

def on_page_read_source(page, config):
    """
    Step 2: Rewrite index.md source BEFORE macros are rendered.
    """
    # Only run on index.md
    if page.file.src_path != 'index.md':
        return None # None tells MkDocs to read the file normally

    docs_dir = config['docs_dir']
    dashboard_items = []
    toc_lines = []
    
    # Sort files
    sorted_files = sorted(STORED_FILES, key=lambda f: f.src_path)
    
    for f in sorted_files:
        if f.src_path == 'index.md': continue
        if not f.src_path.endswith('.md'): continue
            
        file_path = os.path.join(docs_dir, f.src_path)
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors="ignore") as open_file:
                content = open_file.read()
        except Exception:
            continue

        # --- A. Extract Title Manually ---
        # f.page is None at this stage, so we grab the first H1 (# Title)
        page_title = f.name # Fallback
        h1_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if h1_match:
            page_title = h1_match.group(1).strip()

        # --- B. Build TOC ---
        toc_lines.append(f"- [{page_title}]({f.url})")
        
        # --- C. Extract Charts ---
        chart_matches = re.findall(r"\{\{\s*viral_chart\s*\(\s*['\"](.*?)['\"]\s*,\s*([^,\)]+)(.*?)\)\s*\}\}", content)
        
        for (chart_id, var_name, extra_args) in chart_matches:
            home_id = f"home_{chart_id}"
            
            injected_macro = f"""
<div class="grid-item">
    <div class="homepage-chart-wrapper">
        {{{{ viral_chart('{home_id}', {var_name}{extra_args}) }}}}
        <p class="caption">
            <a href="{f.url}">View full size in: {page_title}</a>
        </p>
    </div>
</div>
"""
            dashboard_items.append(injected_macro)

    # --- D. Inject into Source ---
    full_toc = "\n".join(toc_lines)
    full_dashboard = '<div class="grid cards" markdown>\n' + "\n".join(dashboard_items) + "\n</div>"
    
    # Since we are in on_page_read_source, we must
