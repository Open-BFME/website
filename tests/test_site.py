from html.parser import HTMLParser
from pathlib import Path
import json
import re
import subprocess
import sys
import unittest
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]


class PageLinks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.assets = []
        self.anchors = []
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get('id'):
            self.ids.add(attrs['id'])
        for name in ('href', 'src'):
            value = attrs.get(name, '')
            if value.startswith('#'):
                self.anchors.append(value[1:])
            elif value and not value.startswith(('https://', 'http://', 'mailto:')):
                self.assets.append(value.lstrip('/'))


class SiteTest(unittest.TestCase):
    def test_local_assets_and_navigation(self):
        page = (ROOT / 'index.html').read_text()
        links = PageLinks()
        links.feed(page)
        for path in links.assets:
            self.assertTrue((ROOT / path).is_file(), path)
        for anchor in links.anchors:
            self.assertIn(anchor, links.ids)
        css = (ROOT / 'assets/portal.css').read_text()
        for path in re.findall(r'url\(([^)]+)\)', css):
            self.assertTrue((ROOT / 'assets' / path.strip('"\' ')).is_file(), path)
        self.assertNotIn('\u2014', page + css)
        self.assertNotIn('local-reference/', page + css)
        self.assertNotIn('local-bfme/', page + css)

    def test_sources_and_qualified_snapshot(self):
        page = (ROOT / 'index.html').read_text()
        for fragment in ('Open-BFME/Open-BFME-1', 'Open-BFME/Open-BFME-2',
                         'Open-BFME/openbfme-godot', 'discord.gg/wCvA2XqPUT',
                         '69.85%', '79.21%', '2026-10-12',
                         'code in C++', 'not an estimate of overall game completion'):
            self.assertIn(fragment, page)

    def test_search_metadata(self):
        page = (ROOT / 'index.html').read_text()
        self.assertEqual(page.count('<h1 '), 1)
        self.assertNotIn('noindex', page)
        self.assertIn('<link rel="canonical" href="https://openbfme.org/">', page)
        self.assertIn('property="og:image" content="https://openbfme.org/assets/og-openbfme.png"', page)
        self.assertIn('name="twitter:card" content="summary_large_image"', page)
        self.assertRegex(page, r'<meta name="description" content="[^"]{80,170}">')
        schema = re.search(r'<script type="application/ld\+json">(.*?)</script>', page)
        self.assertIsNotNone(schema)
        self.assertEqual({node['@type'] for node in json.loads(schema.group(1))['@graph']},
                         {'Organization', 'WebSite'})
        sitemap = ElementTree.parse(ROOT / 'sitemap.xml')
        self.assertEqual(sitemap.findtext('{*}url/{*}loc'), 'https://openbfme.org/')
        self.assertIn('Sitemap: https://openbfme.org/sitemap.xml', (ROOT / 'robots.txt').read_text())
        self.assertIn('# OpenBFME', (ROOT / 'llms.txt').read_text())
        self.assertIn('https://github.com/Open-BFME/', (ROOT / 'llms.txt').read_text())
        self.assertIn('<meta name="robots" content="noindex">', (ROOT / '404.html').read_text())

    def test_deployment_contains_only_public_files(self):
        subprocess.run([sys.executable, 'tools/build_site.py'], cwd=ROOT, check=True,
                       capture_output=True)
        files = {str(p.relative_to(ROOT / 'dist')) for p in (ROOT / 'dist').rglob('*') if p.is_file()}
        artwork = {str(p.relative_to(ROOT)) for p in (ROOT / 'assets/art').glob('*.png')}
        self.assertEqual(files, {'index.html', '404.html', 'favicon.svg', 'robots.txt',
                                 'sitemap.xml', 'llms.txt', 'assets/portal.css',
                                 'assets/og-openbfme.png'} | artwork)
        self.assertEqual(len(artwork), 17)
        self.assertNotIn('local-reference', ' '.join(files))


if __name__ == '__main__':
    unittest.main()
