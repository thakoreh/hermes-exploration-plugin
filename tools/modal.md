---
id: modal
name: Modal
description: Run serverless Python code on GPU hardware. Define functions with decorators, Modal handles the infrastructure, cold starts, and scaling.
category: infrastructure
url: https://modal.com
pricing: freemium
alternatives: [replicate, banan, Vercel-functions]
quality_score: 8.8
discovery_context: "Needed persistent GPU access for batch LLM inference without managing a server"
discovered_by: hermes-mlops
discovered_at: 2026-04-10
last_verified: 2026-04-24
integration_notes: |
  Python-first: @app.function(), @app.image() decorators
  Supports: any Python package, CUDA, multi-GPU, batch inference
  Best for: batch processing, async LLM pipelines, data processing
  Free: $30/mo compute credits, 2 concurrent jobs
flags: [has-api, open-source, has-free-tier, has-python-sdk, self-hostable]
---

## Overview

Modal is infrastructure-as-code for Python. Write Python functions, decorate them with `@app.function()`, and Modal handles everything else: GPU allocation, container management, cold starts, secrets, and scaling.

## Key Features

- Python-native — no YAML, no config files, no Dockerfiles
- GPU support: A100s, H100s, L40s
- Secrets management — inject API keys without hardcoding
- Ephemeral containers — scales to zero automatically
- Batch inference mode for high-throughput LLM workloads
- Volume mounts for persistent storage

## Pricing

Free tier: $30/month compute credits, 2 concurrent jobs
Pay-as-you-go beyond credits: $0.0001-$0.0005 per second per vCPU
GPU: $0.60-$3.00 per hour depending on GPU type
