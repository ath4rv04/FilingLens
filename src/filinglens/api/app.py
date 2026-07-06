from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from filinglens.api.config import api_settings
from filinglens.api.routes import router
from filinglens.api.middleware import TimingMiddleware
from filinglens.api.exceptions import (
    file_not_found_handler,
    value_error_handler,
    validation_exception_handler,
    runtime_error_handler,
    generic_exception_handler,
)

app = FastAPI(
    title=api_settings.title,
    description=api_settings.description,
    version=api_settings.version,
    contact={"name": "FilingLens Maintenance"},
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=api_settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(TimingMiddleware)

app.add_exception_handler(FileNotFoundError, file_not_found_handler)
app.add_exception_handler(ValueError, value_error_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(RuntimeError, runtime_error_handler)
app.add_exception_handler(Exception, generic_exception_handler)

app.include_router(router)
