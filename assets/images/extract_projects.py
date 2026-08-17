import pathlib, re, json

html = pathlib.Path('index(2).html').read_text(encoding='utf-8')
seen = set()
projects = []
for chunk in re.split(r'(?=<div class="card-project)', html):
    if not chunk.startswith('<div class="card-project'):
        continue
    if 'load-more-wrap' in chunk:
        continue
    title_m = re.search(r'<h3>([^<]+)</h3>', chunk)
    if not title_m:
        continue
    title = title_m.group(1).strip()
    if title in seen:
        continue
    seen.add(title)
    category_m = re.search(r'<div class="card-header-top">[\s\S]*?<span class="tag">([^<]+)</span>', chunk)
    desc_m = re.search(r'<p>(.*?)</p>', chunk, re.S)
    tags_section_m = re.search(r'<div class="tags">([\s\S]*?)</div>', chunk)
    tags = []
    if tags_section_m:
        tags = [t.strip() for t in re.findall(r'<span class="tag">([^<]+)</span>', tags_section_m.group(1))]
    img_m = re.search(r'<img src="([^"]+)"', chunk)
    demo_m = re.search(r'<a href="([^"]+)"[^>]*class="btn-card"[^>]*>\s*<i[^>]*>.*?</i>\s*Live Demo', chunk, re.S)
    code_m = re.search(r'<a href="([^"]+)"[^>]*class="btn-card secondary"[^>]*>.*?GitHub', chunk, re.S)
    projects.append({
        'title': title,
        'category': category_m.group(1).strip() if category_m else '',
        'description': desc_m.group(1).strip() if desc_m else '',
        'tags': tags,
        'image': img_m.group(1).strip() if img_m else '',
        'demoUrl': demo_m.group(1).strip() if demo_m else '',
        'codeUrl': code_m.group(1).strip() if code_m else '',
        'hidden': 'project-hidden' in chunk
    })
print(json.dumps(projects, indent=2, ensure_ascii=False))
print('TOTAL', len(projects))
