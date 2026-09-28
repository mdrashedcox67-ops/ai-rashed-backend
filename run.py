import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host=os.environ.get("HOST"), port=int(os.environ.get("PORT", 5000)))
