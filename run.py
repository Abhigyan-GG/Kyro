"""
Kyro — Application Entry Point

Usage:
    python run.py
"""

from app.factory import create_app
from app.core.config import settings

app = create_app()

if __name__ == "__main__":
    app.run(
        host=settings.flask.HOST,
        port=settings.flask.PORT,
        debug=settings.flask.DEBUG,
    )
