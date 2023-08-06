#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import typer
import pywebcanvas as pwc


main = typer.Typer()


@main.command()
def new(name: str = "pywebcanvas-project"):
    typer.echo(f"Creating project {name}...")
    template = """ 
<!doctype html>
<html>
   <head> 
        <title>{name}</title>
        <script src="https://cdn.jsdelivr.net/pyodide/v0.20.0/full/pyodide.js"></script>
        <script type="text/javascript">
        async function pywebcanvas(){
            let pyodide = await loadPyodide();
            await pyodide.loadPackage("micropip");
            pyodide.runPythonAsync(`
                import  micropip, js, asyncio
                await micropip.install("pywebcanvas=={pwc.__version__}")
                import pywebcanvas as pwc
                # Your Code Here:
                canvas = pwc.Canvas(800, 600)
                canvas.background.fill("blue")
                text = pwc.Text(text="Hello World from pywebcanvas!", x=100, y=100, size=25, color="yellow")
                canvas.render(text)
            `);
        }
        pywebcanvas();
        </script>
   </head>
   <body>
   </body>
</html>
""".replace("{name}", name).replace("{pwc.__version__}", pwc.__version__)
    os.mkdir(f"./{name}")
    with open(f"./{name}/index.html", "w") as f:
        f.write(template)
    typer.echo(f"New pywebcanvas project created at './{name}'!")


if __name__ == '__main__':
    main()
