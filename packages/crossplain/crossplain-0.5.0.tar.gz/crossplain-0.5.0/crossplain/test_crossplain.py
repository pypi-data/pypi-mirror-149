from __init__ import *
from directives import add_header
from ward import test

@test("set_header should not generate duplicates")
def _():
    server = Server()
    server.set_header("Access-Control-Allow-Origin", "*")
    server.set_header("Access-Control-Allow-Origin", "*")

    assert server.headers == [add_header("Access-Control-Allow-Origin", "*")]



@test("add_header can generate duplicates")
def _():
    server = Server()
    server.add_header("Access-Control-Allow-Origin", "*")
    server.add_header("Access-Control-Allow-Origin", "*")

    assert server.headers == [
        add_header("Access-Control-Allow-Origin", "*"),
        add_header("Access-Control-Allow-Origin", "*")
    ]
