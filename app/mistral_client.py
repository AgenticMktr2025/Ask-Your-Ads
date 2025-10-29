import reflex as rx
import os
import json
import logging
from mistralai.client import MistralClient
from app.config import MISTRAL_API_KEY, CLIENT_NAME, DATE_RANGE_DEFAULT
from app.state import KPIRow, ChatMessage


def _build_prompt(question: str, kpi_data: list[KPIRow]) -> list[ChatMessage]:
    system_prompt = """You are a world-class marketing analytics assistant for a digital agency.
Your client is asking for insights about their performance data.
Analyze the provided KPI data and answer user questions with actionable, data-driven insights.
Focus on: spend efficiency, Return On Ad Spend (ROAS), conversion trends, and clear optimization recommendations.
Be concise and clear in your analysis. Use the provided data to back up your claims.
"""
    kpi_json = json.dumps([dict(row) for row in kpi_data], indent=2)
    user_prompt = f"\nClient: {CLIENT_NAME}\nDate Range: {DATE_RANGE_DEFAULT}\n\nCurrent Metrics:\n{kpi_json}\n\nQuestion: {question}\n"
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]


async def query_mistral(question: str, kpi_data: list[KPIRow]) -> str:
    if not MISTRAL_API_KEY:
        raise ValueError("MISTRAL_API_KEY is not set.")
    try:
        client = MistralClient(api_key=MISTRAL_API_KEY)
        messages = _build_prompt(question, kpi_data)
        chat_response = await client.chat_async(
            model="mistral-medium-latest",
            messages=messages,
            temperature=0.7,
            max_tokens=1000,
        )
        return chat_response.choices[0].message.content
    except Exception as e:
        logging.exception(f"Error querying Mistral AI: {e}")
        return "Sorry, I encountered an error while trying to generate a response. Please check the logs."