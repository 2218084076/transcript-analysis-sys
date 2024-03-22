import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from transcript_analysis_sys.rest_api import router
from transcript_analysis_sys.utils.log import init_log

app = FastAPI()
app.include_router(router, prefix='/api/v1')
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def start(host: str, port: int):
    """
    start
    :param host:
    :param port:
    :return:
    """
    uvicorn.run(app, host=host, port=port)


if __name__ == '__main__':
    init_log()
    start('0.0.0.0', 8082)
