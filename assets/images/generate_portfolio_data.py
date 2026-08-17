import json
import pathlib
import re

html_path = pathlib.Path('index(2).html')
html = html_path.read_text(encoding='utf-8')
headline_words = [
    'Open for Opportunities',
    'Agentic AI Engineer',
    'AI Systems Builder',
    'AI & ML Developer',
    'Deep Learning Engineer'
]


def normalize_text(text: str) -> str:
    text = re.sub(r'<[^>]+>', '', text)
    return ' '.join(text.split()).strip()


def find_blocks(source: str, opener: str) -> list[str]:
    blocks = []
    idx = 0
    while True:
        start = source.find(opener, idx)
        if start == -1:
            break
        pos = start + len(opener)
        depth = 1
        while depth > 0:
            next_open = source.find('<div', pos)
            next_close = source.find('</div>', pos)
            if next_close == -1:
                break
            if next_open != -1 and next_open < next_close:
                depth += 1
                pos = next_open + 4
            else:
                depth -= 1
                pos = next_close + 6
        blocks.append(source[start:pos])
        idx = pos
    return blocks


def extract_section(id_value: str) -> str | None:
    match = re.search(rf'<section id="{id_value}".*?</section>', html, re.S)
    return match.group(0) if match else None


def extract_hero() -> dict:
    section = extract_section('about')
    if section is None:
        return {}
    title_match = re.search(r'<span id="rotatingText">([^<]*)</span>', section)
    title = title_match.group(1).strip() if title_match else ''
    if not title:
        title = headline_words[0]
    name_match = re.search(r'<h1>Hi, I(?:&#39;|\'|\u2019)m <span>([^<]+)</span>', section)
    name = name_match.group(1).strip() if name_match else 'Abdullah Javid'
    badges = re.findall(r'<span class="pill-badge">([^<]+)</span>', section)
    stats = []
    for value, label in re.findall(r'<strong>([^<]+)</strong>\s*<span class="stat-label">([^<]+)</span>', section):
        stats.append({'label': label.strip(), 'value': value.strip()})
    summary_match = re.search(r'<p>(.*?)</p>', section, re.S)
    summary = normalize_text(summary_match.group(1)) if summary_match else ''
    buttons = []
    for button_match in re.findall(r'<a[^>]*href="([^"]+)"[^>]*class="btn(?: secondary)?"[^>]*>(?:<i[^>]*>.*?</i>)?\s*([^<]+)</a>', section, re.S):
        label = button_match[1].strip()
        variant = 'secondary' if 'Contact' in label or 'Resume' in label else 'primary'
        buttons.append({'label': label, 'href': button_match[0].strip(), 'variant': variant})
    socials = []
    for url, label in re.findall(r'<button class="glow-btn" data-url="([^"]+)" aria-label="([^"]+)"', section):
        url = url.strip()
        if url.startswith('mailto:'):
            typ = 'email'
        elif 'linkedin.com' in url:
            typ = 'linkedin'
        elif 'github.com' in url:
            typ = 'github'
        else:
            typ = 'huggingface'
        socials.append({'label': label.strip(), 'url': url, 'type': typ})
    img_match = re.search(r'<img src="([^"]+)" alt="[^>]*">', section)
    image = img_match.group(1).strip() if img_match else '/pic.jpeg'
    return {
        'title': title,
        'name': name,
        'badges': badges,
        'stats': stats,
        'summary': summary,
        'buttons': buttons,
        'socials': socials,
        'image': image
    }


def extract_skills() -> list:
    section = extract_section('skills')
    if section is None:
        return []
    panel_map = {'panel-ai': 'ai', 'panel-vision': 'vision', 'panel-web': 'web'}
    skills = []
    panel_blocks = find_blocks(section, '<div class="skills-panel')
    for panel_block in panel_blocks:
        panel_id_match = re.search(r'id="([^"]+)"', panel_block)
        panel_key = panel_map.get(panel_id_match.group(1), 'ai') if panel_id_match else 'ai'
        card_blocks = find_blocks(panel_block, '<div class="pro-skill-card">')
        for card in card_blocks:
            title_match = re.search(r'<h3>([^<]+)</h3>', card)
            category_match = re.search(r'<span class="pro-skill-cat">([^<]+)</span>', card)
            desc_match = re.search(r'<p class="pro-skill-micro-desc">(.*?)</p>', card, re.S)
            level_match = re.search(r'<span class="pro-skill-level [^"]*">([^<]+)</span>', card)
            tags = re.findall(r'<span class="pro-tech-chip">([^<]+)</span>', card)
            filter_match = re.search(r"applySkillFilter\('([^']+)'\)", card)
            skills.append({
                'title': title_match.group(1).strip() if title_match else '',
                'category': category_match.group(1).strip() if category_match else '',
                'description': normalize_text(desc_match.group(1)) if desc_match else '',
                'level': level_match.group(1).strip() if level_match else 'Proficient',
                'tags': tags,
                'filterTag': filter_match.group(1).strip() if filter_match else (tags[0] if tags else ''),
                'panel': panel_key
            })
    return skills


def extract_projects() -> list:
    project_blocks = find_blocks(html, '<div class="card-project')
    projects = []
    seen_titles = set()
    for block in project_blocks:
        title_match = re.search(r'<h3>([^<]+)</h3>', block)
        if not title_match:
            continue
        title = title_match.group(1).strip()
        if title in seen_titles:
            continue
        seen_titles.add(title)
        category_match = re.search(r'<span class="tag">([^<]+)</span>', block)
        description_match = re.search(r'<p>(.*?)</p>', block, re.S)
        tags_match = re.search(r'<div class="tags">(.*?)</div>', block, re.S)
        tags = re.findall(r'<span class="tag">([^<]+)</span>', tags_match.group(1)) if tags_match else []
        img_match = re.search(r'<img src="([^"]+)"', block)
        demo_match = re.search(r'<a href="([^"]+)"[^>]*class="btn-card"[^>]*>\s*<i[^>]*>.*?</i>\s*Live Demo', block, re.S)
        code_match = re.search(r'<a href="([^"]+)"[^>]*class="btn-card secondary"[^>]*>.*?GitHub', block, re.S)
        projects.append({
            'title': title,
            'category': category_match.group(1).strip() if category_match else '',
            'description': normalize_text(description_match.group(1)) if description_match else '',
            'tags': tags,
            'image': '/' + img_match.group(1).strip() if img_match else '',
            'demoUrl': demo_match.group(1).strip() if demo_match else '',
            'codeUrl': code_match.group(1).strip() if code_match else '',
            'hidden': 'project-hidden' in block
        })
    return projects


def extract_education() -> list:
    section = extract_section('education')
    if section is None:
        return []
    cards = find_blocks(section, '<div class="edu-card-interactive">')
    education = []
    for card in cards:
        title_match = re.search(r'<h3>([^<]+)</h3>', card)
        institution_match = re.search(r'<div class="edu-school">(.*?)</div>', card, re.S)
        badge_match = re.search(r'<div class="edu-badge-status">(.*?)</div>', card, re.S)
        date_match = re.search(r'<div class="edu-date-pill">(.*?)</div>', card, re.S)
        highlight_match = re.search(r'<div class="edu-stats-highlight">(.*?)</div>', card, re.S)
        points = [normalize_text(pt) for pt in re.findall(r'<li>(.*?)</li>', card, re.S)]
        cta_match = re.search(r'<a href="([^"]+)"[^>]*class="btn-edu-action"[^>]*>(.*?)</a>', card, re.S)
        education.append({
            'title': title_match.group(1).strip() if title_match else '',
            'institution': normalize_text(institution_match.group(1)) if institution_match else '',
            'badge': normalize_text(badge_match.group(1)) if badge_match else '',
            'dateRange': normalize_text(date_match.group(1)) if date_match else '',
            'highlight': normalize_text(highlight_match.group(1)) if highlight_match else '',
            'points': points,
            'ctaLabel': normalize_text(cta_match.group(2)) if cta_match else 'View Details',
            'ctaUrl': cta_match.group(1).strip() if cta_match else ''
        })
    return education


def extract_certifications() -> list:
    section = extract_section('certifications')
    if section is None:
        return []
    categories = {
        'cert-panel-claude': 'anthropic',
        'cert-panel-fluency': 'fluency',
        'cert-panel-professional': 'professional',
        'cert-panel-achievements': 'achievements'
    }
    certifications = []
    panel_blocks = find_blocks(section, '<div class="cert-panel')
    for panel_block in panel_blocks:
        panel_id_match = re.search(r'id="([^"]+)"', panel_block)
        category = categories.get(panel_id_match.group(1), 'achievements') if panel_id_match else 'achievements'
        card_blocks = find_blocks(panel_block, '<div class="cert-card">')
        for card in card_blocks:
            title_match = re.search(r'<h4>([^<]+)</h4>', card)
            issuer_match = re.search(r'<div class="cert-card-issuer">(.*?)</div>', card, re.S)
            url_match = re.search(r'<a href="([^"]+)"[^>]*class="cert-view-link"', card)
            certifications.append({
                'title': title_match.group(1).strip() if title_match else '',
                'issuer': normalize_text(issuer_match.group(1)) if issuer_match else '',
                'documentUrl': '/' + url_match.group(1).strip() if url_match else '',
                'category': category
            })
    return certifications


def extract_contact() -> dict:
    section = extract_section('contact')
    if section is None:
        return {}
    opening_match = re.search(r'<span class="status-text">(.*?)</span>', section, re.S)
    opening = normalize_text(opening_match.group(1)) if opening_match else ''
    reply_time = ''
    location = ''
    for meta in re.findall(r'<span class="status-meta">(.*?)</span>', section, re.S):
        text = normalize_text(meta)
        if 'replies' in text.lower():
            reply_time = text
        elif 'lahore' in text.lower() or 'remote' in text.lower() or 'on-site' in text.lower():
            location = text
    email_match = re.search(r'href="mailto:([^"]+)"', section)
    linkedin_match = re.search(r'href="(https://www\.linkedin\.com/[^"]+)"', section)
    github_match = re.search(r'href="(https://github\.com/[^"]+)"', section)
    huggingface_match = re.search(r'href="(https://huggingface\.co/[^"]+)"', section)
    resume_match = re.search(r'<a href="([^"]+)" download class="btn-edu-action', section)
    return {
        'opening': opening,
        'replyTime': reply_time,
        'location': location,
        'email': email_match.group(1).strip() if email_match else '',
        'linkedin': linkedin_match.group(1).strip() if linkedin_match else '',
        'github': github_match.group(1).strip() if github_match else '',
        'huggingFace': huggingface_match.group(1).strip() if huggingface_match else '',
        'resumeUrl': '/' + resume_match.group(1).strip() if resume_match else ''
    }

portfolio_data = {
    'hero': extract_hero(),
    'skills': extract_skills(),
    'projects': extract_projects(),
    'education': extract_education(),
    'certifications': extract_certifications(),
    'contact': extract_contact()
}

output_path = pathlib.Path('backend/app/portfolio_data.json')
output_path.write_text(json.dumps(portfolio_data, indent=2), encoding='utf-8')
print(f'Written {output_path}')
print('projects', len(portfolio_data['projects']))
print('skills', len(portfolio_data['skills']))
print('education', len(portfolio_data['education']))
print('certifications', len(portfolio_data['certifications']))
