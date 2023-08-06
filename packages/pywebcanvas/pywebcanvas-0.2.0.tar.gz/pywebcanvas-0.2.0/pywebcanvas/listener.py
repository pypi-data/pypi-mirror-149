import js
import pyodide
from typing import Callable
import pywebcanvas as pwc

def add_event_handler(event: str, handler: Callable):
    pwc.log(f"Add event handler {handler} for event {event}")
    proxy = pyodide.create_proxy(handler)
    js.document.addEventListener(event, proxy)
