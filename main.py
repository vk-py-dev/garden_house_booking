import os
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from routers import router
import uvicorn

project_dir = os.path.dirname(__file__)
st_abs_file_path = os.path.join(project_dir, "static/")

app = FastAPI()
app.mount("/static", StaticFiles(directory=st_abs_file_path), name="static")
app.include_router(router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
