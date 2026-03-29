from fastapi import FastAPI

app = FastAPI()

@app.post("/chat")
async def chat(message: str, employee_id: int):
    # run the agent loop here\
    response = "Hello world"
    # response = await run_agent(message, employee_id)
    return {"response": response}