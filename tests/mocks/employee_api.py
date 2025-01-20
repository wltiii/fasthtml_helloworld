from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import logging

app = FastAPI()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class Record(BaseModel):
    id: Optional[int] = None
    name: str
    email: str
    role: str

class UpdateRecordRequest(BaseModel):
    name: str
    email: str
    role: str

mock_database = {
    1: Record(id=1, name="John Doe", email="john@example.com", role="Admin"),
    2: Record(id=2, name="Jane Smith", email="jane@example.com", role="User"),
    3: Record(id=3, name="Jack Smith", email="jack@example.com", role="User"),
}
next_id = 4

def matches_filter(record, role=None, name=None, email=None):
    # Check if any filters are provided
    if role is None and name is None and email is None:
        return True  # No filters applied, include all records

    if role is not None and role.lower() in record.role.lower():
        return True # role filter matches

    if name is not None and name.lower() in record.name.lower():
        return True # name filter matches

    if email is not None and email.lower() in record.email.lower():
        return True # email filter matches

    return False

def filter_records(records,
    filter_name: str = Query(None, description="Filter by name"),
    filter_email: str = Query(None, description="Filter by email"),
    filter_role: str = Query(None, description="Filter by role")
    ):

    filtered_records = [
        r for r in records if matches_filter(
            r,
            filter_role,
            filter_name,
            filter_email
        )
    ]

    logger.info(f"get_records: filtered records: {filtered_records}")
    return filtered_records

@app.get("/api/records", response_model=List[Record])
async def get_records(
    name: str = Query(None, description="Filter by name"),
    email: str = Query(None, description="Filter by email"),
    role: str = Query(None, description="Filter by role")):
    logger.info(f"get_records(name: {name}, email: {email}, role: {role})")

    if name or email or role:
        return filter_records(
            list(mock_database.values()),
            name,
            email,
            role
        )

    return list(mock_database.values())

@app.get("/api/records/{record_id}", response_model=Record)
async def get_record(record_id: int):
    if record_id not in mock_database:
        raise HTTPException(status_code=404, detail="Record not found")
    return mock_database[record_id]

@app.post("/api/records", response_model=Record)
async def create_record(record: Record):
    global next_id
    record.id = next_id
    mock_database[next_id] = record
    next_id += 1
    return record

@app.put("/api/records/{record_id}", response_model=Record)
async def update_record(record_id: int, update_request: UpdateRecordRequest):
    logger.info(f"update_record(record_id: {record_id}, name: {update_request.name}, email: {update_request.email}, role: {update_request.role})")

    if record_id not in mock_database:
        raise HTTPException(status_code=404, detail="Record not found")
    record = mock_database[record_id]

    logger.info(f"update_record(retrieved record: {record})")
    setattr(record, update_request.field, update_request.value)
    # setattr(record, "name", update_request.name)
    # setattr(record, "email", update_request.email)
    # setattr(record, "role", update_request.role)

    logger.info(f"update_record(updated record to: {record})")
    # return record
    # I've added hx_trigger="load", hx_get="/api/records",
    # hx_target="#records-table", and hx_swap="outerHTML"
    # to the response of the update_record function. This
    # will trigger a refresh of the records list after a
    # record is updated.
    return {"hx_trigger": "load", "hx_get": "/api/records", "hx_target": "#records-table", "hx_swap": "outerHTML"}

@app.delete("/api/records/{record_id}")
async def delete_record(record_id: int):
    if record_id not in mock_database:
        raise HTTPException(status_code=404, detail="Record not found")
    del mock_database[record_id]
    return {"success": True}

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)