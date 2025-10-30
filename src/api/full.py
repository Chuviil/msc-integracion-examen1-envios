"""Waitress entry point that ensures envios data is available."""

import importlib.util
import logging
import os
import subprocess
from pathlib import Path

from waitress import serve

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATA_PATH = (Path(__file__).resolve().parent / ".." / "data" / "envios.json").resolve()
FILE_TRANSFER_DIR = (Path(__file__).resolve().parent / ".." / "file-transfer").resolve()
FILE_TRANSFER_JAR = FILE_TRANSFER_DIR / "file-transfer.jar"


def _ensure_data_file() -> None:
    """Guarantee the JSON data file exists by invoking the Java transformer if needed."""

    if DATA_PATH.exists():
        logger.info("Data file already present at %s; skipping file-transfer step", DATA_PATH)
        return

    if not FILE_TRANSFER_JAR.exists():
        logger.error("Missing transformer jar at %s", FILE_TRANSFER_JAR)
        raise SystemExit(1)

    logger.info("Generating %s using %s", DATA_PATH, FILE_TRANSFER_JAR)

    try:
        process = subprocess.Popen(
            ["java", "-jar", str(FILE_TRANSFER_JAR)],
            cwd=str(FILE_TRANSFER_DIR),
        )
    except FileNotFoundError as exc:
        logger.error("Java runtime not found: %s", exc)
        raise SystemExit(1) from exc

    try:
        process.wait(timeout=10)
    except subprocess.TimeoutExpired:
        logger.info("Transformer still running after 10 seconds; terminating it")
    finally:
        if process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                logger.warning("Force killing transformer process")
                process.kill()
                process.wait()

    if DATA_PATH.exists():
        logger.info("Data file created at %s", DATA_PATH)
        return

    logger.error("Data file %s still missing after running transformer", DATA_PATH)
    raise SystemExit(1)


def _import_app():
    """Import the Flask application regardless of package execution context."""

    try:
        from .app import app as imported_app
        return imported_app
    except ImportError:
        app_path = Path(__file__).resolve().parent / "app.py"
        spec = importlib.util.spec_from_file_location("api.app", app_path)
        if spec is None or spec.loader is None:
            logger.error("Unable to locate api.app module at %s", app_path)
            raise SystemExit(1)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module.app


_ensure_data_file()
app = _import_app()


if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "5000"))
    serve(app, host=host, port=port)
