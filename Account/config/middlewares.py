from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import Scope, Receive, Message
from fastapi import Request, Response

from services import SERVICE_CLASSES
from utils.async_iterator import async_iterator_wrapper as aiwrap

class InternalSecurityMiddleware(BaseHTTPMiddleware):

    async def decrypte_internal_requests(self, request: Request):
        recieve_ = await request._receive()
        if internal_service:= SERVICE_CLASSES.get(request.headers.get("internal-service")):
            body = recieve_.get("body").decode().strip("\"").encode()
            recieve_["body"] = internal_service.Encrypt_tools.decrypt_data(body).encode()
        async def recieve() -> Message:
            return recieve_

        request._receive = recieve

    async def dispatch(self, request, call_next):
        # decrypte body of internal services requests
        self.current_request = request
        await self.decrypte_internal_requests(request)
        response = await call_next(request)
        response = await self.encrypte_internal_response(request, response)
        return response

