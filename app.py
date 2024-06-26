import uvicorn

from src.initializer import get_app

if __name__ == '__main__':
    app = get_app()
    uvicorn.run(app, host="127.0.0.1", port=5002)
