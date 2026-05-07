from fastapi import APIRouter, Depends, status

from typing import Annotated

from app.init_db import get_db 
from sqlalchemy.orm import Session

import uuid

from app.schemas.ticket_schemas import TicketResponse, TicketChats
from app.schemas.chat_schemas import ChatRequest
from app.schemas.agents_requests_schemas import OrchestratorResponse

from app.services.ticket_services import create_ticket, select_ticket, get_tickets
from app.services.user_services import CurrentUser
from app.services.chat_services import new_message
from app.services.orchestrator_service import create_data, call_agents_orchestrator

from app.models.chat_model import Sender

router = APIRouter()


@router.post("", status_code=status.HTTP_201_CREATED, response_model=TicketResponse)
def post_new_ticket(current_user: CurrentUser, db:Annotated[Session, Depends(get_db)]):
    ticket = create_ticket(current_user, db)
    return ticket

@router.get("", response_model=list[TicketResponse])
def get_tickets_from_user(current_user: CurrentUser, db: Annotated[Session, Depends(get_db)]):
    return get_tickets(current_user, db)

@router.get("/{ticket_id}", response_model=TicketResponse)
def get_ticket(current_user: CurrentUser, ticket_id: uuid.UUID, db: Annotated[Session, Depends(get_db)]):
    return select_ticket(ticket_id, current_user, db)

@router.post("/{ticket_id}", response_model=OrchestratorResponse)
def add_chat_to_ticket(current_user: CurrentUser,
               ticket_id: uuid.UUID,
               user_chat: ChatRequest,
               db: Annotated[Session, Depends(get_db)]):
    ticket = select_ticket(ticket_id, current_user, db)
    msg = new_message(user_chat, db, ticket)
    data = create_data(current_user, db, ticket, msg.message)
    rep = call_agents_orchestrator(data, db, msg.message)
    ag_msg = ChatRequest(sender="agent", message= rep.orchestrator_message)
    new_message(ag_msg, db, ticket)
    return rep

@router.get("/{ticket_id}/chats", response_model= TicketChats)
def get_chats(current_user: CurrentUser,
              ticket_id: uuid.UUID,
              db: Annotated[Session, Depends(get_db)]):
    return select_ticket(ticket_id, current_user, db)
