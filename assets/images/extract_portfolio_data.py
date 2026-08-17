import pathlib
from html.parser import HTMLParser

html = pathlib.Path('index(2).html').read_text(encoding='utf-8')

class PortfolioParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.projects = []
        self.certifications = []
        self.education = []
        self.hero = {}
        self.contact = {}
        self.current = None
        self.stack = []
        self.current_text = ''
        self.current_entry = None
        self.in_tags = False
        self.current_tags = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.stack.append((tag, attrs))
        cls = attrs.get('class', '')

        if tag == 'section' and attrs.get('id') == 'about':
            self.current = 'hero'
        elif tag == 'section' and attrs.get('id') == 'contact':
            self.current = 'contact'
        elif tag == 'section' and attrs.get('id') == 'education':
            self.current = 'education'
        elif tag == 'section' and attrs.get('id') == 'projects':
            self.current = 'projects'
        elif tag == 'section' and attrs.get('id') == 'certifications':
            self.current = 'certifications'

        if self.current == 'projects' and tag == 'div' and 'card-project' in cls:
            self.current_entry = {'tags': [], 'hidden': 'project-hidden' in cls}
            self.projects.append(self.current_entry)
        elif self.current == 'certifications' and tag == 'div' and 'cert-card' in cls:
            self.current_entry = {}
            self.certifications.append(self.current_entry)
        elif self.current == 'education' and tag == 'div' and 'edu-card-interactive' in cls:
            self.current_entry = {'points': []}
            self.education.append(self.current_entry)

        if self.current == 'projects':
            if tag == 'img' and self.current_entry is not None and 'src' in attrs:
                self.current_entry['image'] = attrs['src']
            if tag == 'a' and self.current_entry is not None:
                cls_attr = attrs.get('class', '')
                if 'btn-card secondary' in cls_attr:
                    self.current_entry['codeUrl'] = attrs.get('href', '')
                elif 'btn-card' in cls_attr:
                    self.current_entry['demoUrl'] = attrs.get('href', '')
            if tag == 'span' and 'tag' in cls:
                self.in_tags = True
        if self.current == 'certifications':
            if tag == 'a' and attrs.get('class', '') == 'cert-view-link':
                self.current_entry['documentUrl'] = attrs.get('href', '')
            if tag == 'div' and 'cert-card-text' in cls:
                self.current_text = ''
            if tag == 'h4' and self.current_entry is not None:
                self.current_text = ''
            if tag == 'div' and 'cert-card-issuer' in cls:
                self.current_text = ''
        if self.current == 'education':
            if tag == 'h3' and self.current_entry is not None:
                self.current_text = ''
            if tag == 'div' and 'edu-school' in cls:
                self.current_text = ''
            if tag == 'div' and 'edu-badge-status' in cls:
                self.current_text = ''
            if tag == 'div' and 'edu-date-pill' in cls:
                self.current_text = ''
            if tag == 'div' and 'edu-stats-highlight' in cls:
                self.current_text = ''
            if tag == 'li' and self.current_entry is not None:
                self.current_text = ''
            if tag == 'a' and self.current_entry is not None and 'btn-edu-action' in attrs.get('class', ''):
                self.current_text = ''
        if self.current == 'hero':
            if tag == 'span' and attrs.get('id') == 'rotatingText':
                self.current_text = ''
            if tag == 'h1':
                self.current_text = ''
            if tag == 'strong':
                self.current_text = ''
            if tag == 'span' and attrs.get('class') == 'stat-label':
                self.current_text = ''
            if tag == 'p':
                self.current_text = ''
            if tag == 'a' and attrs.get('class', '').startswith('btn'):
                self.current_text = ''
            if tag == 'button' and attrs.get('class', '') == 'glow-btn':
                if attrs.get('aria-label'):
                    self.current_entry = {'label': attrs.get('aria-label'), 'url': attrs.get('data-url'), 'type': None}
                    self.hero.setdefault('socials', []).append(self.current_entry)
        if self.current == 'contact':
            if tag == 'span' and 'status-text' in attrs.get('class', ''):
                self.current_text = ''
            if tag == 'span' and 'status-meta' in attrs.get('class', ''):
                self.current_text = ''
            if tag == 'a' and 'contact-item' in attrs.get('class', ''):
                self.current_entry = {'href': attrs.get('href', '')}
            if tag == 'a' and attrs.get('class', '') == 'btn-edu-action':
                self.current_entry = {'resume': attrs.get('href', '')}

    def handle_endtag(self, tag):
        if self.stack:
            self.stack.pop()
        if self.in_tags and tag == 'span':
            self.in_tags = False
        if self.current == 'projects' and tag == 'h3' and self.current_entry is not None and 'title' not in self.current_entry:
            self.current_entry['title'] = self.current_text.strip()
        if self.current == 'projects' and tag == 'span' and self.in_tags and self.current_text.strip():
            if 'category' not in self.current_entry:
                self.current_entry['category'] = self.current_text.strip()
            else:
                self.current_entry['tags'].append(self.current_text.strip())
        if self.current == 'projects' and tag == 'div' and self.current_text.strip() and self.current_entry is not None and 'description' not in self.current_entry:
            self.current_entry['description'] = self.current_text.strip()
        if self.current == 'certifications' and tag == 'h4' and self.current_entry is not None:
            self.current_entry['title'] = self.current_text.strip()
        if self.current == 'certifications' and tag == 'div' and 'cert-card-issuer' in self.stack[-1][1].get('class', '') if self.stack else False:
            self.current_entry['issuer'] = self.current_text.strip()
        if self.current == 'education' and tag == 'h3' and self.current_entry is not None:
            self.current_entry['title'] = self.current_text.strip()
        if self.current == 'education' and tag == 'div' and 'edu-school' in self.stack[-1][1].get('class', '') if self.stack else False:
            self.current_entry['institution'] = self.current_text.strip()
        if self.current == 'education' and tag == 'div' and 'edu-badge-status' in self.stack[-1][1].get('class', '') if self.stack else False:
            self.current_entry['badge'] = self.current_text.strip()
        if self.current == 'education' and tag == 'div' and 'edu-date-pill' in self.stack[-1][1].get('class', '') if self.stack else False:
            self.current_entry['dateRange'] = self.current_text.strip()
        if self.current == 'education' and tag == 'div' and 'edu-stats-highlight' in self.stack[-1][1].get('class', '') if self.stack else False:
            self.current_entry['highlight'] = self.current_text.strip()
        if self.current == 'education' and tag == 'li' and self.current_entry is not None:
            self.current_entry['points'].append(self.current_text.strip())
        if self.current == 'education' and tag == 'a' and self.current_entry is not None and 'btn-edu-action' in self.stack[-1][1].get('class', '') if self.stack else False:
            self.current_entry['ctaLabel'] = self.current_text.strip()
        if self.current == 'hero' and tag == 'span' and self.stack and self.stack[-1][0] == 'span' and self.stack[-1][1].get('id') == 'rotatingText':
            self.hero['title'] = self.current_text.strip()
        if self.current == 'hero' and tag == 'h1':
            self.hero['name'] = self.current_text.strip().replace("Hi, I'm ", '').strip()
        if self.current == 'hero' and tag == 'strong' and self.stack and 'stat-label' in self.stack[-1][1].get('class', ''):
            self.hero.setdefault('stats', []).append({'value': self.current_text.strip(), 'label': ''})
        if self.current == 'hero' and tag == 'span' and self.stack and self.stack[-1][1].get('class') == 'stat-label':
            if self.hero.get('stats'):
                self.hero['stats'][-1]['label'] = self.current_text.strip()
        if self.current == 'hero' and tag == 'p' and 'summary' not in self.hero:
            self.hero['summary'] = self.current_text.strip()
        if self.current == 'hero' and tag == 'a' and self.stack and 'btn-group' in self.stack[-1][1].get('class', ''):
            self.hero.setdefault('buttons', []).append({'label': self.current_text.strip(), 'href': self.stack[-1][1].get('href', ''), 'variant': 'primary' if 'secondary' not in self.stack[-1][1].get('class', '') else 'secondary'})
        if self.current == 'hero' and tag == 'img' and self.stack and self.stack[-1][1].get('class') == 'profile-img':
            self.hero['image'] = self.stack[-1][1].get('src', '')
        if self.current == 'contact' and tag == 'span' and self.stack and 'status-text' in self.stack[-1][1].get('class', ''):
            self.contact['opening'] = self.current_text.strip()
        if self.current == 'contact' and tag == 'span' and self.stack and 'status-meta' in self.stack[-1][1].get('class', ''):
            text = self.current_text.strip()
            if 'replies' in text or 'replies' in text.lower():
                self.contact['replyTime'] = text
            else:
                self.contact['location'] = text
        if self.current == 'contact' and tag == 'a' and self.current_entry is not None and 'mailto:' in self.current_entry.get('href', ''):
            self.contact['email'] = self.current_entry['href'].replace('mailto:', '')
        if self.current == 'contact' and tag == 'a' and self.current_entry is not None and 'linkedin.com' in self.current_entry.get('href', ''):
            self.contact['linkedin'] = self.current_entry['href']
        if self.current == 'contact' and tag == 'a' and self.current_entry is not None and 'github.com' in self.current_entry.get('href', ''):
            self.contact['github'] = self.current_entry['href']
        if self.current == 'contact' and tag == 'a' and self.current_entry is not None and 'huggingface.co' in self.current_entry.get('href', ''):
            self.contact['huggingFace'] = self.current_entry['href']
        if self.current == 'contact' and tag == 'a' and self.current_entry is not None and self.current_entry.get('resume'):
            self.contact['resumeUrl'] = self.current_entry['resume']
        self.current_text = ''

    def handle_data(self, data):
        if self.current_text is not None:
            self.current_text += data

parser = PortfolioParser()
parser.feed(html)
print('HERO', parser.hero)
print('CONTACT', parser.contact)
print('PROJECTS', len(parser.projects))
for p in parser.projects:
    print(p)
print('CERTS', parser.certifications)
print('EDU', parser.education)
