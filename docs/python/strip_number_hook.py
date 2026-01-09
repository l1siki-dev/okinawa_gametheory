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

    # --- 2. Find the Specific Root Index ---
    
    # Define exactly which files count as "Root Home"
    # This prevents '01-guide/index.md' from confusing the script.
    ROOT_PATHS = ["index.md", "en/index.md", "ja/index.md"]

    home_item = None
    other_items = []

    for item in nav.items:
        is_home = False
        
        # Check if item is a Page (File)
        if hasattr(item, 'file') and item.file:
            if item.file.src_path in ROOT_PATHS:
                is_home = True

        # Check if item is a Section (Folder) containing the index
        elif hasattr(item, 'children') and item.children:
            first_child = item.children[0]
            if hasattr(first_child, 'file') and first_child.file:
                if first_child.file.src_path in ROOT_PATHS:
                    is_home = True

        # Sort into buckets
        if is_home:
            # Using Unicode Emoji 🏠 is safer than :material-home:
            # You can change this string to whatever you want.
            item.title = "🏠 Home"
            home_item = item
        else:
            other_items.append(item)

    # --- 3. Rebuild Navigation ---
    if home_item:
        # Put Home first, then everything else
        nav.items = [home_item] + other_items
    else:
        # If no home found, leave it alone (or just stripped numbers)
        nav.items = other_items # effectively same as original items if home not found

    return nav
