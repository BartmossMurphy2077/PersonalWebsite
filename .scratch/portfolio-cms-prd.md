# PRD: Portfolio CMS Redesign

## Problem Statement

Hugo Kotuc's personal website is a single static HTML page built in roughly an hour and left unfinished. It does not present a professional portfolio experience for recruiters, does not showcase projects or CV content in depth, lacks personal photos, and offers no way to update content without editing code. The site needs to evolve into a multi-page, personality-driven portfolio that remains credible to hiring managers while feeling distinctive to developer peers — with a private admin dashboard so Hugo can manage all content himself.

## Solution

Rebuild the site as a Flask-backed portfolio CMS running locally (deploy later). The public site gains four pages (Home, About, Projects, CV) with a professional-yet-quirky design: split hero with credentials on the left and interactive dev-themed widgets on the right, terminal-inspired visual accents, and terminal-boot page transitions. A password-protected admin dashboard at `/admin` lets Hugo manage site settings, photos, CV timeline entries, projects, and about-page copy through simple forms backed by SQLite and local file uploads. Recruiters get fast access to projects and a downloadable CV; peers get playful interactions that reward exploration.

## User Stories

### Public site — general

1. As a recruiter, I want to understand who Hugo is within 5 seconds of landing, so that I can decide whether to keep reading.
2. As a recruiter, I want obvious buttons to view projects and download a CV, so that I can evaluate fit quickly without hunting through the site.
3. As a peer developer, I want the site to feel distinctive and interactive, so that I enjoy exploring it beyond the minimum hiring information.
4. As any visitor, I want consistent navigation across all pages, so that I can move between Home, About, Projects, and CV without getting lost.
5. As any visitor, I want contact links (LinkedIn, GitHub) in the footer on every page, so that I can reach Hugo without a dedicated contact page.
6. As any visitor, I want the site to work on mobile and desktop, so that I can browse from any device.
7. As any visitor, I want page transitions that feel polished and on-brand, so that navigation feels intentional rather than jarring full reloads.

### Home page

8. As a recruiter, I want to see Hugo's name, role, and a professional photo immediately, so that I can put a face to the credentials.
9. As a recruiter, I want a short hero bio summarizing his background, so that I understand his current position and focus areas.
10. As a recruiter, I want a "View Projects" call-to-action, so that I can jump to his work.
11. As a recruiter, I want a "Download CV" call-to-action, so that I can save his resume offline.
12. As a peer, I want a typewriter-style rotating subtitle cycling through lines like current role, skills, and personality hooks, so that the hero feels alive.
13. As a peer, I want a mini terminal widget that responds to preset commands (`whoami`, `skills`, `projects`), so that I can play with an interactive element.
14. As any visitor, I want a featured project teaser on the home page, so that I get a preview before visiting the full projects page.
15. As any visitor, I want the hero split into a professional left panel and a playful right panel, so that the page serves both audiences at once.

### About page

16. As a recruiter, I want a longer bio than the hero provides, so that I understand Hugo's background in more detail.
17. As a peer, I want to see multiple photos of Hugo, so that the page feels personal and human.
18. As any visitor, I want interests and hobbies represented, so that I get a sense of personality beyond work.
19. As Hugo (site owner), I want about-page content editable from the admin dashboard, so that I can update my story without touching code.

### Projects page

20. As a recruiter, I want a grid or list of project cards with title, description, and tech stack, so that I can assess technical breadth quickly.
21. As a recruiter, I want links to GitHub repos or live demos where available, so that I can verify the work.
22. As a peer, I want project cards to look polished with thumbnails, so that the portfolio feels curated.
23. As any visitor, I want projects ordered intentionally (e.g. featured first), so that the best work appears at the top.
24. As Hugo, I want to add, edit, and delete projects from the admin dashboard, so that I can keep the portfolio current.

### CV page

25. As a recruiter, I want a timeline of education and employment, so that I can scan career progression.
26. As a recruiter, I want bullet points under each timeline entry, so that I understand responsibilities and achievements.
27. As a recruiter, I want a downloadable CV PDF, so that I can share it internally or attach it to applications on Hugo's behalf.
28. As any visitor, I want skills displayed clearly, so that I can see technical competencies at a glance.
29. As Hugo, I want to manage timeline entries and upload a new CV PDF from the admin dashboard, so that my resume stays up to date.

### Visual design and interactions

30. As a recruiter, I want a clean, professional layout for main content areas, so that the site feels trustworthy.
31. As a peer, I want dev-aesthetic accents (dark terminal panel, monospace type, green glow), so that the site feels like a developer built it.
32. As any visitor, I want a cohesive color palette (light content areas, navy primary, green dev accents), so that the design feels intentional.
33. As any visitor, I want terminal-boot-style transitions between pages (brief scanline flash, then content appears), so that navigation reinforces the dev theme.
34. As any visitor, I want hover and micro-interactions on buttons and cards, so that the site feels responsive and modern.
35. As a peer, I want the terminal widget on the home page to use the same visual language as page transitions, so that the experience feels unified.

### Admin dashboard — access and security

36. As Hugo, I want to sign in to `/admin` with a single password, so that only I can edit content.
37. As Hugo, I want the admin password stored in an environment variable, so that credentials are not committed to the repository.
38. As Hugo, I want a logout button, so that I can end my session on a shared machine.
39. As any public visitor, I want admin routes blocked without authentication, so that content cannot be modified by strangers.
40. As Hugo, I want unauthenticated requests to `/admin` redirected to a login page, so that the flow is obvious.

### Admin dashboard — site settings

41. As Hugo, I want to edit my display name from the admin dashboard, so that I can fix typos without redeploying.
42. As Hugo, I want to edit my tagline and hero bio, so that the home page messaging stays current.
43. As Hugo, I want to manage the list of rotating subtitle lines, so that I can add or remove typewriter text.
44. As Hugo, I want to edit social links (GitHub, LinkedIn), so that footer and hero links stay accurate.
45. As Hugo, I want to configure terminal widget command responses, so that I can update what `whoami`, `skills`, and `projects` return.

### Admin dashboard — photos

46. As Hugo, I want to upload profile and gallery photos, so that they appear on the public site.
47. As Hugo, I want to designate which photo is the main hero/profile image, so that I control first impressions.
48. As Hugo, I want to delete photos I no longer want displayed, so that the gallery stays curated.
49. As Hugo, I want uploaded images stored on disk with references in the database, so that they persist across restarts.

### Admin dashboard — CV / experience

50. As Hugo, I want to add timeline entries with title, organization, start/end dates, and bullet points, so that my CV page reflects reality.
51. As Hugo, I want to edit and reorder timeline entries, so that I can keep chronology correct.
52. As Hugo, I want to delete outdated timeline entries, so that old roles do not linger.
53. As Hugo, I want to upload a CV PDF file, so that the public download button serves the latest version.
54. As Hugo, I want to replace an existing CV PDF, so that I do not need developer help to update it.

### Admin dashboard — projects

55. As Hugo, I want to create a project with title, description, tech stack tags, GitHub URL, demo URL, and thumbnail, so that each card is complete.
56. As Hugo, I want to mark a project as featured, so that it surfaces on the home page teaser.
57. As Hugo, I want to edit existing projects, so that descriptions and links stay accurate.
58. As Hugo, I want to delete projects, so that unfinished or embarrassing work can be removed.
59. As Hugo, I want to upload a project thumbnail image, so that cards look visual rather than text-only.

### Admin dashboard — about page

60. As Hugo, I want to edit the long-form about bio, so that I can tell my story in my own words.
61. As Hugo, I want to edit interests/hobbies text, so that the about page personality section stays current.

### Admin dashboard — UI

62. As Hugo, I want the admin UI to use a dark sidebar with section navigation, so that it feels like a dev tool.
63. As Hugo, I want form areas on a light background, so that long text is easy to read while editing.
64. As Hugo, I want monospace headers and green accent on active nav and save actions, so that the dashboard matches the public site's dev aesthetic.
65. As Hugo, I want clear success feedback after saving, so that I know my changes were persisted.
66. As Hugo, I want validation errors shown inline, so that I can fix mistakes without losing my input.

### Data and seeding

67. As Hugo, I want the database seeded with content from the existing single-page site on first run, so that the new site is not empty on day one.
68. As Hugo, I want the database file and uploads directory gitignored, so that local data and images are not accidentally committed.
69. As Hugo, I want a `.env.example` documenting required environment variables, so that setup is reproducible.

### Development workflow

70. As Hugo, I want to run the entire stack locally with Flask's dev server, so that I can develop without deployment infrastructure.
71. As Hugo, I want all work done on the `adding-details` feature branch, so that `main` stays stable until the redesign is ready.

## Implementation Decisions

### Architecture

- Evolve the existing Flask application from a static file server into a dynamic CMS. The Flask app becomes the single entry point for both public pages and the admin dashboard.
- Use SQLite as the database (zero-config, appropriate for a single-user local portfolio). Store uploaded files (images, CV PDF) on the local filesystem; store file paths in the database.
- Render public pages with server-side templates populated from database content. Retain separate routes for Home, About, Projects, and CV rather than a client-side SPA.
- Keep quirky interactions (typewriter, terminal widget, page transitions) in frontend JavaScript/CSS; their behavior is configurable via site settings where practical (subtitle lines, terminal responses) but layout and animation logic remain in code.

### Data model (conceptual)

- **SiteSettings** — singleton or key-value store: name, tagline, hero bio, social links, rotating subtitle lines (JSON list), terminal command responses (JSON map), CV PDF path.
- **Photo** — id, filename/path, alt text, is_primary flag, display order.
- **TimelineEntry** — id, title, organization, start date, end date (nullable for current), bullet points (JSON list), display order.
- **Project** — id, title, description, tech stack tags (JSON list), github_url, demo_url, thumbnail path, is_featured flag, display order.
- **AboutContent** — singleton: long bio, interests text.

### Authentication

- Single admin password from environment variable (e.g. `ADMIN_PASSWORD`).
- Flask server-side session after successful login. All `/admin/*` routes except login require an authenticated session.
- Use a secret key from environment for session signing (e.g. `SECRET_KEY`).

### Public routes

- `GET /` — Home page with split hero, featured project teaser, dynamic content.
- `GET /about` — About page with bio, gallery photos, interests.
- `GET /projects` — All projects as cards.
- `GET /cv` — Timeline, skills, CV PDF download link.
- `GET /uploads/<filename>` or equivalent — Serve uploaded images and PDFs.

### Admin routes

- `GET/POST /admin/login` — Login form.
- `POST /admin/logout` — End session.
- `GET /admin` — Dashboard home / redirect to first section.
- CRUD routes for each section: site settings, photos, timeline entries, projects, about content. Standard pattern: list view, add form, edit form, delete action.

### Frontend structure

- Shared layout template: navigation (Home, About, Projects, CV), footer with social links, transition wrapper, shared CSS/JS.
- Page-specific templates extending the layout.
- Shared assets: global stylesheet (professional light theme + dev accent variables), global JS (page transition boot sequence, shared utilities), page-specific JS for home terminal and typewriter.
- CSS custom properties for colors: navy primary, off-white backgrounds, green terminal accent, dark panel for terminal/hero right side.

### Hero layout (Home)

- Left column: primary photo, name, role/tagline, hero bio, two CTA buttons (View Projects, Download CV).
- Right column: typewriter rotating subtitles + interactive terminal widget with preset commands.

### Page transitions

- On every page load/navigation, play a brief terminal-boot animation (scanline flash or similar) then fade/slide content in. Implement via a shared JS module that runs on DOMContentLoaded and a CSS animation layer. Full page reloads are acceptable (no client-side router).

### Admin UI

- Dark sidebar with five nav items: Site Settings, Photos, CV / Experience, Projects, About.
- Light content panel with forms. Monospace font for section titles. Green highlight for active nav item and primary save buttons.
- Use server-rendered HTML forms (no separate admin SPA).

### Configuration and secrets

- `python-dotenv` or equivalent to load `.env` in development.
- `.env.example` lists `ADMIN_PASSWORD`, `SECRET_KEY`, and any other required vars.
- Gitignore: `.env`, `*.db`, `uploads/`, `BackEnd/venv/`.

### Dependencies (expected)

- Flask (existing)
- Flask-SQLAlchemy or similar ORM for SQLite
- Flask-Login or minimal session-based auth
- python-dotenv
- Werkzeug secure filename handling for uploads

### Seed data

- On first database initialization, seed from existing site content: Hugo Kotuc, IE University 3rd year, Kempelen Institute, skills (Java, Python, C, AI Agents, RAG Solutions), GitHub and LinkedIn URLs, existing hero bio text.

### Branch and scope

- All implementation on `adding-details` branch.
- Local development only; production deployment explicitly deferred.

## Testing Decisions

### What makes a good test

- Test **external behavior** at the HTTP boundary: request a route, assert on status code and response body content. Do not test internal implementation details (e.g. specific ORM query shapes, template variable names).
- Tests should be deterministic: use an isolated test database and temporary upload directory, not the developer's live `portfolio.db`.

### Testing seam (proposed — one seam)

**Single seam: Flask application HTTP layer** using pytest and Flask's test client. This is the highest practical seam for this codebase — there are no existing lower-level test patterns to extend, and E2E browser tests would be overkill for v1.

All tests exercise the app through HTTP:

| Area | Behavior to assert |
|------|-------------------|
| Public pages | `GET /`, `/about`, `/projects`, `/cv` return 200 and contain seeded content (name, project title, timeline entry) |
| CV download | `GET` CV PDF route returns file with correct content-type |
| Auth gate | `GET /admin` without session redirects to login; with valid login session returns 200 |
| Login | `POST /admin/login` with correct password sets session; wrong password returns error |
| Admin CRUD | After authenticated `POST` to create/edit a project, `GET /projects` reflects the change |
| Photo upload | After authenticated upload, public about/home page references the image URL and file is served |
| Logout | After logout, admin routes are blocked again |

### Test infrastructure

- pytest as test runner.
- Flask app factory or test config that points to in-memory SQLite (or temp file) and temp uploads dir.
- Fixtures: `app`, `client`, `authenticated_client` (logs in before each test).
- No prior test art exists in the repo; establish conventions in a `tests/` directory at the BackEnd level.

### Out of scope for tests in v1

- Visual regression / screenshot tests for animations and transitions.
- JavaScript unit tests for terminal widget (behavior is secondary to CMS correctness).
- Load or performance testing.

## Out of Scope

- Production deployment (Railway, Render, VPS, etc.) — deferred until local CMS is complete.
- OAuth / GitHub login for admin.
- Multi-user roles or collaborator accounts.
- WYSIWYG page builder or drag-and-drop layout editor.
- Editing animations, transitions, or terminal UI structure from the admin dashboard.
- Dedicated Contact page (footer links suffice).
- Client-side SPA framework (React, Vue) or static site generator migration.
- GitHub API integration for live commit stats.
- Page visibility toggles (v2 idea).
- Email contact form.
- Internationalization / multiple languages.
- Blog or writing section.

## Further Notes

- **Audience priority**: Recruiters first, peers second. Professional clarity in hero and CV/projects; quirk lives in terminal widget, typewriter, transitions, and about-page personality.
- **Visual direction**: Clean professional base (Option A) blended with dev aesthetic accents (Option C mix) — not full dark mode everywhere.
- **Existing codebase**: Currently Flask serves a single static `index.html` with inline CSS. The redesign replaces this with templated dynamic pages but should preserve the existing bio copy and links as seed data.
- **Content placeholders**: Hugo may not have photos or a CV PDF ready on day one. Admin and public templates should handle missing primary photo and missing CV PDF gracefully (placeholder avatar, disabled or hidden download button with clear admin prompt).
- **After this PRD**: Run `/to-issues` to split into independently implementable issues. Each `/implement` session should receive this PRD plus a single issue.
- **Setup note**: Matt Pocock skills issue-tracker config (`docs/agents/`) has not been run yet; this PRD is published as a GitHub issue using default `ready-for-agent` label vocabulary.
