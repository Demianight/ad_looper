import argparse
import subprocess
from pathlib import Path

import uvicorn


def start():
    uvicorn.run("ad_looper.main:app", host="127.0.0.1", port=8000, reload=True)


def startapp():
    parser = argparse.ArgumentParser(description="Create a new FastAPI app.")
    parser.add_argument(
        "app_name", type=str, help="The name of the app to create"
    )
    args = parser.parse_args()

    app_name = args.app_name
    apps_path = Path("apps")
    path = apps_path / Path(app_name)
    path.mkdir()

    init_path = path / "__init__.py"
    init_path.touch()
    with open(init_path, "w") as f:
        f.write(
            "from .routers import router as router\n\n\n__all__ = ['router']\n"
        )

    routers_path = path / "routers.py"
    routers_path.touch()
    with open(routers_path, "w") as f:
        f.write("from fastapi import APIRouter\n\nrouter = APIRouter()\n")

    schemas_path = path / "schemas.py"
    schemas_path.touch()
    with open(schemas_path, "w") as f:
        f.write("from pydantic import BaseModel\n")

    crud_path = path / "crud.py"
    crud_path.touch()
    with open(crud_path, "w") as f:
        f.write(
            "from fastapi import HTTPException\nfrom sqlalchemy.ext.asyncio import AsyncSession\n"
        )

    with open(apps_path / "__init__.py", "a") as f:
        f.write(
            f"from . import {app_name}\ncore_router.include_router({app_name}.router)\n"
        )

    print(f"App {app_name} created")


def isort():
    subprocess.run(["isort", "."], check=True)
    print("Formatted imports")


def tests():
    subprocess.run(["pytest"], check=True)
    print("Tests passed")


def pre_commit():
    isort()
    tests()


def makemigrations():
    parser = argparse.ArgumentParser(description="Create a new FastAPI app.")
    parser.add_argument("message", type=str, help="Migration message")
    args = parser.parse_args()

    message = args.message
    subprocess.run(
        ["alembic", "revision", "--autogenerate", "-m", message],
        check=True,
    )
    print(f"Migration created: {message}")


def migrate():
    subprocess.run(["alembic", "upgrade", "head"], check=True)
    print("Migration applied")
