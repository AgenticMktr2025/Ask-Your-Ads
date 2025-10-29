# Ask Your Ads

## README

\#\# What this is  
A white-label, multi-tenant performance intelligence platform for marketing agencies.

\#\# Core Services  
\- reflex\_app/: Reflex UI (dashboard \+ AI Copilot) built fully in Python using Reflex.    
  \- Reflex compiles this into a production-ready web app (Next.js frontend \+ FastAPI backend under the hood) without us writing any JS.    
  \- We run it via \`reflex run\`.    
  \- We deploy via Railway or Reflex Cloud.    
  \- We pass tenant context (TENANT\_ID, CLIENT\_NAME) via env.

\- api-backend/: FastAPI service that:  
  \- Serves \`/metrics/summary\`, \`/metrics/daily\`, \`/accounts\` with tenant scoping.  
  \- Serves \`/ai/query\`: builds a scoped prompt and calls ai-service.  
  \- Talks to Postgres for cached metrics.

\- worker/: Daily ingestion job:  
  \- APScheduler wakes at 02:00 UTC.  
  \- Pulls data from Lemonado (Google Ads, Meta Ads, LinkedIn Ads, GA, Stripe, etc.).  
  \- Normalizes \+ upserts into Postgres (\`tenants\`, \`accounts\`, \`metrics\`).  
  \- Alerts Slack if any tenant fails.

\- ai-service/: Thin FastAPI layer around Mistral:  
  \- \`/infer\`: internal inference endpoint for api-backend.  
  \- \`/mcp/infer\`: exposed to Lemonado via "Remote MCP" connector so Lemonado can send data to your AI.  
  \- This makes Mistral the only model dependency.

\- infra/: Alembic migrations (multi-tenant schema with \`tenants\`, \`accounts\`, \`metrics\`).

\#\# Data Flow  
1\. Connexify handles onboarding / permissions to ad accounts.  
2\. Lemonado has connectors to ad platforms and analytics platforms.  
3\. worker/ calls Lemonado daily and writes normalized metrics to Postgres.  
4\. api-backend/ reads those metrics and exposes clean JSON for Reflex.  
5\. reflex\_app/ calls api-backend and renders dashboards \+ Copilot chat.  
6\. Copilot asks api-backend â api-backend asks ai-service (Mistral) â answer comes back to Reflex UI.

\#\# Why Reflex?  
\- Pure Python for UI \+ interactivity.  
\- State management and events in Python classes (no React hooks manually).  
\- âPrompt to productionâ: can bootstrap this project via Reflex Build AI, then we iterate directly in Python.    
  Reflex markets this flow as: describe the app â generate production-grade code â deploy.  \[oai\_citation:10â¡reflex.dev\](https://reflex.dev/?utm\_source=chatgpt.com)  
\- Fits your requirement to keep everything Python-native and hostable on Railway.

\#\# Multi-tenancy  
\- Every account row belongs to a tenant.  
\- Every metrics row belongs (indirectly) to that tenant via FK.  
\- All queries to /metrics/\* and /ai/query require tenant\_id.  
\- Reflex will pass tenant\_id and client\_name on every call, so agency A never sees agency B data.

