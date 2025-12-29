import os

def on_config(config):
    # Check if we are running in GitHub Actions
    if "GITHUB_REPOSITORY" in os.environ:
        # GITHUB_REPOSITORY is "owner/repo-name"
        repo_env = os.environ["GITHUB_REPOSITORY"]
        owner, repo = repo_env.split("/")
        
        # Construct the correct GitHub Pages URL
        # Format: https://owner.github.io/repo/
        new_url = f"https://{owner}.github.io/{repo}/"
        
        # Overwrite the site_url in the config
        config["site_url"] = new_url
        print(f"🌍 Dynamic Host Detected: Setting site_url to {new_url}")
