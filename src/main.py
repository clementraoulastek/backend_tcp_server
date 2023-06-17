import uvicorn

from src.tools.constant import MAIN_APP, SERVER_IP, SERVER_PORT

if __name__ == "__main__":
    uvicorn.run(MAIN_APP, host=SERVER_IP, port=SERVER_PORT)
