import re

def on_nav(nav, config, files):
    # Recursively strip "01-", "02_", etc. from all titles
    def strip_number(items):
        for item in items:
            if item.title:
                # Regex to remove leading numbers followed by - or _
                item.title = re.sub(r"^\d+[-_ ]+", "", item.title)
            if hasattr(item, 'children') and item.children:
                strip_number(item.children)
    
    strip_number(nav.items)
    return nav
