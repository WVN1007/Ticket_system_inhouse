"""routers to tickets data"""

from enum import Enum
from fastapi import APIRouter

class TicketType(str, Enum):
    ritm = "ritm"
    inc = "inc"

router = APIRouter(
    prefix="/api/tickets",
    tags=["tickets"],
    responses={
        404: {"description": "Not found"}
    },
)

@router.get("/{type_name}")
async def read_tickets(type_name: TicketType):
    if type_name is TicketType.inc:
        return [{"inc_ticket_1":"inc_data_!"},{"inc_ticket_2":"inc_data_2"}]
    if type_name is TicketType.ritm:
        return [{"ritm_ticket1":"ritm_items_!"},{"ritm_ticket2":"ritem_data_@"}]

# TODO: make CRUD for tickets
