from app.database import Session
from app.settings import settings
from .app import create_app

with Session() as session:
    app = create_app(session)
    app.run(
        host=settings.admin_app_host,
        port=settings.admin_app_port,
        debug=settings.debug,
    )
