import re

def on_nav(nav, config, files):
    # --- PART 1: Your existing logic to strip numbers ---
    def strip_number(items):
        for item in items:
            # Handle Folders/items with titles
            if item.title:
                item.title = re.sub(r"^\d+[a-zA-Z]*[-_ ]+", "", item.title)
            
            # Handle Pages without titles (clean filenames)
            elif hasattr(item, 'file') and item.file:
                new_title = item.file.name 
                new_title = re.sub(r"^\d+[a-zA-Z]*[-_ ]+", "", new_title)
                new_title = new_title.replace("_", " ").title()
                item.title = new_title

            # Recursion
            if hasattr(item, 'children') and item.children:
                strip_number(item.children)
    
    strip_number(nav.items)

    # --- PART 2: Move index.md to top and rename ---
    root_index = None
    
    # 1. Find the root index.md object
    for item in nav.items:
        # Check if the item is a file and specifically 'index.md'
        if hasattr(item, 'file') and item.file and item.file.src_path == 'index.md':
            root_index = item
            break
    
    # 2. If found, move it and rename it
    if root_index:
        # Remove from current position (likely the end)
        nav.items.remove(root_index)
        
        # Change the Title
        # You can use text "Home" or an icon code like ":material-home:"
        root_index.title = ":material-home:" 
        
        # Insert at the very beginning
        nav.items.insert(0, root_index)

    return nav
