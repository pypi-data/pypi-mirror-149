from crossplain import Directive
from crossplain.utils import split_expression


def location(path_pattern: str, *directives) -> Directive:
    return Directive(
        name="location",
        args=path_pattern.split(" "),
        block=list(directives),
    )


def try_files(*things) -> Directive:
    return Directive(name="try_files", args=list(things))


def error_page(code: int, *files) -> Directive:
    return Directive(name="error_page", args=[str(code)] + list(files))


def add_header(header: str, value: str) -> Directive:
    return Directive(name="add_header", args=[header, value])


def autoindex(on: bool = True) -> Directive:
    return Directive(name="autoindex", args=["on" if on else "off"])


def autoindex_format(format: str) -> Directive:
    return Directive(name="autoindex_format", args=[format])


def xslt_stylesheet(filepath: str) -> Directive:
    return Directive(name="xslt_stylesheet", args=[filepath])


def charset(encoding: str) -> Directive:
    return Directive(name="charset", args=[encoding])


def types(typesmap: dict[str, str | list[str]]) -> Directive:
    return Directive(
        name="types",
        args=[],
        block=list(
            map(
                lambda t: Directive(
                    name=t[0], args=[t[1]] if isinstance(t[1], str) else t[1]
                ),
                typesmap.items(),
            )
        ),
    )


def if_(condition: str, *directives) -> Directive:
    return Directive(name="if", args=split_expression(condition), block=list(directives))


def return_(code: int, url_or_text: str = "") -> Directive:
    return Directive(name="return", args=(
        [str(code), url_or_text] if url_or_text and code 
        else [str(code)] 
        if code 
        else [url_or_text]
    ))


def comment(text: str) -> Directive:
    return Directive(name="#", args=[], comment=" " + text)


def proxy_pass(url: str) -> Directive:
    return Directive(name="proxy_pass", args=[url])
