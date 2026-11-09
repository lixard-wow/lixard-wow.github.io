# lixard-wow.github.io

User guides for Lixard's World of Warcraft addons, published at https://lixard-wow.github.io.

Plain HTML and CSS, served by GitHub Pages from the `main` branch. No build step on the server.

| Page | Folder |
|---|---|
| Home (every addon, with GitHub and CurseForge links) | `index.html` |
| LixardUI (in development) | `lixardui/` |
| Plateau (beta) | `plateau/` |
| Profession Knowledge Treasures | `profession-knowledge-treasures/` |
| CharacterStats | `characterstats/` |
| HealerMana | `healermana/` |
| SmartAssist | `smart-assist/` |
| Auto Expansion Filter | `auto-expansion-filter/` |
| Mark of the Tank (redirects to SmartAssist) | `mark-of-the-tank/` |

Pages are generated: edit `_src/build.py` (home list) or `_src/guides/<slug>.html` (guide text), then run `python _src/build.py .` from the repo root and copy `_src/site.css` to `assets/site.css`. `_src/` is not linked from the site.

Shared styles live in `assets/site.css`. Bump the `?v=` number on the stylesheet link in every page when it changes.
