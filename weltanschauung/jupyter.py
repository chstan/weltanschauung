import sys
import time
import importlib
import traceback

from typing import Any, Callable

from .snippets import SNIPPETS, append_snippet

__all__ = [
    "run_continuously",
]

def format_traceback(exc: Exception) -> str:
    return "".join(traceback.format_exception(exc.__class__, exc, exc.__traceback__))

@append_snippet(SNIPPETS.run_continuously_pin)
def run_continuously(inner_function: Callable[[], Any], interval=0.25):
    """
    Thin utility for Jupyter which allows continuously executing a funtion in a cell
    to allow for iterative development in a real editor.

    There are caveats here. We need to reload modules potentially, so we
    allow passing this through `reload`.

    Additionally, you almost certainly want to dock the output of the Jupyter cell
    and run a Javascript snippet which will keep the scroll of the output pinned at the bottom.
    """
    print(f"rel snippet: \n{SNIPPETS.run_continuously_pin}")

    if "lambda" in inner_function.__name__:
        print("Was passed lambda. Reloading the module should happen inside this lambda as a result.")
    elif inner_function.__module__ == "__main__":
        print("Was passed cell-defined function. Reloading the module should happen inside this function as a result.")
    else:
        parent_module_name = inner_function.__module__
        function_name = inner_function.__name__
        
        def wrapped_inner_function():
            module = importlib.reload(sys.modules[parent_module_name])
            f = getattr(module, function_name)
            return f()
        
        inner_function = wrapped_inner_function


    print_last = ""

    while True:
        try:
            print_next = str(inner_function())
        except Exception as e:
            print_next = format_traceback(e)

        if print_next != print_last:
            print(print_next)

        print_last = print_next
        time.sleep(interval)
