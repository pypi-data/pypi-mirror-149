logging = True

def log(message: str):
    global logging
    if logging:
        print(f"pywebcanvas: {message}")

def disable_logging(disable: bool):
    global logging 
    logging = not disable
    log(f"{logging=}")
