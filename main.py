import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette import status
from starlette.responses import PlainTextResponse, JSONResponse

from controllers.c_admin import admin_route
from controllers.c_employer import employer_router
from controllers.HistoryController import history_router

app = FastAPI()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: RequestValidationError):
    type_ = exc.errors()[0]['type']
    filed_ = exc.errors()[0]['loc']

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={type_: filed_}
    )


app.include_router(admin_route)
app.include_router(employer_router)
app.include_router(history_router)


@app.get('/')
def home():
    return "Hello Man"


if __name__ == '__main__':
    uvicorn.run("main:app", reload=True, port=8089)
