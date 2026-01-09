import re
import logging

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

    # --- 2. Find the Root/Home Item (Page OR Section) ---
    
    home_item = None
    other_items = []

    log.info("--- NAV HOOK START ---")

    for item in nav.items:
        is_home = False
        
        # Debug: Print what we are seeing
        item_type = "Section" if hasattr(item, 'children') else "Page"
        log.info(f"Scanning item: [{item_type}] '{item.title}'")

        # CASE A: It is a standalone Page (e.g. index.md at root)
        if hasattr(item, 'file') and item.file:
            if item.file.src_path.endswith("index.md"):
                log.info(f"-> MATCH (File): {item.file.src_path}")
                is_home = True

        # CASE B: It is a Section (Folder) that contains index.md
        # (e.g. The 'En' folder containing 'en/index.md')
        elif hasattr(item, 'children') and item.children:
            first_child = item.children[0]
            if hasattr(first_child, 'file') and first_child.file:
                if first_child.file.src_path.endswith("index.md"):
                    log.info(f"-> MATCH (Section containing index): {first_child.file.src_path}")
                    is_home = True

        # Separate the Home item from the rest
        if is_home:
            # Rename the tab to the Home Icon
            item.title = ":material-home:"
            home_item = item
        else:
            other_items.append(item)

    # --- 3. Rebuild Navigation ---
    if home_item:
        log.info("-> Moving Home item to the top.")
        nav.items = [home_item] + other_items
    else:
        log.warning("-> Still could not find an index.md or a folder containing it.")

    return nav
