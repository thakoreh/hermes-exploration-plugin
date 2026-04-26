---
id: planetscale
name: PlanetScale
description: Serverless MySQL platform. Branching for databases, horizontal scaling, and non-blocking schema changes.
category: database
url: https://planetscale.com
pricing: freemium
alternatives: [supabase, neon, xata, aurora]
quality_score: 8.8
discovery_context: Needed a MySQL-compatible database with Git-like branching for staging/production parity
discovered_by: hermes-backend
discovered_at: 2026-04-26
last_verified: 2026-04-26
integration_notes: |
  Best for: MySQL workloads needing serverless scale, branching workflows.
  Use Vitess under the hood — MySQL protocol compatible.
flags: [has-api, serverless, has-free-tier, has-branch-deployments]
---

## Overview

PlanetScale is a serverless MySQL platform that brings Git-like branching to database workflows. Built on Vitess, it handles horizontal scaling, non-blocking schema changes, and provides production-grade reliability without database ops overhead.

## Key Features

- Database branching: create dev/staging branches instantly
- Non-blocking schema changes: ALTER TABLE without downtime
- Serverless connections: no connection pool management
- Horizontal read scaling
- Built-in CLI (pscale)
- Deploy requests for schema review

## Pricing

Free tier: 1 development branch, 1 production branch, 1B row reads/month
Scaler tier: $29/mo for production branches with more resources

## How to Use

```bash
npm install @planetscale/database
```

```javascript
import { Client } from '@planetscale/database'

const client = new Client({
  url: 'https://aws.connect.psdb.cloud',
  username: 'YOUR_USERNAME',
  password: 'YOUR_PASSWORD',
})

const rows = await client.execute('SELECT * FROM users WHERE id = ?', [1])
```

## Notes

The branching workflow is excellent for teams. Deploy requests let you review schema changes before applying them to production.
