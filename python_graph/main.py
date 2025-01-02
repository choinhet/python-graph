from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import uvicorn

app = FastAPI()
app.mount(
    "/resources", StaticFiles(directory="python_graph/resources"), name="resources"
)

templates = Jinja2Templates(directory="python_graph/templates")


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
