from .app import create_app
from .settings import settings

app = create_app()

app.run(
    host=settings.app_host,
    port=settings.app_port,
    debug=settings.debug,
)
