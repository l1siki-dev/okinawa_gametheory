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

    # --- 2. DETECT AND UNWRAP LANGUAGE FOLDER ---
    # The logs showed that your Root is just [En] or [En, Ja].
    # We need to find the folder containing 'index.md' and promote its children to the top.
    
    ROOT_PATHS = ["en/index.md", "ja/index.md"]
    
    wrapper_folder_index = None
    
    log.info("--- CHECKING FOR WRAPPED CONTENT ---")
    
    for i, item in enumerate(nav.items):
        # Check if this top-level item is a Folder (Section)
        if hasattr(item, 'children') and item.children:
            # Check the first file inside to see if it's our index
            first_child = item.children[0]
            if hasattr(first_child, 'file') and first_child.file:
                path = first_child.file.src_path
                
                if path in ROOT_PATHS:
                    log.info(f"✅ Found wrapper folder '{item.title}' containing {path}")
                    wrapper_folder_index = i
                    break

    # If we found a wrapper folder (like 'En'), UNWRAP it.
    if wrapper_folder_index is not None:
        wrapper_item = nav.items[wrapper_folder_index]
        
        # 1. Take the children OUT of the folder
        new_root_items = wrapper_item.children
        
        log.info(f"🚀 Unwrapping {len(new_root_items)} items to the top level.")
        
        # 2. Replace the main nav with these children
        # This brings '01-Guide' etc. to the main tabs!
        nav.items = new_root_items

    # --- 3. RENAME HOME ICON ---
    # Now that index.md is at the top level (index 0), rename it.
    
    if nav.items:
        first_item = nav.items[0]
        if hasattr(first_item, 'file') and first_item.file and first_item.file.src_path in ROOT_PATHS:
            log.info("🏠 Renaming first tab to Home Icon")
            first_item.title = "🏠"

    return nav
