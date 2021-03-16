import connexion  # type: ignore
from flask_cors import CORS  # type: ignore

connexion_app = connexion.FlaskApp('Validator Service', specification_dir='doc/')
app = connexion_app.app


@app.errorhandler(Exception)
def handle_validation_error(ex: Exception):
    return {
        'valid': None,
        'message': str(ex),
    }, 500


connexion_app.add_api('openapi.yaml')

CORS(app)
