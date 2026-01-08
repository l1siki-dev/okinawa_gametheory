import logging

def on_nav(nav, config, files):
    # Iterate through top-level navigation items
    for item in nav:
        # Check if the item points to the homepage (usually index.md)
        if item.title == "" or item.title == "Index" or item.title == "Home":
            # You can change this to ":house:" or "🏠" if you prefer
            item.title = ":material-home:"
            break
    return nav
