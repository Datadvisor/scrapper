import asyncio
import logging
import os

import grpc

from sys import argv

from src.grpc_communication.scrapper.scrapper_pb2_grpc import ScrapperServiceServicer, \
    add_ScrapperServiceServicer_to_server
from src.grpc_communication.scrapper.scrapper_pb2 import GetByNameResponse, GetByEmailResponse, GetByFaceResponse, \
    GetByResumeResponse

from src.website.google_search_engine import search_in_google

from src.mail_request import search_mail

from src.face.face_processing import faces_compare

from src.cv.read import read_cv


class Scrapper(ScrapperServiceServicer):

    async def GetByName(self, request, context) -> GetByNameResponse:
        query = request.firstName + ' ' + request.lastName

        response = search_in_google(query, request.demo)

        return GetByNameResponse(data=response['SocialNetworks'])

    async def GetByEmail(self, request, context) -> GetByEmailResponse:
        response = search_mail(request.email)

        return GetByEmailResponse(data=response['result'])

    async def GetByFace(self, request, context) -> GetByFaceResponse:
        query = request.firstName + ' ' + request.lastName
        file_path = 'data/' + request.fileName

        with open(file_path, 'wb') as file:
            file.write(request.fileContent)

        res = faces_compare('data/' + query.replace(' ', ''), file_path, query)

        return GetByFaceResponse(res)

    async def GetByResume(self, request, context):
        file_path = 'data/' + request.fileName

        with open(file_path, 'wb') as file:
            file.write(request.fileContent)

        res = read_cv(file_path)

        return GetByResumeResponse(data=res[0])


async def serve(port) -> None:
    server = grpc.aio.server()
    listen_addr = f'[::]:{port}'

    add_ScrapperServiceServicer_to_server(Scrapper(), server)
    server.add_insecure_port(listen_addr)
    logging.info("Starting server on %s", listen_addr)

    await server.start()
    await server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(serve(os.getenv('GRPC_PORT')))
