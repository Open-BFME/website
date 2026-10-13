# OpenBFME website

OpenBFME's community portal for the Battle for Middle-earth I and II C++ reconstructions and the Rise of the Witch-king Godot alpha. Static HTML/CSS, no package installation or client-side JavaScript.

```sh
python3 -m unittest discover -s tests -v
python3 tools/build_site.py
python3 -m http.server 8765 --bind 127.0.0.1 --directory dist
```

Open http://127.0.0.1:8765/ to inspect the exact publishable files. Deploy **only `dist/`**, never the repository root: the repository can also contain ignored local studies. The approved archive artwork is committed under `assets/art/`; the earlier menu prototype and private review screenshots are not part of the release. Artwork from T3A:Online and Rise of the Witch-king is used with the project owner's confirmed permission. Publication here does not grant third parties a reuse license for that artwork.

The displayed 69.85% and 79.21% are a **12 October 2026 snapshot of each game's code in C++**, not overall game completion. Current progress reports are linked on the page. The Godot alpha requires original game files.

For a Cloudflare Pages direct upload, create the `openbfme` project once and deploy the generated directory with `wrangler pages deploy dist --project-name openbfme --branch main`. Attach the apex domain in the Pages custom-domain settings. Verify the live HTTPS page and its static assets after deployment.
