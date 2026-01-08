import logging

def on_nav(nav, config, files):
    # Iterate through top-level navigation items
    for item in nav:
        # Check if the item points to the homepage (usually index.md)
        if item.url == "" or item.url == "index.html" or item.url == ".":
            # Change the label to the icon
            # You can change this to ":house:" or "🏠" if you prefer
            item.title = ":material-home:"
            break
    return nav
