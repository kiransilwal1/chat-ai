import os
import typer
from sqlalchemy.orm import Session
from models import SessionLocal, ChatPath
from sqlalchemy import exc

app = typer.Typer()


@app.command()
def add_path():
    """Add the current path to the database if it doesn't exist"""
    current_path = os.getcwd()

    session = SessionLocal()

    try:
        session.add(ChatPath(path=current_path))
        session.commit()
        typer.echo(f"Path {current_path} added successfully!")
    except exc.IntegrityError:
        typer.echo(f"Path {current_path} already exists in the database.")
    finally:
        session.close()


@app.command()
def list_path():
    """List all paths"""
    session: Session = SessionLocal()
    paths = session.query(ChatPath).all()
    for path in paths:
        typer.echo(f"{path.id}: {path.path}")


if __name__ == "__main__":
    app()
