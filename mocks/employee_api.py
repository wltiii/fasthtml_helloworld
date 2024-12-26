from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

app = FastAPI()

class Record(BaseModel):
    id: Optional[int] = None
    name: str
    email: str
    role: str

mock_records = {
    1: Record(id=1, name="John Doe", email="john@example.com", role="Admin"),
    2: Record(id=2, name="Jane Smith", email="jane@example.com", role="User"),
}
next_id = 3

@app.get("/api/records", response_model=List[Record])
async def get_records(
    name: str = Query(None, description="Filter by name"),
    email: str = Query(None, description="Filter by email"),
    role: str = Query(None, description="Filter by role")
):
    records = list(mock_records.values())

    if name:
        records = [r for r in records if name.lower() in r.name.lower()]
    if email:
        records = [r for r in records if email.lower() in r.email.lower()]
    if role:
        records = [r for r in records if role.lower() in r.role.lower()]

    return records

@app.get("/api/records/{record_id}", response_model=Record)
async def get_record(record_id: int):
    if record_id not in mock_records:
        raise HTTPException(status_code=404, detail="Record not found")
    return mock_records[record_id]

@app.post("/api/records", response_model=Record)
async def create_record(record: Record):
    global next_id
    record.id = next_id
    mock_records[next_id] = record
    next_id += 1
    return record

@app.put("/api/records/{record_id}", response_model=Record)
async def update_record(record_id: int, field: str, value: str):
    if record_id not in mock_records:
        raise HTTPException(status_code=404, detail="Record not found")
    record = mock_records[record_id]
    setattr(record, field, value)
    return record

@app.delete("/api/records/{record_id}")
async def delete_record(record_id: int):
    if record_id not in mock_records:
        raise HTTPException(status_code=404, detail="Record not found")
    del mock_records[record_id]
    return {"success": True}

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)