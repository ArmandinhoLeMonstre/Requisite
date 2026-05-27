from openai import AsyncOpenAI
import os

openai_api_key = os.getenv("OPENAI_API_KEY")

client = AsyncOpenAI(
  api_key=openai_api_key
)