from fastapi import APIRouter, Depends, status

from typing import Annotated

from app.init_db import get_db 
from sqlalchemy.orm import Session

import uuid

from app.schemas.ticket_schemas import TicketResponse, TicketChats
from app.schemas.chat_schemas import ChatRequest
from app.services.ticket_services import create_ticket, select_ticket
from app.services.user_services import CurrentUser
from app.services.chat_services import new_message
from app.models.chat import Sender


router = APIRouter()


@router.post("", status_code=status.HTTP_201_CREATED, response_model=TicketResponse)
def post_new_ticket(message: str, current_user: CurrentUser, db:Annotated[Session, Depends(get_db)]):
    ticket = create_ticket(current_user, db)
    chat = ChatRequest(sender= Sender.user, message= message)
    new_message(chat, db, ticket)
    return ticket

@router.get("/{ticket_id}", response_model=TicketResponse)
def get_ticket(current_user: CurrentUser, ticket_id: uuid.UUID, db: Annotated[Session, Depends(get_db)]):
    return select_ticket(ticket_id, current_user, db)

@router.post("/{ticket_id}", response_model=TicketResponse)
def get_ticket(current_user: CurrentUser,
               ticket_id: uuid.UUID,
               chat: ChatRequest,
               db: Annotated[Session, Depends(get_db)]):
    ticket = select_ticket(ticket_id, current_user, db)
    new_message(chat, db, ticket)
    return ticket

@router.get("{ticket_id}/chats", response_model= TicketChats)
def get_chats(current_user: CurrentUser,
              ticket_id: uuid.UUID,
              db: Annotated[Session, Depends(get_db)]):
    return select_ticket(ticket_id, current_user, db)