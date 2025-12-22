import json
import textwrap
import os
import re
import glob

def define_env(env):
    """
    This is the hook for defining variables, macros and filters
    """

    # ==============================================================================
    # 1. DEFINE YOUR DATA HERE (CRITICAL: RESTORE YOUR DATA)
    # ==============================================================================
    # You must uncomment/add your data definitions here, or the charts will be blank.
    # Example:
    # env.variables.test2 = { "xAxis": ..., "series": ... } 
    
    # If your data comes from a file, load it here:
    # with open('docs/data/my_data.json') as f:
    #     env.variables.test2 = json.load(f)

    # ==============================================================================
    # 2. VIRAL CHART MACRO (Your Original Logic)
    # ==============================================================================
    @env.macro
    def viral_chart(id, options, height="700px"):
        # Safety check: if options are missing, return error msg
        if not options:
            return f'<div style="color:red; border:1px solid red; padding:10px;">Error: Data for chart "{id}" is missing or None.</div>'

        json_options = json.dumps(options)
        
        icon_share = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path fill="currentColor" d="M18 16.08c-.76 0-1.44.3-1.96.77L8.91 12.7c.05-.23.09-.46.09-.7s-.04-.47-.09-.7l7.05-4.11c.54.5 1.25.81 2.04.81a3 3 0 0 0 3-3 3 3 0 0 0-3-3 3 3 0 0 0-3 3c0 .24.04.47.09.7L8.04 9.81C7.5 9.31 6.79 9 6 9a3 3 0 0 0-3 3 3 3 0 0 0 3 3c.79 0 1.5-.31 2.04-.81l7.12 4.15c-.05.21-.08.43-.08.66 0 1.61 1.31 2.91 2.92 2.91s2.92-1.3 2.92-2.91a2.92 2.92 0 0 0-2.92-2.91"/></svg>'

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

    # ==============================================================================
    # 3. DASHBOARD MACRO (Automated Grid)
    # ==============================================================================
    @env.macro
    def render_dashboard():
        docs_dir = env.conf['docs_dir']
        dashboard_items = []
        
        md_files = sorted(glob.glob(os.path.join(docs_dir, '**', '*.md'), recursive=True))

        for file_path in md_files:
            if os.path.basename(file_path) == 'index.md' and os.path.dirname(file_path) == docs_dir:
                continue

            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            except:
                continue

            # 1. Get Title
            page_title = os.path.basename(file_path)
            h1 = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
            if h1:
                page_title = h1.group(1).strip()

            # 2. Get Link
            rel_path = os.path.relpath(file_path, docs_dir).replace('\\', '/')
            if rel_path.endswith('index.md'):
                url = rel_path.replace('index.md', '')
            else:
                url = rel_path.replace('.md', '')

            # 3. Find Charts
            # Regex captures: 1=ID, 2=VariableName
            matches = re.findall(r"\{\{\s*viral_chart\s*\(\s*['\"](.*?)['\"]\s*,\s*([^,\)]+)(.*?)\)\s*\}\}", content)

            for (chart_id, var_name, extra) in matches:
                # Retrieve data safely
                chart_data = getattr(env.variables, var_name, None)
                
                if chart_data:
                    home_id = f"home_{chart_id}"
                    
                    # CALL VIRAL CHART "AS IS" (No height override)
                    chart_html = viral_chart(home_id, chart_data)
                    
                    # Wrap in simple card div
                    item = f"""
                    <div class="dashboard-card">
                        <div class="card-header"><a href="{url}">{page_title}</a></div>
                        <div class="card-content">
                            {chart_html}
                        </div>
                    </div>
                    """
                    dashboard_items.append(item)
        
        if not dashboard_items:
            return "No charts found (Check if variables like 'test2' are defined in main.py)"

        return '<div class="dashboard-grid">' + "\n".join(dashboard_items) + "</div>"

    # ==============================================================================
    # 4. TOC MACRO
    # ==============================================================================
    @env.macro
    def render_global_toc():
        docs_dir = env.conf['docs_dir']
        toc_lines = []
        md_files = sorted(glob.glob(os.path.join(docs_dir, '**', '*.md'), recursive=True))

        for file_path in md_files:
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

            lines = content.split('\n')
            for line in lines:
                if line.startswith('# '):
                    title = line.replace('# ', '').strip()
                    toc_lines.append(f"- [{title}]({url})")
                elif line.startswith('## '):
                    sub = line.replace('## ', '').strip()
                    anchor = sub.lower().replace(' ', '-').replace('?', '').replace(':', '')
                    toc_lines.append(f"    - [{sub}]({url}#{anchor})")
        
        return "\n".join(toc_lines)
