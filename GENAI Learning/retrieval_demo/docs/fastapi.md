# FastAPI

FastAPI is a modern, fast (high-performance), web framework for building APIs with Python based on standard Python type hints.

## Key Features

- **Fast**: Very high performance, on par with NodeJS and Go (thanks to Starlette and Pydantic). One of the fastest Python frameworks available.
- **Fast to code**: Increase the speed to develop features by about 200% to 300%.
- **Fewer bugs**: Reduce about 40% of human (developer) induced errors.
- **Intuitive**: Great editor support. Completion everywhere. Less time debugging.
- **Easy**: Designed to be easy to use and learn. Less time reading docs.
- **Short**: Minimize code duplication. Multiple features from each parameter declaration.
- **Robust**: Get production-ready code. With automatic interactive documentation.
- **Standards-based**: Based on (and fully compatible with) the open standards for APIs: OpenAPI and JSON Schema.

---

## Installation

```bash
pip install fastapi
pip install "uvicorn[standard]"
```

---

## First Steps

Create a file `main.py` with:

```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}
```

Run the server with:

```bash
uvicorn main.py:app --reload
```

---

## Path Parameters

You can declare path parameters with the same syntax used by Python format strings:

```python
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}
```

The value of the path parameter `item_id` will be passed to your function as the argument `item_id`. FastAPI automatically validates and converts the type — if you pass a non-integer, a clear HTTP error is returned.

### Predefined values with Enum

If you have a path operation that receives a path parameter, but you want the possible valid values to be predefined, you can use a standard Python `Enum`:

```python
from enum import Enum
from fastapi import FastAPI

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

app = FastAPI()

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}
    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}
    return {"model_name": model_name, "message": "Have some residuals"}
```

---

## Query Parameters

When you declare other function parameters that are not part of the path parameters, they are automatically interpreted as "query" parameters:

```python
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]
```

The query is the set of key-value pairs that go after the `?` in a URL, separated by `&` characters. For example: `/items/?skip=0&limit=10`.

### Optional parameters

The same way, you can declare optional query parameters, by setting their default to `None`:

```python
from typing import Union

@app.get("/items/{item_id}")
async def read_item(item_id: str, q: Union[str, None] = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}
```

---

## Request Body

When you need to send data from a client to your API, you send it as a request body. A request body is data sent by the client to your API. A response body is data your API sends to the client.

To declare a request body, you use Pydantic models:

```python
from fastapi import FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

app = FastAPI()

@app.post("/items/")
async def create_item(item: Item):
    return item
```

FastAPI will:
- Read the body of the request as JSON.
- Convert the corresponding types.
- Validate the data. If invalid, it returns a clear error.
- Give you the received data in the parameter `item`.
- Generate JSON Schema definitions for your model.

---

## Response Model

You can declare the model used for the response with the parameter `response_model` in any path operation:

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list[str] = []

@app.post("/items/", response_model=Item)
async def create_item(item: Item) -> Item:
    return item
```

FastAPI will use the `response_model` to filter the output data and limit it to what is defined in the model, even if there are extra fields.

---

## Dependencies

FastAPI has a powerful but intuitive Dependency Injection system. Dependencies can be functions, classes, or other callables. Use `Depends` to declare them:

```python
from typing import Annotated
from fastapi import Depends, FastAPI

app = FastAPI()

async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}

@app.get("/items/")
async def read_items(commons: Annotated[dict, Depends(common_parameters)]):
    return commons
```

Dependencies can have sub-dependencies, and FastAPI resolves the entire dependency graph automatically.

---

## Security

FastAPI provides several tools to handle security, authentication, and authorization. It integrates well with OAuth2, JWT tokens, and API keys.

### OAuth2 with Password (Bearer)

```python
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}
```

---

## Middleware

You can add middleware to FastAPI applications. A "middleware" is a function that works with every request before it is processed by any specific path operation, and with every response before returning it:

```python
import time
from fastapi import FastAPI, Request

app = FastAPI()

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
```

---

## Background Tasks

You can define background tasks to be run after returning a response:

```python
from fastapi import BackgroundTasks, FastAPI

app = FastAPI()

def write_notification(email: str, message: str = ""):
    with open("log.txt", mode="w") as email_file:
        content = f"notification for {email}: {message}"
        email_file.write(content)

@app.post("/send-notification/{email}")
async def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_notification, email, message="some notification")
    return {"message": "Notification sent in the background"}
```

---

## Testing

FastAPI applications are easy to test. Using `pytest` and `httpx`:

```python
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}
```

---

## Deployment

FastAPI is ready for production deployment. Common options include:

- **Uvicorn** — ASGI server, great for development and simple deployments.
- **Gunicorn + Uvicorn workers** — recommended for production.
- **Docker** — containerize your application for consistent deployments.
- **Kubernetes** — for large-scale orchestration.

A typical production command:

```bash
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:80
```

---

## Async Support

FastAPI is built on top of Starlette and supports `async`/`await` natively. You can declare path operation functions as `async def` or regular `def`. FastAPI handles both correctly:

```python
@app.get("/async-item/")
async def read_async_item():
    result = await some_async_function()
    return result

@app.get("/sync-item/")
def read_sync_item():
    result = some_sync_function()
    return result
```

Sync functions are run in a thread pool to avoid blocking the event loop.

---

## WebSockets

FastAPI supports WebSockets natively:

```python
from fastapi import FastAPI, WebSocket

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")
```

---

## OpenAPI & Docs

FastAPI automatically generates:
- **Swagger UI** at `/docs`
- **ReDoc** at `/redoc`
- **OpenAPI JSON** at `/openapi.json`

No extra configuration needed. The interactive documentation lets you explore and test your API directly from the browser.
