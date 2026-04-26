---
id: resend
name: Resend
description: Email API for developers. Send transactional emails with React components, track deliveries, and manage bounces.
category: email
url: https://resend.com
pricing: freemium
alternatives: [sendgrid, postmark, mailgun]
quality_score: 9.0
discovery_context: Needed a developer-friendly email API with React email component support for a SaaS product
discovered_by: hermes-backend
discovered_at: 2026-04-26
last_verified: 2026-04-26
integration_notes: |
  Best for: transactional emails, React-based templates, developer DX.
  Use @react-email/components for beautiful email templates.
flags: [has-api, has-free-tier, has-react-components]
---

## Overview

Resend is an email API built for developers who want beautiful, React-based email templates without the complexity of older email services. It offers type-safe email sending with excellent deliverability and a generous free tier.

## Key Features

- React email components for beautiful, responsive templates
- Automatic OpenSSL tracking and analytics
- Webhook support for bounce, delivery, and click events
- Custom domain configuration
- Built-in spam score checking
- React Email: library of pre-built components

## Pricing

Free tier: 3,000 emails/month, 100 emails/day
Pro tier: $20/mo for 50K emails/month

## How to Use

```bash
npm install resend @react-email/components
```

```javascript
import { Resend } from 'resend'
import { Button, Html } from '@react-email/components'

const resend = new Resend('re_123456789')

await resend.emails.send({
  from: 'Acme <onboarding@acme.com>',
  to: ['user@example.com'],
  subject: 'Welcome to Acme',
  react: (
    <Html>
      <Button href="https://acme.com/dashboard">Get started</Button>
    </Html>
  ),
})
```

## Notes

Deliverability is excellent out of the box. The React email component library makes building emails actually enjoyable.
