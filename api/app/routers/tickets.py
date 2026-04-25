from fastapi import APIRouter, Depends, status

from typing import Annotated

from app.init_db import get_db 
from sqlalchemy.orm import Session

import uuid

from app.schemas.ticket_schemas import TicketCreate, TicketResponse
from app.services.ticket_services import create_ticket, select_ticket


router = APIRouter()


@router.post("", status_code=status.HTTP_201_CREATED, response_model=TicketResponse)
def post_new_ticket(request: TicketCreate, db:Annotated[Session, Depends(get_db)]):
    return create_ticket(request, db)

@router.get("/{ticket_id}", response_model=TicketResponse)
def get_ticket(ticket_id: uuid.UUID, db: Annotated[Session, Depends(get_db)]):
    return select_ticket(ticket_id, db)