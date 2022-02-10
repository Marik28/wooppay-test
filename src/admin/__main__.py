from app.database import Session
from .app import create_app

with Session() as session:
    app = create_app(session)
    app.run()
