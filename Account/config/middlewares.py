# In the name of GOD

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

    async def encrypte_internal_response(self, request: Request, response: Response):
        if internal_service:= SERVICE_CLASSES.get(request.headers.get("internal-service")):
            resp_body = [section.decode() async for section in response.__dict__['body_iterator']]
            resp_body = internal_service.Encrypt_tools.encrypt_data("\n".join(resp_body))
            response.__setattr__('body_iterator', aiwrap([section.encode() for section in resp_body.split("\n")]))
            response.headers['content-length'] = f"{len(resp_body)}"
        return response


    async def dispatch(self, request, call_next):
        # decrypte body of internal services requests
        self.current_request = request
        await self.decrypte_internal_requests(request)
        response = await call_next(request)
        response = await self.encrypte_internal_response(request, response)
        return response


    # async def __call__(self, scope, receive, send):
    #     if scope["type"] != "http":
    #         what = await self.app(scope, receive, send)
    #         return
    #     body_size = 0

    #     async def receive_logging_request_body_size():
    #         nonlocal body_size
    #         message = await receive()
    #         assert message["type"] == "http.request"
    #         body_size += len(message.get("body", b""))
    #         if not message.get("more_body", False):
    #             print(f"Size of request body was: {body_size} bytes")
    #         print(f"\n{'=='*25}\nmessage: {message}\t message type: {type(message)}\n")
    #         return message

    #     async def send_with_reader(message):
    #         print(f"\n {'=='*25}\ngetattr(self, \'current_request\', None)  : {getattr(self, 'current_request', None)}\n")
    #         if message["type"] == "http.response.body":
    #             print("iiiiiiiiiiiiiiiiiiiiiiiiiiiiiii")
    #             # Read the response body as bytes
    #             message['body'] = await self.encrypte_internal_response(self.current_request, message['body'].decode())
    #             body = message.get("body", b"")
    #             # Decode the bytes to a string
    #             body_str = body.decode()
    #             # Print the response body to the console
    #             print(f"Response body: {body_str}")
    #         print(f"\n {'=='*25}\nmessage in sendss: {message}\t message type: {type(message)}\n")
    #         await send(message)

    #     await super().__call__(scope, receive_logging_request_body_size, send_with_reader)

        # async def encrypte_internal_response(self, request: Request, message: bytes):
    #     if internal_service:= SERVICE_CLASSES.get(request.headers.get("internal-service")):
    #         # # Consuming FastAPI response and grabbing body here
    #         # resp_body = [section async for section in response.__dict__['body_iterator']]
    #         # # Repairing FastAPI response
    #         # response.__setattr__('body_iterator', aiwrap(resp_body)
    #         message = internal_service.Encrypt_tools.encrypt_data(message)
    #     return message.encode()
        
