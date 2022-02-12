import sqlalchemy.exc
import typer

from app import tables
from app.app import bcrypt
from app.database import Session

app = typer.Typer()


@app.command(
    help="Create admin user for admin panel",
)
def main():
    username = typer.prompt("Enter username")
    password1 = typer.prompt("Enter password", hide_input=True)
    password2 = typer.prompt("Repeat password", hide_input=True)
    if password1 != password2:
        typer.echo("Passwords are different")
        raise typer.Abort()
    password_hash = bcrypt.generate_password_hash(password1)
    user = tables.User(username=username, password_hash=password_hash, is_admin=True)
    with Session() as session:
        session.add(user)
        try:
            session.commit()
        except sqlalchemy.exc.IntegrityError:
            typer.echo("User with such username exists!")
            raise typer.Abort()
    typer.echo("Admin user created!")


if __name__ == '__main__':
    app()
