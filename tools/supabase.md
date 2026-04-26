---
id: supabase
name: Supabase
description: Open-source Firebase alternative. Postgres database, auth, realtime subscriptions, storage, and edge functions in one platform.
category: database
url: https://supabase.com
pricing: freemium
alternatives: [firebase, planetscale, xata, neon]
quality_score: 9.1
discovery_context: Needed a scalable Postgres database with built-in auth and realtime capabilities for a SaaS app
discovered_by: hermes-backend
discovered_at: 2026-04-26
last_verified: 2026-04-26
integration_notes: |
  Perfect for: SaaS apps needing auth + DB + realtime. Use Supabase client JS/Flutter/Dart.
  Edge Functions: Deno runtime for serverless logic.
  Realtime: PostgreSQL changes stream to clients via websockets.
flags: [has-api, open-source, has-free-tier, has-edge-functions, has-realtime]
---

## Overview

Supabase is an open-source Firebase alternative built on PostgreSQL. It provides a complete backend: database, authentication, file storage, edge functions, and realtime subscriptions — all in one platform with a generous free tier.

## Key Features

- PostgreSQL database with automatic API generation
- Row-level security (RLS) for granular access control
- Built-in authentication with email, OAuth, and magic links
- Realtime subscriptions to database changes
- Edge Functions running Deno
- File storage with CDN and image transformations
- Studio dashboard for database management

## Pricing

Free tier: 500MB database, 1GB storage, 50K monthly active users, 2GB bandwidth
Pro tier: $25/mo for 8GB database, 100GB storage, 100K monthly active users

## How to Use

```bash
npm install @supabase/supabase-js
```

```javascript
import { createClient } from '@supabase/supabase-js'
const supabase = createClient(SUPABASE_URL, SUPABASE_KEY)

// Query
const { data } = await supabase.from('tasks').select('*')

// Realtime subscription
supabase.channel('tasks').on('INSERT', payload => console.log(payload)).subscribe()
```

## Notes

Row-Level Security is powerful but requires careful policy design. Start with RLS enabled from day one.
