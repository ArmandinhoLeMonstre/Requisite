from fastapi import FastAPI, Request, status, HTTPException, Depends
from starlette.exceptions import HTTPException as StarletteHTTPException # fastapi is built on top of scarlette, when a user goes to a rout that doesnt exist, it is managed by scarlette. Some cases are not handled by fastapi, so with this we make sure cover everything
from fastapi.responses import  JSONResponse # Manually return JSONresponse from our exception handler
from fastapi.exceptions import RequestValidationError # Handling validation error ex: someone passes a 'hello' when a int is expected (I think fastapi handles it by itself, thanks to this we can do i manually)

from app.schemas.user_schemas import UserCreate, UserResponse, UserUpdate
from app.schemas.ticket_schemas import TicketCreate, TicketResponse
from app.schemas.group_schemas import GroupCreate, GroupResponse

from app.services.user_services import create_user, select_user, patch_user, delete_user
from app.services.ticket_services import create_ticket, select_ticket
from app.services.group_services import create_group, select_group

from app.init_db import engine, get_db, Session

from typing import Annotated #fastapi  pattern for dependencies

app = FastAPI()

@app.get("/")
def root():
    return {"Petit", "Zeub"}


@app.post("/api/user", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def post_new_user(user: UserCreate, db:Annotated[Session, Depends(get_db)]):
    return create_user(user, db)

@app.get("/api/user/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db:Annotated[Session, Depends(get_db)]):
    return select_user(user_id, db)

@app.patch("/api/user/{user_id}", response_model=UserResponse)
def update_user(user_id:int, new_data: UserUpdate, db: Annotated[Session, Depends(get_db)]):
    return patch_user(user_id, new_data, db)

@app.delete("/api/user/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def del_user(user_id: int, db: Annotated[Session, Depends(get_db)]):
    return  delete_user(user_id, db)


@app.post("/api/ticket", status_code=status.HTTP_201_CREATED, response_model=TicketResponse)
def post_new_ticket(request: TicketCreate, db:Annotated[Session, Depends(get_db)]):
    return create_ticket(request, db)

@app.get("/api/ticket/{ticket_id}", response_model=TicketResponse)
def get_ticket(ticket_id: int, db: Annotated[Session, Depends(get_db)]):
    return select_ticket(ticket_id, db)


@app.post("/api/group", status_code=status.HTTP_201_CREATED, response_model=GroupResponse)
def post_new_group(group: GroupCreate, db: Annotated[Session, Depends(get_db)]):
    return create_group(group, db)

@app.get("/api/group/{group_id}", response_model=GroupResponse)
def get_group(group_id: int, db: Annotated[Session, Depends(get_db)]):
    return select_group(group_id, db)

# @app.exception_handlers(StarletteHTTPException) #handling HTTP error
# def general_http_exception_handler(request: Request, exception: StarletteHTTPException):
#     message = (
#         exception.detail
#         if exception.detail
#         else "An error occured. Please check your request and try again."
#     )

#     if request.url.path.startswith("/api"):
#         return JSONResponse(
#             status_code=exception.status_code,
#             content={"detail": message},
#         )
#     return 
    
# @app.exception_handler(RequestValidationError) #handling Validation error, it's always 422 errors
# def validation_exception_handler(request: Request, exception: RequestValidationError):
#     if request.url.path.startswith("/api"):
#         return JSONResponse(
#             status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
#             content={"detail": exception.errors()},
#         )
#     return 