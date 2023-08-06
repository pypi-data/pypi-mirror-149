from __init__ import *
from directives import *
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

@test("add_server should create a new server")
def _():
    configuration = parse_combined(Path(__file__).parent.parent / "fixtures" / "empty.conf")

    configuration.add_server("queyd.ewen.works", 80, 
        location("/graphql", 
            if_('$http_authentication != "Bearer hunter2"', 
                return_(403, "https://queyd.ewen.works/unauthorized.html")
            ),
            proxy_pass("http://localhost:8080") 
        )
    )

    assert configuration.build() == """
server queyd.ewen.works 80 {
    location /graphql {
        if ($http_authentication != 'Bearer hunter2') {
            return 403 https://queyd.ewen.works/unauthorized.html;
        }
        proxy_pass http://localhost:8080;
    }
}
    """.strip()
