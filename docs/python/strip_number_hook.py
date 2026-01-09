import re

def on_nav(nav, config, files):
    # --- PART 1: Strip numbers (Same as before) ---
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

    # --- PART 2: Handle i18n Root Index ---
    root_index = None
    
    # Iterate through the TOP LEVEL items of the navigation
    for item in nav.items:
        # We only care about Files (Pages), not Folders (Sections) at this level
        if hasattr(item, 'file') and item.file:
            
            # Check the source path.
            # Using .endswith() handles "index.md", "en/index.md", "ja/index.md"
            if item.file.src_path.endswith("index.md"):
                root_index = item
                break
    
    # Move and Rename
    if root_index:
        # 1. Remove from current position (usually the end)
        nav.items.remove(root_index)
        
        # 2. Rename to Icon (Make sure emoji extension is on)
        # root_index.title = ":material-home:"
        root_index.title = "aaaa"
        
        # 3. Insert at the absolute top (Index 0)
        nav.items.insert(0, root_index)

    return nav
