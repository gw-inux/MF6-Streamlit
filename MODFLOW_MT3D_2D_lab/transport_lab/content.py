"""UTF-8 Markdown text, filename language suffixes and per-key English fallback.

Files: intro_en.md, intro_de.md, interface_en.md, interface_de.md, etc.
Interface blocks use <!-- key: stable label -->; keys are never translated.
"""
from pathlib import Path
import re
from functools import lru_cache
from matplotlib.text import Text as FigureText

ROOT=Path(__file__).resolve().parents[1]/'assets'/'md'
# Same language choices and order as Picard–Newton Lab v0.19.
LANGUAGE_NAMES={'en':'🇬🇧 English','de':'🇩🇪 Deutsch','fr':'🇫🇷 Français','es':'🇪🇸 Español',
                'it':'🇮🇹 Italiano','hi':'🇮🇳 हिन्दी','ar':'🌐 العربية','zh':'🇨🇳 简体中文',
                'pt':'🇵🇹 Português','bn':'🇧🇩 বাংলা (Bengali)'}


def available_languages(root=ROOT):
    codes={p.stem.rsplit('_',1)[-1] for p in Path(root).glob('interface_*.md')}
    return {**LANGUAGE_NAMES,**{c:c.upper() for c in sorted(codes-set(LANGUAGE_NAMES))}}



def parse_blocks(text):
    matches=list(re.finditer(r'^<!-- key: (.*?) -->\s*$',text,re.M));out={}
    for i,m in enumerate(matches):
        out[m.group(1)]=text[m.end():matches[i+1].start() if i+1<len(matches) else len(text)].strip()
    return out


class Catalog:
    def __init__(self,language='en',root=ROOT):
        self.language=language;self.root=Path(root)
        self.english=parse_blocks(self.document('interface','en'))
        self.local=parse_blocks(self.document('interface',language))
        self.entries={**self.english,**{k:v for k,v in self.local.items() if v.strip()}}
    def document(self,name,language=None):
        code=language or self.language
        if not re.fullmatch(r'[a-z]{2}(?:_[A-Z]{2})?',code):code='en'
        p=self.root/f'{name}_{code}.md'
        if not p.is_file() or not p.read_text(encoding='utf-8').strip():p=self.root/f'{name}_en.md'
        return p.read_text(encoding='utf-8') if p.is_file() else ''
    def __call__(self,key,**values):
        template=self.entries.get(key,self.english.get(key,key))
        return template.format(**values) if values else template
    def translate_literal(self,text):
        if text in self.entries:return self(text)
        # Translate dynamically formatted figure labels from external templates.
        for key,english in self.english.items():
            if '{' not in english or '\n' in english:continue
            fields=re.findall(r'\{(\w+)(?::[^}]+)?\}',english)
            if not fields or len(fields)!=len(set(fields)):continue
            parts=re.split(r'(\{\w+(?::[^}]+)?\})',english)
            pattern=''
            for part in parts:
                m=re.fullmatch(r'\{(\w+)(?::[^}]+)?\}',part)
                pattern+=f'(?P<{m.group(1)}>.+?)' if m else re.escape(part)
            match=re.fullmatch(pattern,text)
            if match:
                translated=re.sub(r'\{(\w+):[^}]+\}',r'{\1}',self.entries.get(key,english))
                try:return translated.format(**match.groupdict())
                except (KeyError,ValueError):pass
        return text
    def figure(self,fig):
        if self.language=='en':return fig
        for artist in fig.findobj(match=FigureText):
            value=artist.get_text()
            if value:artist.set_text(self.translate_literal(value))
        return fig
