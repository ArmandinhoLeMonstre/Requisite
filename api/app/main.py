from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from starlette.exceptions import HTTPException as StarletteHTTPException # fastapi is built on top of scarlette, when a user goes to a rout that doesnt exist, it is managed by scarlette. Some cases are not handled by fastapi, so with this we make sure cover everything
from fastapi.responses import  JSONResponse # Manually return JSONresponse from our exception handler
from fastapi.exceptions import RequestValidationError # Handling validation error ex: someone passes a 'hello' when a int is expected (I think fastapi handles it by itself, thanks to this we can do i manually)


app = FastAPI()

@app.get("/")
def root():
    return {"Petit", "Zeub"}

@app.exception_handlers(StarletteHTTPException)
def general_http_exception_handler(request: Request, exception: StarletteHTTPException):
    message = (
        exception.detail
        if exception.detail
        else "An error occured. Please check your request and try again."
    )

    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=exception.status_code,
            content={"detail": message},
        )