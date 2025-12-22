import json
import textwrap
import os
import re
import glob

def define_env(env):
    """
    This is the hook for defining variables, macros and filters
    """

    # --------------------------------------------------------------------------
    # 1. DEFINE YOUR DATA VARIABLES HERE
    # --------------------------------------------------------------------------
    # Example data (Replace this with your real data loading logic)
    # env.variables.test2 = { ... } 
    
    # If your data is dense, ensure it is loaded into env.variables 
    # so the dashboard macro can access it by name.

    # --------------------------------------------------------------------------
    # 2. THE CHART GENERATOR (Used by both chapters and dashboard)
    # --------------------------------------------------------------------------
    @env.macro
    def viral_chart(id, options, height="800px"):
        """
        Generates the HTML for an EChart.
        args:
            id: Unique string ID for the div
            options: Dictionary containing ECharts option data
            height: CSS height string (default 800px)
        """
        json_options = json.dumps(options)
        
        # SVG Icon for the share button
        icon_share = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path fill="currentColor" d="M18 16.08c-.76 0-1.44.3-1.96.77L8.91 12.7c.05-.23.09-.46.09-.7s-.04-.47-.09-.7l7.05-4.11c.54.5 1.25.81 2.04.81a3 3 0 0 0 3-3 3 3 0 0 0-3-3 3 3 0 0 0-3 3c0 .24.04.47.09.7L8.04 9.81C7.5 9.31 6.79 9 6 9a3 3 0 0 0-3 3 3 3 0 0 0 3 3c.79 0 1.5-.31 2.04-.81l7.12 4.15c-.05.21-.08.43-.08.66 0 1.61 1.31 2.91 2.92 2.91s2.92-1.3 2.92-2.91a2.92 2.92 0 0 0-2.92-2.91"/></svg>'

        # The HTML Structure
        # We use the 'height' argument here to allow resizing
        html = f"""
        <div class="chart-wrapper" style="position: relative; width: 100%; overflow-x: auto; margin: 2em auto; border: 1px solid var(--md-default-fg-color--lightest); border-radius: 8px; background: #fff;">
            
            <div style="position: absolute; top: 10px; left: 10px; z-index: 10; display: flex; gap: 10px;">
                <button class="share-button chart-action-btn" onclick="shareChart('{id}')" title="Share Chart">
                    {icon_share}
                </button>
            </div>
            
            <div id="{id}" class="lazy-chart" style="width: 100%; height: {height};"></div>
        </div>

        <script>
            window.osintChartData = window.osintChartData || {{}};
            window.osintChartData['{id}'] = {json_options};
        </script>
        """
        return textwrap.dedent(html)

    # --------------------------------------------------------------------------
    # 3. THE DASHBOARD GENERATOR (Home Page Only)
    # --------------------------------------------------------------------------
    @env.macro
    def render_dashboard():
        """
        Scans all markdown files, finds 'viral_chart' calls, 
        and re-renders them as mini-charts for the index.md grid.
        """
        docs_dir = env.conf['docs_dir']
        dashboard_items = []
        
        # Recursively find all .md files and sort them
        md_files = sorted(glob.glob(os.path.join(docs_dir, '**', '*.md'), recursive=True))

        for file_path in md_files:
            filename = os.path.basename(file_path)
            
            # Skip the homepage itself to avoid infinite recursion
            if filename == 'index.md' and os.path.dirname(file_path) == docs_dir:
                continue

            # Read file content
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            except Exception as e:
                print(f"Skipping {filename}: {e}")
                continue

            # A. Get Page Title (First H1)
            page_title = filename
            h1 = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
            if h1:
                page_title = h1.group(1).strip()

            # B. Get URL for linking
            rel_path = os.path.relpath(file_path, docs_dir).replace('\\', '/')
            if rel_path.endswith('index.md'):
                url = rel_path.replace('index.md', '')
            else:
                url = rel_path.replace('.md', '')
            
            # C. Find Chart Calls: {{ viral_chart('id', variable_name) }}
            # Group 1: ID
            # Group 2: Variable Name
            # Group 3: Extra args (ignored)
            matches = re.findall(r"\{\{\s*viral_chart\s*\(\s*['\"](.*?)['\"]\s*,\s*([^,\)]+)(.*?)\)\s*\}\}", content)

            for (chart_id, var_name, extra) in matches:
                # Retrieve the actual data object from env.variables
                chart_data = getattr(env.variables, var_name, None)
                
                if chart_data:
                    # Create a unique ID for the dashboard
                    home_id = f"home_{chart_id}"
                    
                    # Call viral_chart() manually with a FIXED height for the dashboard
                    chart_html = viral_chart(home_id, chart_data, height="350px")
                    
                    # Wrap in grid item
                    wrapper = f"""
                    <div class="grid-item">
                        <div class="homepage-chart-wrapper">
                            {chart_html}
                            <p class="caption">
                                <a href="{url}">Source: {page_title}</a>
                            </p>
                        </div>
                    </div>
                    """
                    dashboard_items.append(wrapper)

        # Return the full grid HTML
        return '<div class="grid cards" markdown>\n' + "\n".join(dashboard_items) + "\n</div>"

    # --------------------------------------------------------------------------
    # 4. THE GLOBAL TOC GENERATOR
    # --------------------------------------------------------------------------
    @env.macro
    def render_global_toc():
        """
        Scans all markdown files and generates a global nested list of links.
        """
        docs_dir = env.conf['docs_dir']
        toc_lines = []
        md_files = sorted(glob.glob(os.path.join(docs_dir, '**', '*.md'), recursive=True))

        for file_path in md_files:
            # Skip homepage
            if os.path.basename(file_path) == 'index.md' and os.path.dirname(file_path) == docs_dir:
                continue

            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            except:
                continue

            rel_path = os.path.relpath(file_path, docs_dir).replace('\\', '/')
            if rel_path.endswith('index.md'):
                url = rel_path.replace('index.md', '')
            else:
                url = rel_path.replace('.md', '')

            # Parse headers
            lines = content.split('\n')
            for line in lines:
                if line.startswith('# '):
                    title = line.replace('# ', '').strip()
                    toc_lines.append(f"- [{title}]({url})")
                elif line.startswith('## '):
                    sub = line.replace('## ', '').strip()
                    # Basic slugify (lowercase + hyphen). 
                    # Note: For complex headers, you might need a stronger slugify function.
                    anchor = sub.lower().replace(' ', '-').replace('?', '').replace(':', '')
                    toc_lines.append(f"    - [{sub}]({url}#{anchor})")
        
        return "\n".join(toc_lines)
