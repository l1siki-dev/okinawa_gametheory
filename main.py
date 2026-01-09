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
    # 1. DYNAMIC JSON LOADER (Restored)
    # ==============================================================================
    # Define the path to your data folder
    json_dir = os.path.join(env.project_dir, 'docs', 'json')

    # Check if directory exists
    if os.path.exists(json_dir):
        # Iterate over every file in that directory
        for filename in os.listdir(json_dir):
            if filename.endswith('.json'):
                # Create variable name: "my_stats.json" -> "my_stats"
                var_name = os.path.splitext(filename)[0]
                file_path = os.path.join(json_dir, filename)

                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        # Load the JSON and inject it into the environment
                        env.variables[var_name] = json.load(f)
                        print(f" -> Loaded data variable: {var_name}")
                except Exception as e:
                    print(f"Error loading {filename}: {e}")
    else:
        print(f"Warning: Data directory not found at {json_dir}")


    # ==============================================================================
    # 2. VIRAL CHART MACRO
    # ==============================================================================
    @env.macro
    def viral_chart(id, options, height="700px"):
        """
        Generates the HTML for an EChart.
        """
        if not options:
            return f'<div style="color:red; border:1px solid red; padding:10px;">Error: Data for chart "{id}" is missing.</div>'

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
        
        # return "\n".join(toc_lines)
        return "\n"
