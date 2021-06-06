import uvicorn as uvicorn
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from api.api import api_router
from utils.doc_utils import get_code_samples

app = FastAPI()

API_PREFIX = '/api/v1'
app.include_router(router=api_router, prefix=API_PREFIX)


def custom_openapi():
    # cache the generated schema
    if app.openapi_schema:
        return app.openapi_schema

    # custom settings
    openapi_schema = get_openapi(
        title="Sample Project",
        version='0.0.1',
        routes=app.routes,
    )
    for route in app.routes:
        if route.path.startswith(API_PREFIX) and '.json' not in route.path:
            for method in route.methods:
                if method.lower() in openapi_schema["paths"][route.path]:
                    code_samples = get_code_samples(route=route, method=method)
                    openapi_schema["paths"][route.path][method.lower()]["x-codeSamples"] = code_samples

    app.openapi_schema = openapi_schema

    return app.openapi_schema


# assign the customized OpenAPI schema
app.openapi = custom_openapi

if __name__ == '__main__':
    uvicorn.run('main:app')
