import re
import logging

# Setup logging
log = logging.getLogger("mkdocs")

def on_nav(nav, config, files):
    # --- 1. Strip Numbers (Your existing code) ---
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

    # --- 2. DEBUG LOG & SNIPE EXACT FILE ---
    
    # 📝 CONFIGURATION: Put the EXACT path you want to move here.
    # Check the console logs below if this doesn't work.
    TARGET_PATHS = ["en/index.md", "index.md", "ja/index.md"]

    target_index = None

    log.info("================ NAV DEBUG LOG ================")

    for i, item in enumerate(nav.items):
        # Case A: It is a standalone File (Page)
        if hasattr(item, 'file') and item.file:
            path = item.file.src_path
            log.info(f"[{i}] TYPE: Page    | TITLE: {item.title} | PATH: {path}")
            
            if path in TARGET_PATHS:
                target_index = i

        # Case B: It is a Folder (Section)
        elif hasattr(item, 'children'):
            log.info(f"[{i}] TYPE: Section | TITLE: {item.title}")
            
            # Check the first file inside the folder to see if it's the index
            if item.children and hasattr(item.children[0], 'file') and item.children[0].file:
                child_path = item.children[0].file.src_path
                log.info(f"    -> First Child Path: {child_path}")
                
                if child_path in TARGET_PATHS:
                    target_index = i
        
        else:
             log.info(f"[{i}] TYPE: Unknown | TITLE: {item.title}")

    log.info("===============================================")

    # --- 3. Execute Move ---
    if target_index is not None:
        log.info(f"✅ FOUND target at Index [{target_index}]. Moving to TOP.")
        
        # 1. Grab the item
        item_to_move = nav.items[target_index]
        
        # 2. Rename it
        item_to_move.title = "🏠 Home"
        
        # 3. Remove from old spot
        nav.items.pop(target_index)
        
        # 4. Insert at the start
        nav.items.insert(0, item_to_move)
    else:
        log.warning("❌ TARGET NOT FOUND. Please check the PATH in the logs above.")

    return nav
