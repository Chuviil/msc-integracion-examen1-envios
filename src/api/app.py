import json
from pathlib import Path

from apiflask import APIFlask, abort

from schemas.envios import EnvioIn

app = APIFlask(__name__)

DATA_PATH = (Path(__file__).resolve().parent / ".." / "data" / "envios.json").resolve()


def _load_envios():
    with DATA_PATH.open(encoding="utf-8") as json_file:
        return json.load(json_file)


def _save_envios(envios):
    with DATA_PATH.open("w", encoding="utf-8") as json_file:
        json.dump(envios, json_file, ensure_ascii=False, indent=4)


@app.get("/envios")
def get_envios():
    return _load_envios()


@app.get("/envios/<string:envio_id>")
def get_envio_by_id(envio_id):
    for envio in _load_envios():
        if envio.get("id_envio") == envio_id:
            return envio
    abort(404, message="Envio not found")


@app.post("/envios")
@app.input(EnvioIn)
def create_envio(json_data):
    envios = _load_envios()

    for envio in envios:
        if envio.get("id_envio") == json_data["id_envio"]:
            abort(409, message="Envio already exists")

    envios.append(json_data)
    _save_envios(envios)

    return json_data, 201
