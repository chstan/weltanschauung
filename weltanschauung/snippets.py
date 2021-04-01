from pathlib import Path
from weltanschauung.utils import read_template, read_resource

__all__ = [
    "SNIPPETS",
    "append_snippet",
]


class FileSnippet:
    def __init__(self, filename: str):
        self.filename = filename

    def __repr__(self):
        return f"Snippet {self.filename}"

    def _repr_html_(self):
        template = read_template(Path("html/snippet.html"))

        return template.render(
            header=str(self),
            content="<pre>{}</pre>".format(read_resource(Path("snippets") / self.filename)),
            label="Show",
        )


class Snippets:
    run_continuously_pin = FileSnippet("run_continuously_pin.js")


SNIPPETS = Snippets()


def append_snippet(snippet):
    def wrapper(f):
        def repr_html():
            return f"<div>{str(f)}</div>{snippet._repr_html_()}"

        f._repr_html_ = repr_html
        return f

    return wrapper
