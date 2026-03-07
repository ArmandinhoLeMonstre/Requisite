from fastapi import APIRouter
from app.services import fake_data as fake_data_service
import httpx
import os


router = APIRouter(prefix="/serp")

@router.get("/")
async def get_serp():
	async with httpx.AsyncClient() as client:
		response = await client.get(
			"https://serpapi.com/search",
			params={
				"engine": "google_shopping",
				"q": "Apple wireless keyboard",
				"gl": "be",
				"hl": "fr",
				"google_domain": "google.be",
				"api_key": os.getenv("SERP_API_KEY"),
				"num": 3
			}
		)
		data = response.json()

	return data

@router.get("/fake")
def get_fake_data():
	data = fake_data_service.get_fake_data()
	return data