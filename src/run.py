import uvicorn

from src.settings import SETTINGS


def main():
    uvicorn.run(
        "src.api.main:app",
        host=SETTINGS.api_host,
        port=SETTINGS.api_port,
        reload=SETTINGS.api_reload,
    )


if __name__ == "__main__":
    main()
