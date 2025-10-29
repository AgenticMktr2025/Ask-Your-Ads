# Ask Your Ads

## Multi-Tenancy Upgrade

# Introduction

The purpose of this document is to provide a **detailed integration plan** for using Mistral AI Studio (and/or self-hosted Mistral models) as your AI infrastructure layer. This covers architecture, prompt engineering, model variant choices, cost modelling, and dev-ops steps.

## **1\. System Architecture: how Mistral fits in**

**Our stack:**

* Front-end and API: Python (FastAPI)

* Data layer: Lemanado MCP for ad & analytics connectors

* Onboarding/management: Connexify white-label

* Hosting: Railway containers

* AI layer: Mistral Studio / self-hosted Mistral models

**Flow:**

1. User issues a query via front-end (via Rio or Lovable UI).

2. FastAPI endpoint receives: /ai/query.

3. Decision logic: Is it simple (metric fetch) or complex (analysis)?

   * If simple: fetch data from Lemanado/DB, return summary.

   * If complex: route to Mistral model.

4. FastAPI sends prompt to Mistral endpoint (either Mistral Studio API or self-hosted).

   * Example: model âmistral-medium-latestâ.

5. Receive response from model â FastAPI formats and returns to UI.

6. Optionally store interaction in DB for analytics/memory.

**Deployment options:**

* **Managed API mode**: Use Mistralâs API (âLa Plateformeâ) â quick start. 

* **Self-hosted mode**: Deploy open weights using vLLM or another inference engine. 

  * You could host this in Railway as a container (if GPU/appropriate resources available)

* In either case you control the integration.

## **2\. Prompt Engineering & Model Variant Selection**

### **Model Variant Choices**

| Use Case | Model | Notes |
| ----- | ----- | ----- |
| Lightweight reasoning & dispatching | Mistral-Small / Mistral-7B-Instruct | Lower compute & cost |
| Medium-complex analysis (insights from metrics) | Mistral-Medium / Mistral-Large (depending) | Balanced performance |
| Heavy reasoning / narrative reports | Mistral-Large or custom fine-tuned variant | Higher cost, longer runtime |

From docs: Mistral supports both API and self-deployment, open weights are available. 

### **Prompt Patterns**

For your analytics copilot, you may use pattern like:

You are an Analytics Assistant. The user data for platform X:

{

  "platform": "google\_ads",

  "account\_id": "12345",

  "metrics": \[

     { "date": "2025-10-20", "spend": 200.5, "clicks": 450, "conversions": 12 },

     { "date": "2025-10-21", "spend": 250.0, "clicks": 500, "conversions": 15 }

  \]

}

Task: Provide insights, highlight anomalies (if any), and recommend three actions to optimise ROAS. Format your answer as:

1\. Key observations:

2\. Anomalies:

3\. Recommendations:

You may also use function-calling via Mistralâs API (if supported) to control output format.

### **Data Fetch vs Reasoning Routing**

In your backend you may implement:

if simple\_metric\_request:

    return fetch\_from\_db(...)

else:

    prompt \= build\_prompt(...)

    response \= mistral\_client.chat\_complete(model=chosen\_model, messages=\[...\])

    return response\["content"\]

## **3\. Cost and Compute Planning**

### **Managed vs Self-Host**

* **Managed API**: You pay per token/usage. Good to start, less control.

* **Self-Host**: You pay for compute (Railway container, possibly GPU). Good long-term for cost-predictability.

Docs: self-deployment via vLLM is supported. 

### **Compute Estimation**

Assume you choose Mistral-Medium variant self-hosted:

* Container runs on a 1-2 vCPU \+ GPU (say A10G) or highâRAM CPU if no GPU.

* You estimate X queries/day; each query uses Y tokens.

* Compute cost \= container hourly cost \* hours uptime \+ storage.

* You avoid per-token billing from external API, giving you cost control.

### **Implementation Steps**

1. Benchmark selected model locally (on your Railway equivalent) to measure tokens/s, latency.

2. Estimate peak concurrent usage \=\> set container autoâscale.

3. Set budget alerts (Railway supports usage caps) to monitor.

## **4\. DevOps & Integration Steps**

### **a) API Key / Authentication**

* If using Mistral API: setup MISTRAL\_API\_KEY as environment variable in FastAPI service.

* If self-hosting: secure endpoint (auth, rate limiting) inside your network or Railway private network.

### **b) Containerising the LLM service**

* Build Dockerfile for model service:

FROM python:3.11-slim

RUN pip install vllm transformers torch

COPY . /app

WORKDIR /app

CMD \["python", "serve\_model.py"\]

* In serve\_model.py, use vLLM to load the model and expose REST HTTP endpoint (OpenAI compatible). Docs show example. 

### **c) Secure Networking**

* Expose services internal only. For Railway, use project âinternal networkâ or set appropriate domain restrictions.

* Use HTTPS \+ authentication between FastAPI â LLM service.

### **d) Logging & Monitoring**

* Log each model call (user id, prompt size, model used, latency).

* Store logs in DB for audit \+ cost tracking.

* Monitor error rates, latency spikes.

### **e) Versioning & Model Switching**

* You may support multiple models (small vs large). Add parameter model in your API to route accordingly.

* Maintain feature flags to switch to new model versions without breaking.

### **f) Failover Plan**

* If your self-hosted model fails (container crash), fallback to Mistralâs managed API temporarily.

## **5\. What needs implementing**

* **In your FastAPI backend**:

  * Module to call Lemanado MCP endpoints (e.g., mcp\_client.py): handle authentication, request construction, error handling.

  * Module to call Mistral API (or your self-hosted endpoint).

  * Routing logic that bridges user query â data fetch â prompt â model call â result.

* **In your orchestration logic**:

  * Define which âtoolsâ or MCP endpoints the model can call (you may register them).

  * Structure your prompt to include instructions for the model about how to interpret metrics.

  * Possibly integrate function-calling so that Mistral can directly invoke a âget\_metricsâ tool rather than you doing all the fetch yourself.

* **In your Lemanado setup**:

  * Ensure that all your data sources (Google Ads, Meta Ads, etc.) are connected and exposed via MCP endpoints.

  * Possibly expose a âtoolâ schema that the model can call (if you use MCP tool invocation).

* **In your deployment**:

  * Secure API keys (for Mistral, Lemanado) via environment variables.

  * Monitor latency, failures, and cost (Mistral token usage or compute if self-hosted).

  * Define fallback logic: if Mistral fails, what happens?

