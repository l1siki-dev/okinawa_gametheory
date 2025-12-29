import re
from mkdocs.structure.pages import Page
from mkdocs.config.defaults import MkDocsConfig

def on_page_markdown(markdown: str, page: Page, config: MkDocsConfig, **kwargs):
    # 1. Clean up the text (remove HTML, markdown symbols) to get pure content
    text = re.sub(r'<[^>]*>', '', markdown)
    text = re.sub(r'[#*`~\[\]]', '', text)
    
    # 2. Detect Language based on file path
    # Adjust this logic to match your folder structure!
    # Common setups: "docs/ja/..." or "filename.ja.md"
    is_japanese = '/ja/' in page.file.src_path or page.file.src_path.endswith('.ja.md')

    if is_japanese:
        # JAPANESE LOGIC: Count Characters
        # Strip spaces/newlines to count actual chars
        clean_text = text.replace(' ', '').replace('\n', '')
        count = len(clean_text)
        
        # Japanese avg speed: ~500 chars/minute
        minutes = round(count / 500)
        label = "文字" # "Characters"
    else:
        # ENGLISH LOGIC: Count Words
        # Split by whitespace to count words
        words = text.split()
        count = len(words)
        
        # English avg speed: ~200 words/minute
        minutes = round(count / 200)
        label = "Words"

    # Minimum 1 minute
    if minutes < 1:
        minutes = 1

    # 3. Save data to page metadata
    # You can use {{ page.meta.read_time }} in your theme templates
    page.meta['read_time'] = minutes
    page.meta['word_count'] = count
    
    # 4. (Optional) Inject directly into the top of the page
    # This automatically adds it to every page without editing templates
    if is_japanese:
        header = f"<p style='opacity:0.6; font-size:0.8rem; margin-top:-1rem;'>⏱️ 読了時間: 約{minutes}分 ({count} {label})</p>\n\n"
    else:
        header = f"<p style='opacity:0.6; font-size:0.8rem; margin-top:-1rem;'>⏱️ Read time: ~{minutes} min ({count} {label})</p>\n\n"
        
    return header + markdown
