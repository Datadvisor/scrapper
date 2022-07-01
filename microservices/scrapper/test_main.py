#!/usr/bin/env python3

"""
        scrapper

    Author: bricetoffolon
    Created on: 01/07/2022
    About: 

"""

from fastapi.testclient import TestClient

from src.api.api import app

client = TestClient(app)


def test_search_by_mail_sucess():
    response = client.get('/search_by_mail?query=someone@example.com')
    assert response.status_code == 200
    assert response.json()['success'] == True


def test_search_by_mail_empty():
    response = client.get('/search_by_mail?query=')
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Can't perform request for this query: "
    }


def test_search_by_mail_wrong_mail():
    response = client.get('/search_by_mail?query=someone')
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Can't perform request for this query: someone - invalid mail"
    }
