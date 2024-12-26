from fasthtml.common import *
import httpx
from urllib.parse import urlencode

MOCK_DB_URL = "http://localhost:8000/api"

app, rt = fast_app()

async def call_mock_db(method, endpoint, json=None, params=None):
    async with httpx.AsyncClient() as client:
        response = await client.request(
            method,
            f"{MOCK_DB_URL}/{endpoint}",
            json=json,
            params=params
        )
        response.raise_for_status()
        return response.json()

def create_add_form():
    return Form(
        Input(name="name", placeholder="Enter name", cls="border p-2"),
        Input(name="email", placeholder="Enter email", cls="border p-2"),
        Input(name="role", placeholder="Enter role", cls="border p-2"),
        Button("Add", cls="bg-green-500 text-white p-2"),
        hx_post="/api/records",
        hx_target="#records-table",
        hx_swap="beforeend"
    )

def create_filter_header(field):
    return Th(
        Div(field.title()),
        Input(
            name=f"filter_{field}",
            placeholder=f"Filter {field}...",
            cls="w-full border p-1 mt-1",
            hx_trigger="keyup changed delay:500ms",
            hx_get="/api/records",
            hx_target="#records-table",
            hx_include="[name^='filter_']"
        )
    )

def create_record_row(record):
    return Tr(
        Td(
            Div(
                record["name"],
                hx_get=f"/api/records/{record['id']}/edit/name",
                hx_trigger="click",
                hx_target="closest td",
                hx_swap="innerHTML"
            )
        ),
        Td(
            Div(
                record["email"],
                hx_get=f"/api/records/{record['id']}/edit/email",
                hx_trigger="click",
                hx_target="closest td",
                hx_swap="innerHTML"
            )
        ),
        Td(
            Div(
                record["role"],
                hx_get=f"/api/records/{record['id']}/edit/role",
                hx_trigger="click",
                hx_target="closest td",
                hx_swap="innerHTML"
            )
        ),
        Td(
            Button(
                "Delete",
                cls="bg-red-500 text-white p-2",
                hx_delete=f"/api/records/{record['id']}",
                hx_target="closest tr",
                hx_swap="outerHTML"
            )
        )
    )

@rt("/")
async def get():
    records = await call_mock_db("GET", "records")
    return Titled(
        "Employees - A CRUD Grid Demo",
        Container(
            create_add_form(),
            Table(
                Thead(
                    Tr(
                        create_filter_header("name"),
                        create_filter_header("email"),
                        create_filter_header("role"),
                        Th("Actions")
                    )
                ),
                Tbody(
                    *[create_record_row(record) for record in records],
                    id="records-table"
                ),
                cls="w-full border-collapse"
            )
        )
    )

@rt("/api/records")
async def get(filter_name: str = "", filter_email: str = "", filter_role: str = ""):
    # Get all records and filter client-side for demo
    # In production, filtering should be done at database level
    records = await call_mock_db("GET", "records")

    filtered = [r for r in records
                if (not filter_name or filter_name.lower() in r["name"].lower()) and
                   (not filter_email or filter_email.lower() in r["email"].lower()) and
                   (not filter_role or filter_role.lower() in r["role"].lower())]

    return Tbody(
        *[create_record_row(record) for record in filtered],
        id="records-table"
    )

@rt("/api/records")
async def post(name: str, email: str, role: str):
    record = await call_mock_db("POST", "records", json={"name": name, "email": email, "role": role})
    return create_record_row(record)

@rt("/api/records/{id}")
async def delete(id: int):
    await call_mock_db("DELETE", f"records/{id}")
    return ""

@rt("/api/records/{id}/edit/{field}")
async def get(id: int, field: str):
    record = await call_mock_db("GET", f"records/{id}")
    return Form(
        Input(
            value=record[field],
            name="value",
            cls="border p-1"
        ),
        Button("Save", cls="bg-green-500 text-white p-1"),
        hx_put=f"/api/records/{id}/field/{field}",
        hx_target="closest td",
        hx_swap="innerHTML"
    )

@rt("/api/records/{id}/field/{field}")
async def put(id: int, field: str, value: str):
    record = await call_mock_db("PUT", f"records/{id}", params={"field": field, "value": value})
    return Div(
        record[field],
        hx_get=f"/api/records/{id}/edit/{field}",
        hx_trigger="click",
        hx_target="closest td",
        hx_swap="innerHTML"
    )

if __name__ == "__main__":
    serve(app, port=5001)