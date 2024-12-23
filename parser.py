"""
usage: python3 parser.py
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, Response, UploadFile
from fastapi.responses import FileResponse

from sd_parsers import ParserManager
import webbrowser
import uvicorn
import os


PORT = int(os.environ.get("PORT", 8000))


parser_manager = ParserManager()


@asynccontextmanager
async def lifespan(app: FastAPI):
    webbrowser.open(f"http://127.0.0.1:{PORT}")
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
def index():
    return FileResponse("index.html")


@app.post("/api/parse")
def parse(image: UploadFile):
    try:
        info = parser_manager.parse(image.file)
        if info is None:
            return {"error": "no metadata found"}

        return Response(content=info.to_json(), media_type="application/json")

    except Exception as error:
        return {"error": str(error)}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=PORT)
