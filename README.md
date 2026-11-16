# Mr AI Decoder website

The site for the Instagram page [@mr.ai.decoder](https://www.instagram.com/mr.ai.decoder/): claim checks on AI and jobs, one page per episode, and the free files promised in the Reels.

## Folders
| | |
|---|---|
| `public/` | The live site, exactly as served. Plain HTML and CSS, no build step on the host. |
| `src/` | Page templates (`*.html`), the character drawings (`art/`, from `studio/world/guy.js` and `claude.js`) and `build.py`, which turns the templates into `public/`. |
| `public/files/` | Free files linked from the Reels and the DM replies. |

## Change the site
1. Edit a template in `src/` (or add one, e.g. `src/ep6.html`, copied from `ep5.html`).
2. `python src/build.py` (writes `public/`).
3. Look at `public/index.html` in a browser.
4. `python push_site.py "what changed"` (from the `website` folder; `--dry-run` first lists the changes).

## Hosting (free)
Cloudflare Pages, connected to the GitHub repo `adityan-nainar/jobsarenawebsite`, branch `main`.
Settings: no framework preset, no build command, build output directory `public`. Every push redeploys.

## Rules
- Every number on a page has a source and a grade (A to D); our assumptions are labelled as ours.
- The site never says or implies that the Reels or the site were made by AI.
- Chad and Claude are our animated characters; the footer says the page is not affiliated with Anthropic.
- Fonts: Inter, Lora and JetBrains Mono, all SIL Open Font License (licences in `public/assets/fonts/`).
