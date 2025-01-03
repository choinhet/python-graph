from pathlib import Path
from typing import List
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from pydantic import BaseModel
import uvicorn
import logging

log = logging.getLogger("uvicorn")

app = FastAPI()
app.mount(
    "/resources", StaticFiles(directory="python_graph/resources"), name="resources"
)

templates = Jinja2Templates(directory="python_graph/templates")


class NodeEdge(BaseModel):
    name: str
    node_type: str


class Node(BaseModel):
    name: str
    inputs: List[NodeEdge]
    outputs: List[NodeEdge]


nodes = [
    Node(
        name="Node 1",
        inputs=[NodeEdge(name="Input 1", node_type="int")],
        outputs=[NodeEdge(name="Output 1", node_type="int")],
    ),
    Node(
        name="Node 2",
        inputs=[NodeEdge(name="Input 2", node_type="int")],
        outputs=[NodeEdge(name="Output 2", node_type="int")],
    ),
]


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse(
        "index.html", {"request": request, "nodes": nodes}
    )


@app.post("/nodes/search", response_class=HTMLResponse)
async def search_nodes(request: Request):
    form = await request.form()
    search_term = form.get("search", "")
    filtered_nodes = [
        node for node in nodes if search_term.lower() in node.name.lower()
    ]

    template = templates.get_template("index.html")
    return template.module.node_list(nodes=filtered_nodes)


@app.get("/workflow/load", response_class=HTMLResponse)
async def load_workflow(request: Request):
    log.info("Loading workflow")
    return templates.TemplateResponse(
        "index.html", {"request": request, "nodes": nodes}
    )


@app.get("/workflow/save", response_class=HTMLResponse)
async def save_workflow(request: Request):
    log.info("Saving workflow")
    return templates.TemplateResponse(
        "index.html", {"request": request, "nodes": nodes}
    )


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
