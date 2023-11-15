from fastapi import Depends, FastAPI, HTTPException, Security
from fastapi.security.api_key import APIKey, APIKeyCookie, APIKeyHeader, APIKeyQuery
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi

from starlette.status import HTTP_403_FORBIDDEN
from starlette.responses import JSONResponse, RedirectResponse

from app.config import settings


api_key_query = APIKeyQuery(name=settings.API_KEY_NAME, auto_error=False)
api_key_header = APIKeyHeader(name=settings.API_KEY_NAME, auto_error=False)
api_key_cookie = APIKeyCookie(name=settings.API_KEY_NAME, auto_error=False)

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)


async def get_api_key(
    api_key_query: str = Security(api_key_query),
    api_key_header: str = Security(api_key_header),
    api_key_cookie: str = Security(api_key_cookie),
):

    if api_key_query == settings.API_KEY:
        return api_key_query
    elif api_key_header == settings.API_KEY:
        return api_key_header
    elif api_key_cookie == settings.API_KEY:
        return api_key_cookie
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="Could not validate credentials"
        )
    

@app.get("/")
async def homepage():
    return 'Welcome to the security test!'


@app.get("/openapi.json", tags=["documentation"])
async def get_open_api_endpoint(api_key: APIKey = Depends(get_api_key)):
    response = JSONResponse(get_openapi(title="FastAPI security test docs", version='1', routes=app.routes))
    return response


@app.get("/documentation", tags=["documentation"])
async def get_documentation(api_key: APIKey = Depends(get_api_key)):
    response = get_swagger_ui_html(openapi_url="/openapi.json", title="docs")
    response.set_cookie(
        settings.API_KEY_NAME,
        value=api_key,
        domain=settings.COOKIE_DOMAIN,
        httponly=True,
        max_age=1800,
        expires=1800,
    )
    return response


@app.get("/logout")
async def route_logout_and_remove_cookie():
    response = RedirectResponse(url="/")
    response.delete_cookie(settings.API_KEY_NAME, domain=settings.COOKIE_DOMAIN)
    return response


@app.get("/secure_endpoint", tags=["test"])
async def get_open_api_endpoint(api_key: APIKey = Depends(get_api_key)):
    response = "How cool is this?"
    return response
