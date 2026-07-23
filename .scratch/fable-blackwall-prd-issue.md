## Problem Statement

The portfolio site's content has drifted from reality — the projects grid still leads with CI/CD classroom exercises while newer work (NLP final project, GPT challenge, expense management system, well-being visualisation) is invisible, and the LinkedIn-sourced copy is a first-draft seed. Meanwhile the hidden cyberpunk theme ("netrunner") is a light cyan/magenta reskin that doesn't deliver the Blackwall fantasy its unlock sequence promises: no red/black identity, no distortion, no atmosphere. Dark mode also reads as a generic GitHub-dark clone with green accents, giving peers no hint of the site's personality.

## Solution

Refresh the seeded content one-shot from LinkedIn (core: headline, hero bio, about, work/edu timeline) and GitHub (a curated six-project list with real descriptions), with a `flask refresh-content` CLI so an existing local database can adopt the new content without losing photos or the CV PDF. Rename the hidden theme from `netrunner` to `blackwall` and rebuild it as a proper Blackwall experience: red/black palette, dense scanlines, a stronger unlock flash, and a continuous fullscreen raw-WebGL atmosphere (noise, warp, chromatic aberration) that runs only while the theme is active, degrades adaptively on weak devices, and falls back to CSS-only under `prefers-reduced-motion`. Dark mode picks up red/black accents (no WebGL, no glitch) so it feels edgier without spoiling the egg. Light mode stays recruiter-safe and untouched. Discovery gets two quiet breadcrumbs — a glitching footer glyph and a one-time terminal hint — while `theme icebreak` remains the canonical unlock, persisted in localStorage.

## User Stories

1. As a recruiter, I want the light theme to remain clean and professional, so that my first impression of Hugo is credible.
2. As a recruiter, I want the projects page to show Hugo's current, real work with accurate descriptions, so that I can assess his abilities quickly.
3. As a recruiter, I want the CV timeline and hero bio to reflect Hugo's up-to-date LinkedIn experience, so that the site and his resume tell the same story.
4. As a recruiter, I want no distracting distortion effects in the default themes, so that I can read the content without friction.
5. As a peer developer, I want dark mode to carry red/black cyberpunk accents, so that the site feels distinctive even before I find the egg.
6. As a peer developer, I want a subtle glitching glyph in the footer, so that I get a hint something is hidden.
7. As a peer developer, I want a one-time terminal hint on my first visit, so that I'm nudged toward exploring the terminal commands.
8. As a peer developer, I want `theme icebreak` to run a breach sequence and flash into the Blackwall theme, so that discovery feels like an event.
9. As a peer developer, I want the Blackwall theme to be red/black with dense scanlines and a continuous WebGL atmosphere, so that the unlocked mode feels genuinely different from dark mode.
10. As a peer developer, I want the Blackwall theme to persist across visits via localStorage, so that I don't have to re-unlock it every time.
11. As a peer developer who previously unlocked netrunner, I want my stored theme migrated to blackwall, so that I'm not silently kicked back to light mode.
12. As a visitor on a low-powered device, I want the WebGL atmosphere to lower its quality adaptively, so that the site stays smooth.
13. As a visitor with `prefers-reduced-motion` set, I want a CSS-only Blackwall with no WebGL or animation-heavy effects, so that the site respects my accessibility preference.
14. As a visitor, I want the WebGL canvas to never intercept clicks or scrolling, so that the atmosphere is purely decorative.
15. As a visitor, I want the theme toggle to keep swapping light and dark (and exit Blackwall), so that I can always get back to a normal look.
16. As a visitor, I want the WebGL loop to pause when the tab is hidden, so that it doesn't waste battery in the background.
17. As any visitor, I want the terminal's `projects` command to list the current project set, so that the terminal and the projects page agree.
18. As Hugo (site owner), I want a `flask refresh-content` command that replaces settings, about, timeline, and projects with the new seed while keeping photos and CV PDF, so that my existing local database adopts the refresh without data loss.
19. As Hugo, I want all content still editable via the admin dashboard afterwards, so that the refresh is a starting point, not a lock-in.
20. As Hugo, I want the README to document the Blackwall egg, the rename, and the refresh command, so that future contributors (human or agent) understand the system.

## Implementation Decisions

- One-shot content refresh only: no live LinkedIn or GitHub API integration, no scraper service. Content is baked into the seed module.
- LinkedIn scope is core-only: name, tagline, hero bio, subtitle lines, long bio, work/education timeline. No recommendations, certification dumps, or full skills mirror.
- Curated six-project list (display order): PromptInjectionTester (featured), PersonalWebsite, NLP_Final_project, GPTchallenge, ExpenseManagementSystem, WellBeingVisualisation — each with a real description derived from its repository, replacing the CI/CD exercise entries.
- A Flask CLI command `refresh-content` deletes and re-inserts SiteSettings, AboutContent, TimelineEntry, and Project rows from the seed data, leaving Photo rows, uploaded files, and admin auth untouched.
- Theme identifier renamed `netrunner` → `blackwall` across the pre-paint allowlist, theme manager, stylesheet selectors, and terminal unlock; `theme netrunner` remains accepted as a legacy alias for the icebreak sequence. Stored `netrunner` preference migrates to `blackwall` on read.
- `theme icebreak` remains the canonical unlock; theme preference (including blackwall) persists in localStorage; the nav toggle only swaps light/dark and thereby exits Blackwall.
- Dark theme accent shifts from green to a red/black family; polish only — no scanlines, glitch, or WebGL outside Blackwall. Light theme tokens unchanged.
- Blackwall visual chrome: red/black tokens, denser scanline overlay, stronger red unlock flash, updated breach copy (BLACKWALL theme pack).
- Continuous atmosphere implemented as one fullscreen fragment shader on raw WebGL (no Three.js, no npm dependency), mounted as a fixed, pointer-events-none canvas in the shared layout, started only when the blackwall theme is active and torn down on theme exit.
- Adaptive quality: device-pixel-ratio capping and frame-time-based downscaling; loop pauses when the document is hidden; `prefers-reduced-motion: reduce` skips WebGL entirely (CSS-only Blackwall).
- Two discovery breadcrumbs: a footer glyph with a hover glitch, and a once-per-browser muted terminal hint line (localStorage-flagged) that nudges toward hidden themes without naming the command.

## Testing Decisions

- Single test seam: the existing Flask test client → rendered public HTML, matching the current public behaviour suite. Tests assert externally observable outcomes only.
- New/updated assertions: refreshed seed strings appear on home/about/projects/cv; the shared layout allowlists `blackwall` and mounts the Blackwall canvas element; the string `netrunner` no longer appears in public HTML responses.
- Existing tests asserting old seeded titles are updated to the new content.
- Explicitly not tested: WebGL rendering output, shader behaviour, frame rates, browser localStorage flows, or any network fetches (there are none).
- Prior art: the existing public page tests that assert seeded names, project titles, and timeline entries.

## Out of Scope

- Live LinkedIn/GitHub sync or any scheduled content import.
- WebGL or heavy glitch effects on the light or dark themes.
- Making Blackwall a visible entry in the theme toggle.
- New public routes or pages, CMS schema changes, or admin dashboard redesign.
- Deployment and infrastructure changes.

## Further Notes

- Work happens on the `fable-enhancements` branch; done means a cohesive, merge-ready vertical slice (content + dark accents + full Blackwall egg), not an open-ended effects playground.
- The Blackwall shader is the showpiece of this slice; it should feel like crossing a boundary relative to dark mode, per the locked "hard line" decision: dark mode gets palette only, Blackwall alone gets motion and distortion.
