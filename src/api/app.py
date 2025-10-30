import json
import logging
import os
from pathlib import Path

from apiflask import APIFlask, abort
from waitress import serve

from schemas.envios import EnvioIn

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = APIFlask(__name__)

DATA_PATH = (Path(__file__).resolve().parent / ".." / "data" / "envios.json").resolve()

if not DATA_PATH.exists():
    logger.error(
        "Data file missing at %s. Run the CSV transformation from src/file-transfer first.",
        DATA_PATH,
    )
    raise SystemExit(1)


def _load_envios():
    with DATA_PATH.open(encoding="utf-8") as json_file:
        return json.load(json_file)


def _save_envios(envios):
    with DATA_PATH.open("w", encoding="utf-8") as json_file:
        json.dump(envios, json_file, ensure_ascii=False, indent=4)


@app.get("/envios")
def get_envios():
    envios = _load_envios()
    logger.info("Fetched %d envios", len(envios))
    return envios


@app.get("/envios/<string:envio_id>")
def get_envio_by_id(envio_id):
    for envio in _load_envios():
        if envio.get("id_envio") == envio_id:
            logger.info("Envio %s found", envio_id)
            return envio
    logger.warning("Envio %s not found", envio_id)
    abort(404, message="Envio not found")


@app.post("/envios")
@app.input(EnvioIn)
def create_envio(json_data):
    envios = _load_envios()

    for envio in envios:
        if envio.get("id_envio") == json_data["id_envio"]:
            logger.warning("Envio %s already exists", json_data["id_envio"])
            abort(409, message="Envio already exists")

    envios.append(json_data)
    _save_envios(envios)
    logger.info("Envio %s created", json_data["id_envio"])

    return json_data, 201


if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "5000"))
    serve(app, host=host, port=port)
