from venv import logger
from fasthtml.common import *
import httpx
from urllib.parse import urlencode
import logging

MOCK_EMPLOYEE_API_URL = "http://localhost:8000/api"

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app, rt = fast_app()

async def call_mock_db(method, endpoint, json=None, params=None):
    logger.info(f"call_mock_db(method: {method}, endpoint: {endpoint}, json: {json}, params: {params})")

    async with httpx.AsyncClient() as client:
        response = await client.request(
            method,
            f"{MOCK_EMPLOYEE_API_URL}/{endpoint}",
            json=json,
            params=params
        )
        response.raise_for_status()
        return response.json()

def create_add_form():
    logger.info(f"create_add_form()")

    return Form(
        Td(
            Input(name="name", placeholder="Enter name", cls="border p-2"),
        ),
        Td(
            Input(name="email", placeholder="Enter email", cls="border p-2"),
        ),
        Td(
            Input(name="role", placeholder="Enter role", cls="border p-2"),
        ),
        Td(""),  # Empty cell for last_modified
        Td(
            Button("Add", cls="bg-green-500 text-white p-2"),
        ),
        # hx_get specifies the URL to send a GET request to when the element
        # is triggered. when the form is submitted, a GET request will be
        # sent to the /api/records endpoint to retrieve the updated list of records.
        hx_get="/api/records",
        # The hx_post parameter specifies the URL where the POST request
        # is sent when the form is submitted.
        hx_post="/api/records",
        # hx_swap specifies how to swap the content of the target element
        # with the response from the server. hx_swap="beforeend" means
        # that the server response will be inserted before the end of
        # the #records-table element. This is useful for adding new records
        # to the table without replacing the existing content.
        hx_swap="beforeend",
        # hx_target specifies the CSS selector of the element to
        # update with the response from the server.
        hx_target="#records-table",
        # hx_trigger identifies the event that triggers the request. it means
        # the request will be triggered when the form is loaded. However, it is
        # not the only trigger - the form will also be submitted when
        # the user clicks the "Add" button, which is the default behavior
        # for a form.
        hx_trigger="load"
    )

def create_filter_header(field):
    logger.info(f"create_filter_header(field: {field})")

    return Th(
        Input(
            name=f"filter_{field}",
            placeholder=f"Filter {field}...",
            cls="w-full border p-1 mt-1",
            hx_get="/api/records",
            hx_include="[name^='filter_']",
            hx_target="#records-table",
            hx_trigger="keyup changed delay:500ms"
        )
    )


def create_record_row(record):
    logger.info(f"create_record_row({record})")

    return Tr(
        Td(
            Div(
                record["name"],
                hx_get=f"/api/records/{record['id']}/edit/name",
                hx_swap="innerHTML",
                hx_target="closest td",
                hx_trigger="click"
            ),
            cls="border p-2"
        ),
        Td(
            Div(
                record["email"],
                hx_get=f"/api/records/{record['id']}/edit/email",
                hx_swap="innerHTML",
                hx_target="closest td",
                hx_trigger="click"
            ),
            cls="border p-2"
        ),
        Td(
            Div(
                record["role"],
                hx_get=f"/api/records/{record['id']}/edit/role",
                hx_swap="innerHTML",
                hx_target="closest td",
                hx_trigger="click"
            ),
            cls="border p-2"
        ),
        Td(record.get("last_modified", ""), cls="border p-2"),
        Td(
            # I've also added hx_trigger="load" and
            # hx_get="/api/records" to the delete button in
            # the create_record_row function. This will trigger
            # a refresh of the records list after a record is
            # deleted.
            Button(
                "Delete",
                cls="bg-red-500 text-white p-2",
                hx_delete=f"/api/records/{record['id']}",
                hx_get="/api/records",
                hx_swap="outerHTML",
                hx_target="#records-table",
                hx_trigger="load"
            ),
            cls="border p-2"
        )
    )
@rt("/")
async def get():
    logger.info(f"get()")

    records = await call_mock_db("GET", "records")

    return Html(
        Titled(
        "Employees - A CRUD Grid Demo"
        ),
        Style("""
            table { width: 100%; border-collapse: collapse; margin: 1em 0; }
            th, td {
                border: 1px solid #ddd;
                padding: 8px;
                text-align: left;
            }
            th { background-color: #f5f5f5; }
            tr:hover { background-color: #f9f9f9; }
        """),
        Container(
            Table(
                Thead(
                    Tr(
                        Th(H3("Name"), cls="text-left"),
                        Th(H3("Email"), cls="text-left"),
                        Th(H3("Role"), cls="text-left"),
                        Th(H3("Last Modified"), cls="text-left"),
                        Th(H3("Actions"), cls="text-left"),
                    ),
                    Tr(
                        create_add_form(),
                    ),
                    Tr(
                        create_filter_header("name"),
                        create_filter_header("email"),
                        create_filter_header("role"),
                        Th(""),  # Empty cell for last_modified
                        Th("")   # Empty cell for actions
                    )
                ),
                Tbody(
                    *[create_record_row(record) for record in records],
                    id="records-table"
                ),
                cls="w-full border-collapse table-fixed"
            )
        )
    )

@rt("/api/records")
async def get(filter_name: str = "", filter_email: str = "", filter_role: str = ""):
    logger.info(f"get(filter_name: {filter_name}, filter_email: {filter_email}, filter_role: {filter_role})")

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
    logger.info(f"post(name: {name}, email: {email}, role: {role})")

    record = await call_mock_db("POST", "records", json={"name": name, "email": email, "role": role})
    return create_record_row(record)

@rt("/api/records/{id}")
async def delete(id: int):
    logger.info(f"delete(id: {id})")

    await call_mock_db("DELETE", f"records/{id}")
    return ""

@rt("/api/records/{id}/edit/{field}")
async def get(id: int, field: str):
    logger.info(f"get(id: {id}, field: {field})")

    record = await call_mock_db("GET", f"records/{id}")

    return Form(
        Input(
            value=record[field],
            name="value",
            cls="border p-1"
        ),
        Button("Save", cls="bg-green-500 text-white p-1"),
        hx_put=f"/api/records/{id}/field/{field}",
        hx_swap="innerHTML",
        hx_target="closest td"
    )

@rt("/api/records/{id}/field/{field}")
async def put(id: int, field: str, value: str):
    logger.info(f"put(id: {id}, field: {field}, value: {value})")

    record = await call_mock_db("PUT", f"records/{id}", params={"field": field, "value": value})
    return Div(
        record[field],
        hx_get=f"/api/records/{id}/edit/{field}",
        hx_swap="innerHTML",
        hx_target="closest td",
        hx_trigger="click"
    )

if __name__ == "__main__":
    serve(app, port=8001)