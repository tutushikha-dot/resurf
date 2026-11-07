# Resurf.so Offline Mirror & Local Server

An offline, high-fidelity mirror of [Resurf](https://resurf.so/) — the personal knowledge base and bookmark manager for Mac, iPhone, and iPad.

![Resurf Preview](preview_screenshot.png)

## Overview

This repository contains a full static mirror of `resurf.so`, preserving:
- **All 97 Pages**: Landing page, product tours, comparison sheets (mymind, raindrop, anybox, eagle), all 70+ user guides, changelogs, roadmap, and blog posts.
- **Interactive UI & Dynamic Chunks**: Full Next.js client-side bundles, styles, and custom typography (`.woff2`).
- **Complete Media Assets**: High-resolution screenshots, layered carousel WebP visuals, brand vectors, and all 30+ guide MP4 demonstration videos.
- **Local Network Development Server**: A built-in Python server (`serve.py`) supporting Next.js dynamic image endpoints, clean URLs, Range video streaming, and same-Wi-Fi network previews.

---

## Quick Start

### 1. Run the Local Server

```bash
# Start server on default port (8088 or available):
python3 serve.py

# Or specify a custom port:
python3 serve.py 3000
```

### 2. View in Browser

- **On this computer**: [http://localhost:8088](http://localhost:8088)
- **On another Mac, iPhone, or iPad on the same Wi-Fi**:
  The server prints your local Wi-Fi IP and Bonjour hostname on startup:
  ```text
  http://<YOUR-LOCAL-IP>:8088
  or
  http://<HOSTNAME>.local:8088
  ```

---

## Directory Structure

```text
resurf/
├── index.html                     # Prerendered landing page
├── serve.py                       # Local HTTP & Next.js asset server
├── preview_screenshot.png         # High-res verification preview
├── _next/                         # Compiled JavaScript chunks, CSS & WOFF2 fonts
│   ├── static/chunks/
│   ├── static/css/
│   └── static/media/
├── product-tour/                  # Layered carousel WebP assets & hero demo video
│   ├── bento/
│   ├── cards/
│   └── carousel/2026-10-25-layers/library-similar.mp4
├── brand/                         # Icons, official logos, SVG assets & app screenshots
├── guides/                        # 70+ interactive guides & 30+ demonstration MP4 video clips
│   ├── clips/
│   └── shots/
├── compare/                       # Comparison landing pages (mymind, raindrop, anybox, eagle)
├── blog/                          # All blog articles and migration guides
├── api/                           # Prerendered JSON endpoints (e.g. /api/native-version)
├── about/, changelogs/, roadmap/, download/, faq/, ios/, presskit/, privacy/, terms/, etc.
└── external/                      # Offline cached third-party assets (e.g. Twitter/X avatars)
```

---

## License & Attribution

Mirror for offline documentation and study purposes. Original content, trademarks, and brand assets are the property of [Resurf](https://resurf.so/).
