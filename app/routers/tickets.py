"""routers to tickets data"""

from enum import Enum
from fastapi import APIRouter
from ..schemas import TicketCreate

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
# TODO: Tasks
'''
- [x] check how pydantic behave in GET method
- [ ] create tests data in the database to test for GET method
- [ ] write GET method to read from database
'''

@router.post("/{type_name}/")
async def create_ticket(type_name:TicketType,ticket:TicketCreate):
    if type_name is TicketType.inc:
        return {"ticket":ticket, "type":"INC"}
    if type_name is TicketType.ritm:
        return {"ticket":ticket, "type":"RITM"}

