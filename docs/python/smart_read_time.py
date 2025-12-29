import re
import os
from mkdocs.structure.pages import Page
from mkdocs.config.defaults import MkDocsConfig

def on_page_markdown(markdown: str, page: Page, config: MkDocsConfig, **kwargs):
    # --- DEBUGGING (Optional: Check your console output if still stuck) ---
    # print(f"Processing: {page.file.src_path}") 
    
    # 1. Clean up text to get pure content
    text = re.sub(r'<[^>]*>', '', markdown)
    text = re.sub(r'[#*`~\[\]]', '', text)
    
    # 2. Robust Language Detection for "folder" structure
    #    This checks if the file path starts with "ja/" OR contains "/ja/" (nested)
    src_path = page.file.src_path  # e.g., "ja/01_Fake_Tourism/..."
    
    is_japanese = (
        src_path.startswith('ja/') or 
        '/ja/' in src_path or
        src_path.endswith('.ja.md')
    )

    # 3. Calculate based on language
    if is_japanese:
        # JAPANESE: Count Characters (No spaces)
        clean_text = text.replace(' ', '').replace('\n', '')
        count = len(clean_text)
        # Avg speed: 500 chars/min
        minutes = round(count / 500)
        label = "文字"
        read_label = "読了時間"
    else:
        # ENGLISH: Count Words (Split by space)
        words = text.split()
        count = len(words)
        # Avg speed: 200 words/min
        minutes = round(count / 200)
        label = "Words"
        read_label = "Read time"

    if minutes < 1:
        minutes = 1

    # 4. Save metadata (usable in templates)
    page.meta['read_time'] = minutes
    page.meta['word_count'] = count
    
    # 5. Inject header into the page content
    #    Styles: slightly transparent, small font, negative margin to pull it up
    header_html = (
        f"<p style='opacity:0.6; font-size:0.8rem; margin-top:-1rem; margin-bottom:1rem;'>"
        f"⏱️ {read_label}: ~{minutes} min ({count} {label})"
        f"</p>\n\n"
    )
        
    return header_html + markdown
