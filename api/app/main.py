from fastapi import FastAPI, Request, status, HTTPException, Depends
from starlette.exceptions import HTTPException as StarletteHTTPException # fastapi is built on top of scarlette, when a user goes to a rout that doesnt exist, it is managed by scarlette. Some cases are not handled by fastapi, so with this we make sure cover everything
from fastapi.responses import  JSONResponse # Manually return JSONresponse from our exception handler
from fastapi.exceptions import RequestValidationError # Handling validation error ex: someone passes a 'hello' when a int is expected (I think fastapi handles it by itself, thanks to this we can do i manually)
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from app.limiter import limiter
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.routers import groups_router, tickets_router, users_router, inventory_router
from app.logger import setup_logger

@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logger()
    yield

app = FastAPI()

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_router.router, prefix="/api/users", tags=["users"])
app.include_router(tickets_router.router, prefix="/api/tickets", tags=["tickets"])
app.include_router(groups_router.router, prefix="/api/groups", tags=["groups"])
app.include_router(inventory_router.router, prefix="/api/inventory", tags=["inventory"])

@app.get("/")
def root(request: Request):
    return {"Petit", "Zeub"}

@app.exception_handler(StarletteHTTPException) #handling HTTP error
def general_http_exception_handler(request: Request, exception: StarletteHTTPException):
    message = (
        exception.detail
        if exception.detail
        else "An error occured. Please check your request and try again."
    )

    return JSONResponse(status_code=exception.status_code, content={"detail": message}) 
    
# @app.exception_handler(RequestValidationError) #handling Validation error, it's always 422 errors
# def validation_exception_handler(request: Request, exception: RequestValidationError):
#     return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, content={"detail": exception.errors()})