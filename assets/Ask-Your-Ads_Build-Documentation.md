# Ask Your Ads

## Build Guide & Documentation

# Introduction

Lorem Ipsom

# Monorepo Layout

connexify-intelligence/  
âââ reflex\_app/                 \# Reflex "frontend" app (pure Python UI \+ state)  
â   âââ reflex\_app/\_\_init\_\_.py  
â   âââ reflex\_app/state.py     \# global app state, tenant context, actions  
â   âââ reflex\_app/components/  
â   â   âââ kpi\_table.py  
â   â   âââ chat\_panel.py  
â   â   âââ \_\_init\_\_.py  
â   âââ reflex\_app/pages/  
â   â   âââ dashboard.py        \# tenant-scoped KPI dashboard  
â   â   âââ copilot.py          \# AI copilot view  
â   â   âââ index.py            \# router/home  
â   âââ reflex\_app/config.py    \# points to api-backend base URL, tenant info  
â   âââ rxconfig.py             \# standard Reflex config  
â   âââ requirements.txt  
â   âââ README.md  
â  
âââ api-backend/  
â   âââ app/  
â   â   âââ main.py  
â   â   âââ config.py  
â   â   âââ db.py  
â   â   âââ models.py  
â   â   âââ schemas.py  
â   â   âââ deps.py  
â   â   âââ routes/  
â   â   â   âââ health.py  
â   â   â   âââ metrics.py      \# tenant-scoped metrics summary & daily  
â   â   â   âââ accounts.py     \# tenant-scoped account list  
â   â   â   âââ ai.py           \# /ai/query â calls ai-service  
â   â   âââ services/  
â   â   â   âââ prompt\_builder.py  
â   â   â   âââ lemanado\_client.py   \# placeholder for direct fresh pulls if needed  
â   â   â   âââ ai\_client.py         \# calls ai-service  
â   â   â   âââ \_\_init\_\_.py  
â   â   âââ utils/  
â   â   â   âââ logger.py  
â   â   â   âââ \_\_init\_\_.py  
â   â   âââ \_\_init\_\_.py  
â   âââ requirements.txt  
â   âââ Dockerfile  
â   âââ alembic.ini  
â   âââ README.md  
â  
âââ ai-service/  
â   âââ main.py                \# /infer, /mcp/infer, /mcp/manifest.json  
â   âââ config.py  
â   âââ mistral\_client.py      \# calls Mistral AI Studio OR self-hosted mistral  
â   âââ schemas.py  
â   âââ requirements.txt  
â   âââ Dockerfile  
â   âââ README.md  
â  
âââ worker/  
â   âââ scheduler.py           \# APScheduler daily cron (02:00 UTC)  
â   âââ sync\_loop.py           \# multi-tenant pull \+ upsert  
â   âââ config.py  
â   âââ lemanado\_pull.py       \# call Lemonado MCP connectors  
â   âââ normalizer.py  
â   âââ utils.py               \# logging, Slack alert  
â   âââ requirements.txt  
â   âââ Dockerfile  
â   âââ README.md  
â  
âââ infra/  
â   âââ alembic/  
â   â   âââ env.py  
â   â   âââ versions/  
â   â       âââ 0001\_multitenant.py  
â   âââ README.md  
â  
âââ README.md                  \# top-level overview

## Notes: 

* Reflex app will run with reflex run in dev and can also be containerized / deployed on Railway or Reflex Cloud. Reflex supports âprompt to app,â then you iterate in Python. 

* We are keeping api-backend because the separation of concerns is still valuable: Reflex is UI \+ session state \+ light logic, FastAPI is your multi-tenant API boundary and data service. This mirrors how Reflex internally compiles to NextJS/React frontends and FastAPI backends under the hood; conceptually, youâre just explicitly keeping your analytics/business API in api-backend. 

# Key Files

Below are code stubs for each of the key files related to this build.

### **reflex\_app/requirements.txt**

reflex  
requests  
python-dotenv

### **reflex\_app/config.py**

import os

API\_BASE \= os.getenv("API\_BACKEND\_URL", "http://localhost:8000")

\# tenancy context for this deployed instance / subdomain  
TENANT\_ID \= int(os.getenv("TENANT\_ID", "1"))  
CLIENT\_NAME \= os.getenv("CLIENT\_NAME", "Acme Co")  
DATE\_RANGE\_DEFAULT \= "7d"

### **reflex\_app/state.py**

\#\#\#Reflex apps use a State class for reactive state, events, and side effects. State methods can call external APIs, update variables, and trigger rerenders.\#\#\#

import reflex as rx  
import requests  
from .config import API\_BASE, TENANT\_ID, CLIENT\_NAME, DATE\_RANGE\_DEFAULT

class AppState(rx.State):  
    \# reactive vars  
    kpi\_rows: list\[dict\] \= \[\]  
    chat\_messages: list\[dict\] \= \[\]

    def load\_summary(self):  
        """Fetch KPI summary for the dashboard."""  
        resp \= requests.get(  
            f"{API\_BASE}/metrics/summary",  
            params={  
                "tenant\_id": TENANT\_ID,  
                "client\_name": CLIENT\_NAME,  
                "date\_range": DATE\_RANGE\_DEFAULT,  
            },  
            timeout=10,  
        )  
        resp.raise\_for\_status()  
        self.kpi\_rows \= resp.json()

    def ask\_copilot(self, question: str):  
        """Send a question to AI and append answer to chat history."""  
        \# append user message locally  
        self.chat\_messages \= self.chat\_messages \+ \[  
            {"role": "user", "content": question}  
        \]

        resp \= requests.post(  
            f"{API\_BASE}/ai/query",  
            json={  
                "question": question,  
                "tenant\_id": TENANT\_ID,  
                "client\_name": CLIENT\_NAME,  
            },  
            timeout=20,  
        )  
        resp.raise\_for\_status()  
        answer \= resp.json()\["answer"\]

        self.chat\_messages \= self.chat\_messages \+ \[  
            {"role": "assistant", "content": answer}  
        \]

### **reflex\_app/components/kpi\_table.py**

\#\#\#In Reflex, UI is declared in Python using rx.\* components. Reflex compiles that to React+NextJS under the hood so you never touch JS manually.\#\#\#

import reflex as rx

def kpi\_table(rows: list\[dict\]) \-\> rx.Component:  
    \# rows: \[{platform, total\_spend, total\_clicks, total\_conversions, total\_revenue, ...}\]  
    header \= rx.hstack(  
        rx.text("Platform", weight="bold"),  
        rx.text("Spend", weight="bold"),  
        rx.text("Clicks", weight="bold"),  
        rx.text("Conv", weight="bold"),  
        rx.text("Revenue", weight="bold"),  
        spacing="2rem",  
    )

    body \= \[  
        rx.hstack(  
            rx.text(r\["platform"\]),  
            rx.text(f"{r\['total\_spend'\]:.2f}"),  
            rx.text(str(r\["total\_clicks"\])),  
            rx.text(str(r\["total\_conversions"\])),  
            rx.text(f"{r\['total\_revenue'\]:.2f}"),  
            spacing="2rem",  
        )  
        for r in rows  
    \]

    return rx.vstack(  
        header,  
        \*body,  
        spacing="0.5rem",  
        border="1px solid \#e2e2e2",  
        border\_radius="0.5rem",  
        padding="1rem",  
        width="100%",  
    )

### **reflex\_app/components/chat\_panel.py**

import reflex as rx  
from ..state import AppState

def chat\_panel():  
    def render\_message(message: dict):  
        who \= "You" if message\["role"\] \== "user" else "Copilot"  
        color \= "gray" if message\["role"\] \== "user" else "purple"  
        return rx.box(  
            rx.text(f"{who}:", weight="bold", color=color),  
            rx.text(message\["content"\]),  
            border="1px solid \#ddd",  
            border\_radius="0.5rem",  
            padding="0.75rem",  
            margin\_bottom="0.75rem",  
            width="100%",  
        )

    messages\_box \= rx.vstack(  
        rx.foreach(AppState.chat\_messages, render\_message),  
        height="300px",  
        overflow\_y="auto",  
        border="1px solid \#ccc",  
        border\_radius="0.5rem",  
        padding="1rem",  
        width="100%",  
        background="white",  
    )

    input\_box \= rx.hstack(  
        rx.input(  
            placeholder="Ask about performance...",  
            on\_blur=lambda value: AppState.ask\_copilot(value),  
            width="100%",  
        ),  
        width="100%",  
        spacing="1rem",  
    )

    return rx.vstack(  
        rx.heading("AI Copilot", size="md"),  
        messages\_box,  
        input\_box,  
        spacing="1rem",  
        width="100%",  
    )

### **reflex\_app/pages/dashboard.py**

import reflex as rx  
from ..state import AppState  
from ..components.kpi\_table import kpi\_table  
from ..config import CLIENT\_NAME, DATE\_RANGE\_DEFAULT

def dashboard\_page() \-\> rx.Component:  
    \# on load \-\> AppState.load\_summary()  
    return rx.vstack(  
        rx.heading(f"Client: {CLIENT\_NAME}", size="lg"),  
        rx.text(f"Last {DATE\_RANGE\_DEFAULT} performance"),  
        kpi\_table(AppState.kpi\_rows),  
        spacing="1.5rem",  
        padding="2rem",  
        width="100%",  
        on\_mount=AppState.load\_summary,  
    )

### **reflex\_app/pages/copilot.py**

import reflex as rx  
from ..components.chat\_panel import chat\_panel  
from ..config import CLIENT\_NAME

def copilot\_page() \-\> rx.Component:  
    return rx.vstack(  
        rx.heading(f"AI Copilot for {CLIENT\_NAME}", size="lg"),  
        chat\_panel(),  
        spacing="1.5rem",  
        padding="2rem",  
        width="100%",  
        height="100%",  
    )

### **reflex\_app/pages/index.py**

\#\#\#Reflex normally lets you define multipage apps by returning app \= rx.App() with routers or by setting routes. Weâll expose a simple sidebar layout with two âpages.â\#\#\#

import reflex as rx  
from .dashboard import dashboard\_page  
from .copilot import copilot\_page  
from ..state import AppState

def layout(content: rx.Component) \-\> rx.Component:  
    return rx.hstack(  
        rx.vstack(  
            rx.button("Dashboard", on\_click=lambda: rx.redirect("/dashboard")),  
            rx.button("Copilot", on\_click=lambda: rx.redirect("/copilot")),  
            spacing="1rem",  
            padding="1rem",  
            border\_right="1px solid \#eee",  
            min\_width="200px",  
            height="100vh",  
        ),  
        rx.box(  
            content,  
            padding="1rem",  
            width="100%",  
            height="100vh",  
            overflow\_y="auto",  
        ),  
        width="100%",  
    )

def index() \-\> rx.Component:  
    return layout(dashboard\_page())

def dashboard() \-\> rx.Component:  
    return layout(dashboard\_page())

def copilot() \-\> rx.Component:  
    return layout(copilot\_page())

app \= rx.App(state=AppState)  
app.add\_page(index, route="/")  
app.add\_page(dashboard, route="/dashboard", title="Dashboard")  
app.add\_page(copilot, route="/copilot", title="AI Copilot")

### **reflex\_app/rxconfig.py**

\#\#\#This is part of a normal Reflex project. Reflex uses this to configure the appâs metadata when you run reflex init and reflex run.\#\#\#

import reflex as rx

class ConnexifyConfig(rx.Config):  
    app\_name \= "reflex\_app"  
    \# You can set additional config options here (e.g. API keys via env)

config \= ConnexifyConfig()  
