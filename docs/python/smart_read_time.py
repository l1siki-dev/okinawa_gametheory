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
        # Calculate current indentation level (spaces/tabs)
        current_indent = len(line) - len(stripped)

        # Detect the start of a "???" block
        # We check startswith('???') to catch both "???" and "???+" (if you use that)
        if stripped.startswith('???'):
            in_exclude_block = True
            exclude_base_indent = current_indent
            continue  # Skip the title line itself

        if in_exclude_block:
            # If line is empty, it's usually part of the block spacing -> skip
            if not stripped:
                continue
            
            # If line is indented deeper than the '???' definition, it is inside the block
            if current_indent > exclude_base_indent:
                continue
            else:
                # We hit a line with equal or less indentation -> Block has ended
                in_exclude_block = False
                # Proceed to add this line to cleaned_lines
        
        cleaned_lines.append(line)

    # Reassemble text without the ??? blocks
    filtered_markdown = "\n".join(cleaned_lines)

    # 1. Clean up text to get pure content (Use filtered_markdown now)
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
        # JAPANESE: Count Characters (No spaces)
        clean_text = text.replace(' ', '').replace('\n', '')
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
    
    # Return original markdown (including the ??? blocks), but with the header added
    return header_html + markdown
