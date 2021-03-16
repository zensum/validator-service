import os

from app import app


if __name__ == '__main__':
    port = os.getenv('PORT', '80')
    host = '0.0.0.0'
    app.run(port=int(port), host=host)
