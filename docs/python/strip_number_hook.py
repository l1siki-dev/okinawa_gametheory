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

    # --- 2. Find and Move Root Index (In-Place) ---
    
    # Define your root files
    ROOT_PATHS = ["index.md", "en/index.md", "ja/index.md"]
    
    home_index = None

    # Iterate through the top-level items to find WHERE the home page is
    for i, item in enumerate(nav.items):
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
        
        if is_home:
            home_index = i
            break # Stop looking once we found it

    # --- 3. Execute the Move ---
    if home_index is not None:
        log.info(f"Found Home at index {home_index}. Moving to top.")
        
        # Get the item
        home_item = nav.items[home_index]
        
        # Rename it
        home_item.title = "🏠 Home"
        
        # Move it: Pop from old spot, Insert at 0
        # This guarantees we don't lose any other tabs!
        nav.items.pop(home_index)
        nav.items.insert(0, home_item)
        
    return nav
