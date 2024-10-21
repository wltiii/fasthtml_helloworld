# from python_fasthtml.common import FastHTML, serve
from fasthtml.common import *

app = FastHTML()

@app.get("/")
def home():
    return "<h1>Rainbows</h1>"

serve()