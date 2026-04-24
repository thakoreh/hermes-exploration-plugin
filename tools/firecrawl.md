---
id: firecrawl
name: Firecrawl
description: Turn entire websites into clean markdown or structured data. Handles JavaScript-rendered pages, rate limits, and anti-scraping automatically.
category: scraping
url: https://firecrawl.dev
pricing: freemium
alternatives: [crawlfe, scrapeops, apify]
quality_score: 9.0
discovery_context: "Needed to extract content from a JavaScript-heavy SPA for RAG pipeline"
discovered_by: hermes-content
discovered_at: 2026-04-15
last_verified: 2026-04-24
integration_notes: |
  API: POST https://api.firecrawl.dev/v0/scrape
  API: POST https://api.firecrawl.dev/v0/crawl
  Best for: RAG data pipelines, competitor research, content aggregation.
  Handles bot detection, JS rendering, returns clean markdown.
  Free: 500 pages/month
flags: [has-api, has-free-tier, supports-webhook]
---

## Overview

Firecrawl is a web scraping API that handles the hard parts: JavaScript rendering, rate limiting, proxy rotation, and extracting clean content. Give it a URL or sitemap, get back clean markdown or structured JSON.

## Key Features

- Single URL scrape → clean markdown/HTML/JSON
- Full site crawl → all pages, respects robots.txt
- JavaScript rendering (like Puppeteer but as a service)
- Removes ads, nav, footers — content only
- Returns metadata: title, description, og tags, links

## Pricing

Free tier: 500 pages/month
Pay-as-you-go: $0.01-$0.05 per page depending on features
Enterprise: custom limits
