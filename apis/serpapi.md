---
id: serpapi
name: SerpAPI
description: Google and Bing search API that returns structured results. Handles CAPTCHA, rate limiting, and proxy rotation. Ideal for building search-augmented AI applications.
category: search
url: https://serpapi.com
pricing: freemium
alternatives:
  - tavily
  - brave-search
  - google-custom-search
quality_score: 8.2
discovery_context: Need structured Google search results for an SEO analysis pipeline without managing proxies/CAPTCHAs
discovered_by: hermes-content
discovered_at: 2026-04-25
last_verified: 2026-04-25
flags:
  - has-api
  - has-free-tier
API: https://serpapi.com/overview
Free: 100 searches/month (no credit card)
Pricing: $50-$500/mo depending on volume
---

# SerpAPI

SerpAPI handles Google and Bing search at scale. It abstracts away proxy rotation, CAPTCHA handling, and rate limiting — you get back clean, structured JSON results.

## Key Features

- **Structured results** — organic, ads, people also ask, reviews, jobs, etc.
- **Google Maps** — local search results with ratings, hours
- **Video and image search** — structured video/image results
- **Trending searches** — real-time trending topics
- **No CAPTCHA** — SerpAPI handles all of that
- **Historical data** — some result pages available with historical data

## API Example

```python
from serpapi import GoogleSearch
params = {
    "q": "best AI coding tools 2026",
    "api_key": "YOUR_API_KEY",
    "engine": "google"
}
search = GoogleSearch(params)
results = search.get_dict()
organic = results["organic_results"]
for r in organic:
    print(r["title"], r["link"])
```

## Use Cases

- SEO competitive analysis
- Price monitoring
- Review aggregation
- Search-augmented RAG (search → extract content → summarize)
- Trend detection

## Pricing

- **Free**: 100 searches/month
- **Basic**: $50/mo for 5,000 searches
- **Pro**: $500/mo for 50,000 searches
