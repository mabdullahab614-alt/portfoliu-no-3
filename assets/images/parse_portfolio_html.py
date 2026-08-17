import json
import pathlib
import re
from html import unescape

html_path = pathlib.Path('index(2).html')
html = html_path.read_text(encoding='utf-8')

# Parse hero
hero_section = re.search(r'<section id="about".*?</section>', html, re.S)
if hero_section:
    hero = hero_section.group(0)
    print('HERO_FOUND')

# Parse contact
contact_section = re.search(r'<section id="contact".*?</section>', html, re.S)
if contact_section:
    print('CONTACT_FOUND')

# Parse all projects
project_blocks = re.findall(r'<div class="card-project[\s\S]*?</div>\s*</div>\s*</div>|<div class="card-project[\s\S]*?</div>\s*</div>', html)
print('PROJECT_COUNT', len(project_blocks))
for idx, block in enumerate(project_blocks, 1):
    title = re.search(r'<h3>([^<]+)</h3>', block)
    category = re.search(r'<span class="tag">([^<]+)</span>', block)
    tags = re.findall(r'<div class="tags">[\s\S]*?<span class="tag">([^<]+)</span>', block)
    demo = re.search(r'<a href="([^"]+)"[^>]*class="btn-card"', block)
    code = re.search(r'<a href="([^"]+)"[^>]*class="btn-card secondary"', block)
    img = re.search(r'<img src="([^"]+)"', block)
    print(idx, title.group(1) if title else None, category.group(1) if category else None)
    print('TAGS', tags)
    print('IMG', img.group(1) if img else None)
    print('DEMO', demo.group(1) if demo else None)
    print('CODE', code.group(1) if code else None)
    print('---')
