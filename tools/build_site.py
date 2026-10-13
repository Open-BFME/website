#!/usr/bin/env python3
"""Copy only the approved one-page site into a deployable directory."""
from pathlib import Path
from shutil import copy2, copytree, rmtree

root = Path(__file__).resolve().parents[1]
output = root / 'dist'
if output.exists():
    rmtree(output)
for name in ('index.html', 'favicon.svg', 'robots.txt', 'sitemap.xml',
             'assets/portal.css', 'assets/og-openbfme.png'):
    source = root / name
    destination = output / name
    destination.parent.mkdir(parents=True, exist_ok=True)
    copy2(source, destination)
copytree(root / 'assets/art', output / 'assets/art')
print(f'Built {output}')
