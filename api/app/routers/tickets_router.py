from fastapi import APIRouter, Depends, status, Request

from typing import Annotated

from app.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession

import uuid

from app.schemas.ticket_schemas import TicketResponse, TicketChats, TicketCreate, TicketsGroup
from app.schemas.chat_schemas import ChatRequest
from app.schemas.agents_requests_schemas import OrchestratorResponse

from app.services.ticket_services import create_ticket, select_ticket, get_tickets, get_tickets_group, change_status
from app.services.user_services import CurrentUser
from app.services.chat_services import new_message
from app.services.orchestrator_service import create_data, call_agents_orchestrator

from app.models.ticket_model import TicketStatus

from app.limiter import limiter

router = APIRouter()


@router.post("", status_code=status.HTTP_201_CREATED, response_model=TicketResponse)
async def post_new_ticket(body: TicketCreate, current_user: CurrentUser, db:Annotated[AsyncSession, Depends(get_db)]):
    ticket = await create_ticket(body.user_message, current_user, db)
    return ticket

@router.get("", response_model=list[TicketResponse])
async def get_tickets_from_user(current_user: CurrentUser, db: Annotated[AsyncSession, Depends(get_db)]):
    return await get_tickets(current_user, db)

@router.get("/manager", response_model=TicketsGroup)
async def get_tickets_from_group(current_user: CurrentUser,
                                 db: Annotated[AsyncSession, Depends(get_db)]):
    return await get_tickets_group(current_user, db)

@router.get("/{ticket_id}", response_model=TicketResponse)
async def get_ticket(current_user: CurrentUser, ticket_id: uuid.UUID, db: Annotated[AsyncSession, Depends(get_db)]):
    return await select_ticket(ticket_id, current_user, db)

@router.post("/{ticket_id}", response_model=OrchestratorResponse)
@limiter.limit("200/hour") #A configurer avec le chiffre exact en prod
async def add_chat_to_ticket(
				request: Request, # param obligatoire pour rate limit
    			current_user: CurrentUser,
                ticket_id: uuid.UUID,
                user_chat: ChatRequest,
                db: Annotated[AsyncSession, Depends(get_db)]):
    ticket = await select_ticket(ticket_id, current_user, db)
    msg = await new_message(user_chat, db, ticket)
    data = await create_data(current_user, db, ticket, msg.message)
    rep = await call_agents_orchestrator(data, db, msg.message)
    ag_msg = ChatRequest(sender="agent", message= rep.orchestrator_message)
    await new_message(ag_msg, db, ticket)
    return rep

@router.get("/{ticket_id}/chats", response_model= TicketChats)
async def get_chats(current_user: CurrentUser,
              ticket_id: uuid.UUID,
              db: Annotated[AsyncSession, Depends(get_db)]):
    return await select_ticket(ticket_id, current_user, db)

@router.patch("/{ticket_id}/status", response_model=TicketResponse)
async def change_ticket_status(current_user: CurrentUser,
                 db: Annotated[AsyncSession,Depends(get_db)],
                 status: TicketStatus,
                 ticket_id: uuid.UUID):
    return await change_status(current_user,ticket_id, status, db)
    
