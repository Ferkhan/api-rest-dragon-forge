from app import create_app
import uvicorn

app = create_app()

if __name__ == "__main__":
    uvicorn.run("main:app", port=8080, reload=True)    