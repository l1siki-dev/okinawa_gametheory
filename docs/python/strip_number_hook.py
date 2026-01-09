import re
import logging

# Setup logging so you can see the output in your terminal
log = logging.getLogger("mkdocs")

def on_nav(nav, config, files):
    # --- 1. Strip Numbers (Your existing logic) ---
    def strip_number(items):
        for item in items:
            if item.title:
                item.title = re.sub(r"^\d+[a-zA-Z]*[-_ ]+", "", item.title)
            elif hasattr(item, 'file') and item.file:
                new_title = item.file.name 
                new_title = re.sub(r"^\d+[a-zA-Z]*[-_ ]+", "", new_title)
                new_title = new_title.replace("_", " ").title()
                item.title = new_title
            
            if hasattr(item, 'children') and item.children:
                strip_number(item.children)
    
    strip_number(nav.items)

    # --- 2. Find, Rename, and Sort the Root Index ---
    
    home_items = []
    other_items = []

    log.info("--- NAV HOOK START ---")

    for item in nav.items:
        is_home = False
        
        # Check if this item is a Page (File) and ends with index.md
        # This covers "index.md", "en/index.md", "ja/index.md"
        if hasattr(item, 'file') and item.file:
            path = item.file.src_path
            log.info(f"Found Top-Level Page: {path}")
            
            if path.endswith("index.md"):
                is_home = True

        if is_home:
            # Rename it here
            log.info(f"-> Identifying {item.title} as HOME")
            item.title = ":material-home:" # Or "Home" or "aaaa"
            home_items.append(item)
        else:
            other_items.append(item)

    # --- 3. Rebuild the Navigation ---
    # If we found a home item, put it first.
    if home_items:
        nav.items = home_items + other_items
        log.info("-> Home moved to top.")
    else:
        log.warning("-> No top-level index.md found. Tabs order unchanged.")

    return nav
