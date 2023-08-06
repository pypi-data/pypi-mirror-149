import contextlib
from dataclasses import dataclass
from itertools import product
from pathlib import Path
from typing import Callable
import crossplane

with contextlib.suppress(ImportError):
    from rich import print

# def DirectiveNamed(name: str) -> Type[NamedTuple]:
#     return NamedTuple(name, line=int)
#
# class AbsoluteRedirect(DirectiveNamed("absolute_redirect")):
#     value: bool
#

global current_line
current_line = 0


@dataclass
class Directive:
    name: str
    args: list[str | int | bool]
    includes: list["ConfigurationFile"] | None = None
    block: list["Directive"] | None = None
    comment: str | None = None

    def json_ready(self) -> dict:
        global current_line
        current_line += 1
        d = {
            "directive": self.name,
            "line": current_line,
            "args": self.args,
        }
        if self.block is not None:
            d["block"] = [d.json_ready() for d in self.block]

        if self.name == "include":
            d["includes"] = self.includes or []

        if self.name == "#":
            d["comment"] = self.comment

        return d

    def __repr__(self) -> str:
        return f"{self.name} {' '.join(map(str, self.args))}" + (
            " { ... }" if self.block != None else ""
        )

    def walk(self, do: Callable[[int, "Directive"], None]):
        if self.block:
            for i, d in enumerate(self.block):
                do(i, d)
                d.walk(do)

    @property
    def args_str(self) -> str:
        return " ".join(map(str, self.args))
    
    def __eq__(self, __o: object) -> bool:
        return self.__dict__ == __o.__dict__


def _without(directive_name: str, directives: list[Directive]) -> list[Directive]:
    return [d for d in directives if d.name != directive_name]


def _index_of_first(directive_name: str, directives: list[Directive]) -> int:
    for i, d in enumerate(directives):
        if d.name == directive_name:
            return i
    return None


def _index_of_last(directive_name: str, directives: list[Directive]) -> int:
    matches = [i for i, d in enumerate(directives) if d.name == directive_name]
    if len(matches):
        return matches[-1]
    return None


def _index_of(
    predicate: Callable[[Directive], bool], directives: list[Directive]
) -> int:
    for i, d in enumerate(directives):
        if predicate(d):
            return i
    return None


@dataclass
class Server(Directive):
    def __init__(self, _directive=None, **kwargs):
        super().__init__(**({"name": "server", "args": [], "block": []} | kwargs))
        self._directive = _directive

    @property
    def locations(self) -> list[Directive]:
        return [l for l in self.block if l.name == "location"]

    @locations.setter
    def locations(self, locations: list[Directive]):
        first_location_was_at = _index_of_first("location", self.block) or 0
        self.block = (
            self.block[:first_location_was_at]
            + locations
            + _without("location", self.block[first_location_was_at:])
        )
        self._directive.block = self.block

    def set_location(self, pattern: str, *directives: list[Directive]):
        new_location = Directive(name="location", args=[pattern], block=directives)

        if pattern not in [l.args_str for l in self.locations]:
            self.block.insert(
                (_index_of_last("location", self.block) or -1) + 1, new_location
            )
            self._directive.block = self.block
        else:
            self.locations = [
                l if l.args_str != pattern else new_location for l in self.locations
            ]

    @property
    def headers(self) -> list[Directive]:
        return [h for h in self.block if h.name == "add_header"]

    @headers.setter
    def headers(self, headers: list[Directive]):
        first_header_was_at = _index_of_first("add_header", self.block) or 0
        self.block = (
            self.block[:first_header_was_at]
            + headers
            + _without("add_header", self.block[first_header_was_at:])
        )
        if self._directive:
            self._directive.block = self.block

    def set_header(self, header: str, value: str):
        new_header = Directive(name="add_header", args=[header, value])
        if header not in [h.args[0] for h in self.headers]:
            self.add_header(header, value)
        else:
            self.headers = [
                h if h.args[0] != header else new_header for h in self.headers
            ]
    
    def add_header(self, header: str, value: str):
        new_header = Directive(name="add_header", args=[header, value])
        self.block.insert(
            (_index_of_last("add_header", self.block) or -1) + 1, new_header
        )
        if self._directive:
            self._directive.block = self.block
    

    @property
    def error_pages(self) -> list[Directive]:
        return [e for e in self.block if e.name == "error_page"]

    @error_pages.setter
    def error_pages(self, error_pages: list[Directive]):
        first_error_page_was_at = _index_of_first("error_page", self.block) or 0
        self.block = (
            self.block[:first_error_page_was_at]
            + error_pages
            + _without("error_page", self.block[first_error_page_was_at:])
        )
        self._directive.block = self.block

    def set_error_page(self, code: int, url: str):
        new_error_page = Directive(name="error_page", args=[str(code), url])
        if code not in [e.args_str for e in self.error_pages]:
            self.block.insert(
                (_index_of_last("error_page", self.block) or -1) + 1, new_error_page
            )
            self._directive.block = self.block
        else:
            self.error_pages = [
                e if e.args_str != code else new_error_page for e in self.error_pages
            ]


@dataclass
class ConfigurationFile:
    filepath: Path
    directives: list[Directive]

    def dict(self) -> dict:
        return {
            "file": str(self.filepath),
            "status": "ok",
            "errors": [],
            "parsed": [d.json_ready() for d in self.directives],
        }

    def build(self) -> str:
        return crossplane.build(self.dict()["parsed"])

    def server(self, name: str, port: int) -> Server:
        for d in self.directives:
            if (
                d.name == "server"
                and name == [s.args[0] for s in d.block if s.name == "server_name"][0]
                and str(port) == [s.args[0] for s in d.block if s.name == "listen"][0]
            ):
                return Server(
                    _directive=d,
                    name="server",
                    args=d.args,
                    block=d.block,
                )
        raise KeyError(f"No server with server_name {name!r} and port {port!r}")

    def walk(self, do: Callable[[int, Directive], None]):
        for i, d in enumerate(self.directives):
            do(i, d)
            d.walk(do)


@dataclass
class NGINXConfiguration:
    files: list[ConfigurationFile]

    def build(self) -> dict[str, str]:
        return {
            f.filepath: str(crossplane.build(f.dict()["parsed"])) for f in self.files
        }

    def __getitem__(self, __name: str) -> ConfigurationFile:
        if (
            len(
                matches := [
                    f
                    for f in self.files
                    if __name in {str(f.filepath), f.filepath.name}
                ]
            )
            > 0
        ):
            return matches[0]
        raise AttributeError(f"No such file: {__name}. Available files: {self.files}")


def _parse(filepath: str | Path, combine: bool = False) -> list[ConfigurationFile]:
    response = crossplane.parse(str(filepath), combine=combine, comments=True)
    if response["status"] == "failed":
        raise Exception(
            f"The following errors occured while parsing {filepath}: \n"
            + "\n".join(
                f"· {e['file']}:{e['line']} {e['error']}" for e in response["errors"]
            )
        )

    return [
        ConfigurationFile(
            filepath=Path(file["file"]),
            directives=list(map(_instanciate_directive, file["parsed"])),
        )
        for file in response["config"]
    ]


def parse(filepath: str | Path) -> NGINXConfiguration:
    return NGINXConfiguration(_parse(filepath, combine=False))


def parse_combined(filepath: str | Path) -> ConfigurationFile:
    return _parse(filepath, combine=True)[0]


def _instanciate_directive(directive: dict) -> Directive:
    d = Directive(
        name=directive["directive"],
        args=directive["args"],
        block=None,
        includes=directive.get("includes"),
        comment=directive.get("comment"),
    )
    if directive.get("block"):
        d.block = list(map(_instanciate_directive, directive["block"]))

    return d
