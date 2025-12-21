import json
import textwrap

def define_env(env):
    @env.macro
    def viral_chart(id, options, height="500px"):
        json_options = json.dumps(options)

        html = f"""
        <div class="chart-wrapper" style="position: relative; width: 100%; max-width: 800px; margin: 0 auto;">
            
            <!-- BUTTON GROUP -->
            <div style="position: absolute; top: 10px; right: 10px; z-index: 10; display: flex; gap: 8px;">
                <button class="md-button" onclick="copyPageUrl()" title="Copy Page URL"
                        style="padding: 4px 10px; font-size: 0.7rem; min-width: auto; background-color: #f0f0f0; color: #333; border: 1px solid #ddd;">
                    🔗 Link
                </button>
                <button class="md-button md-button--primary" onclick="shareChart('{id}')"
                        style="padding: 4px 10px; font-size: 0.7rem; min-width: auto;">
                    ⌲ Share Graph
                </button>
            </div>
            
            <!-- Chart Container: Added class 'lazy-chart' -->
            <div id="{id}" class="lazy-chart" style="width: 100%; height: {height}; background-color: #fff; border-radius: 4px;"></div>
        </div>

        <!-- Store data globally, do not render yet -->
        <script>
            window.osintChartData = window.osintChartData || {{}};
            window.osintChartData['{id}'] = {json_options};
        </script>
        """
        return textwrap.dedent(html)
