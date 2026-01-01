import re

def on_nav(nav, config, files):
    def strip_number(items):
        for item in items:
            # 1. Handle items that already have a title (usually Folders)
            if item.title:
                item.title = re.sub(r"^\d+[a-zA-Z]*[-_ ]+", "", item.title)
            
            # 2. Handle Pages (Files) that don't have a title yet
            # MkDocs usually fills this later from the H1 header, but we want 
            # to clean the filename and set it now.
            elif hasattr(item, 'file') and item.file:
                # Get the filename without extension (e.g., "02_why_tourism_is_not_working")
                new_title = item.file.name 
                
                # Apply the regex to strip the number
                new_title = re.sub(r"^\d+[a-zA-Z]*[-_ ]+", "", new_title)
                
                # Optional: Replace underscores with spaces and capitalize
                new_title = new_title.replace("_", " ").title()
                
                # Assign the new title to the item
                item.title = new_title

            # 3. Recursion for nested folders
            if hasattr(item, 'children') and item.children:
                strip_number(item.children)
    
    strip_number(nav.items)
    return nav
