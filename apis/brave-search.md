---
id: brave-search
name: Brave Search API
description: Independent web search API from the Brave browser company. Privacy-respecting, no tracking, fast. Great alternative to Google for AI search-augmented applications.
category: search
url: https://brave.com/search/api
pricing: freemium
alternatives:
  - tavily
  - serpapi
  - serper
quality_score: 8.0
discovery_context: Needed a privacy-respecting search API without Google's tracking for an AI research assistant
discovered_by: hermes-content
discovered_at: 2026-04-25
last_verified: 2026-04-25
flags:
  - has-api
  - has-free-tier
API: https://api.search.brave.com/res/v1
Free: 2,000 queries/month (free tier)
Pricing: $5-$15/10K queries after free tier
---

# Brave Search API

Brave Search API provides independent, privacy-respecting web search. No Google/Bing dependency, no tracking, fast. Results are高质量 and the API is simple to integrate.

## Key Features

- **Web search** — standard search results with snippets
- **Images search** — image results
- **News search** — recent news articles
- **Summarizer** — AI-generated summaries of top results (similar to Google AI Overviews)
- **No tracking** — Brave's core value prop, no user data collection
- **Real-time** — fast index refresh, recent results available

## API Example

```python
import requests
headers = {
    "Accept": "application/json",
    "X-Subscription-Token": "YOUR_API_KEY"
}
params = {"q": "latest AI agent frameworks 2026"}
r = requests.get(
    "https://api.search.brave.com/res/v1/web/search",
    headers=headers,
    params=params
)
data = r.json()
for result in data["web"]["results"]:
    print(result["title"], result["url"])
```

## Brave Summarizer

Enable AI summaries of top results:
```python
params = {
    "q": "how do AI agents work",
    "summary": True  # returns AI summary
}
```

## Pricing

- **Free**: 2,000 queries/month
- **Basic**: $5/10K queries beyond free tier
- **Standard**: $15/10K queries for higher rate limits

## vs Tavily

| Feature | Brave | Tavily |
|---------|-------|--------|
| Results | Raw web | AI-optimized |
| Summaries | Yes (basic) | Yes (deeper) |
| Free tier | 2K/mo | 1K/mo |
| Best for | General search | AI/RAG apps |
