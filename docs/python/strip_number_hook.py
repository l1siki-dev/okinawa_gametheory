import re
import logging

# Set up logging to see what's happening in the console
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

    # --- 2. Find and Move the Root Index ---
    target_item = None
    parent_list = None

    # Helper function to find index.md recursively
    def find_index(items, is_root=False):
        nonlocal target_item, parent_list
        
        for item in items:
            # Check if this item is a File (Page)
            if hasattr(item, 'file') and item.file:
                path = item.file.src_path
                
                # Debug: Print what we found to the console
                if is_root:
                    log.info(f"Root item found: '{item.title}' -> {path}")

                # Check for index.md or language-specific index (en/index.md)
                if path.endswith("index.md"):
                    # We found it!
                    target_item = item
                    parent_list = items
                    return True

            # Check if this item is a Folder (Section) that might contain the index
            # (Only check 1 level deep for the 'home' page usually)
            if hasattr(item, 'children') and item.children:
                if find_index(item.children):
                    return True
        return False

    # Start the search
    log.info("--- LOOKING FOR INDEX.MD ---")
    find_index(nav.items, is_root=True)

    # --- 3. Execute the Move ---
    if target_item and parent_list:
        log.info(f"MOVING: {target_item.title} to the top.")
        
        # Remove from its current location (could be at the end, or inside a folder)
        parent_list.remove(target_item)
        
        # Rename to Icon
        # target_item.title = ":material-home:" 
        target_item.title = "aaaaa" 
        
        # Insert at the very top of the ROOT navigation
        nav.items.insert(0, target_item)
    else:
        log.warning("WARNING: Could not find any 'index.md' to move.")

    return nav
