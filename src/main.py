import asyncio
import logging

import grpc

from grpc_communication.scrapper.scrapper_pb2_grpc import ScrapperServiceServicer, add_ScrapperServiceServicer_to_server
from grpc_communication.scrapper.scrapper_pb2 import GetByNameResponse, GetByEmailResponse, GetByFaceResponse, GetByResumeResponse

from website.google_search_engine import search_in_google

from request_handler import response_format

from mail_request import search_mail

from face.face_processing import faces_compare

from cv.read import read_cv


class Scrapper(ScrapperServiceServicer):

    async def GetByName(self, request, context) -> GetByNameResponse:
        query = request.firstName + ' ' + request.lastName

        response = search_in_google(query)

        return GetByNameResponse(data=response['SocialNetworks'])

    async def GetByEmail(self, request, context) -> GetByEmailResponse:
        response = search_mail(request.email)

        return GetByEmailResponse(data=response['result'])

    async def GetByFace(self, request_iterator, context) -> GetByFaceResponse:
        data = bytearray()
        filepath = None
        query = None
        res = None

        async for request in request_iterator:
            if request.metadata.filename and request.metadata.extension:
                filepath = f'data/{request.metadata.filename.split("/")[-1]}{request.metadata.extension}'
                query = f'{request.metadata.firstName} {request.metadata.lastName}'
                continue
            data.extend(request.chunk_data)
            with open(filepath, 'wb') as f:
                f.write(data)

        if query and filepath:
             res = faces_compare(f'data/{query.replace(" ", "")}', filepath, query)

        return GetByFaceResponse(res)


    async def GetByResume(self, request_iterator, context):
        data = bytearray()
        filepath = None

        async for request in request_iterator:
            if request.metadata.filename and request.metadata.extension:
                filepath = f'data/{request.metadata.filename.split("/")[-1]}{request.metadata.extension}'
                continue
        data.extend(request.chunk_data)
        with open(filepath, 'wb') as f:
            f.write(data)

        if filepath:
            res = read_cv(filepath)

        return GetByResumeResponse(data=res[0])


async def serve() -> None:
    server = grpc.aio.server()
    listen_addr = '[::]:8002'

    add_ScrapperServiceServicer_to_server(Scrapper(), server)
    server.add_insecure_port(listen_addr)
    logging.info("Starting server on %s", listen_addr)

    await server.start()
    await server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(serve())