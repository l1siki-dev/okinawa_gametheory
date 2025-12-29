import re
import os
from mkdocs.structure.pages import Page
from mkdocs.config.defaults import MkDocsConfig

def on_page_markdown(markdown: str, page: Page, config: MkDocsConfig, **kwargs):
    # --- 0. PRE-PROCESS: Remove '???' blocks (Optional Read/Raw Data) ---
    lines = markdown.split('\n')
    cleaned_lines = []
    in_exclude_block = False
    exclude_base_indent = 0

    for line in lines:
        stripped = line.lstrip()
        current_indent = len(line) - len(stripped)

        if stripped.startswith('???'):
            in_exclude_block = True
            exclude_base_indent = current_indent
            continue 

        if in_exclude_block:
            if not stripped:
                continue 
            if current_indent > exclude_base_indent:
                continue
            else:
                in_exclude_block = False

        cleaned_lines.append(line)

    filtered_markdown = "\n".join(cleaned_lines)

    # 1. Clean up HTML tags and basic markdown symbols
    #    (We do this first to avoid counting hidden HTML attributes)
    text = re.sub(r'<[^>]*>', '', filtered_markdown)
    text = re.sub(r'[#*`~\[\]]', '', text) 
    
    # 2. Robust Language Detection
    src_path = page.file.src_path
    is_japanese = (
        src_path.startswith('ja/') or 
        '/ja/' in src_path or
        src_path.endswith('.ja.md')
    )

    # 3. Calculate based on language
    if is_japanese:
        # JAPANESE: Keep ONLY Japanese characters
        # \u3001-\u303F : Japanese Punctuation (excludes \u3000 space)
        # \u3040-\u309F : Hiragana
        # \u30A0-\u30FF : Katakana
        # \u4E00-\u9FFF : Kanji
        
        japanese_chars = re.findall(r'[\u3001-\u303F\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF]+', text)
        clean_text = "".join(japanese_chars)
        
        count = len(clean_text)
        # Avg speed: 500 chars/min
        minutes = round(count / 500)
        label = "文字"
        read_label = "読了時間"
    else:
        # ENGLISH: Count Words
        words = text.split()
        count = len(words)
        # Avg speed: 200 words/min
        minutes = round(count / 200)
        label = "Words"
        read_label = "Read time"

    if minutes < 1:
        minutes = 1

    # 4. Save metadata
    page.meta['read_time'] = minutes
    page.meta['word_count'] = count
    
    # 5. Inject header
    header_html = (
        f"<p style='opacity:0.6; font-size:0.8rem; margin-top:-1rem; margin-bottom:1rem;'>"
        f"⏱️ {read_label}: ~{minutes} min ({count} {label})"
        f"</p>\n\n"
    )
        
    return header_html + markdown
