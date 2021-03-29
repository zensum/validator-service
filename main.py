import os

from app import app


if __name__ == '__main__':
    import debugpy  # type: ignore
    debugpy.listen(('0.0.0.0', 10001))
    print('⏳ VS Code debugger can now be attached, press F5 in VS Code ⏳', flush=True)
    debugpy.wait_for_client()
    print('🎉 VS Code debugger attached, enjoy debugging 🎉', flush=True)
    port = os.getenv('PORT', '80')
    host = '0.0.0.0'
    app.run(port=int(port), host=host)
