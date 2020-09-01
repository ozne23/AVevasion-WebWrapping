from flask import Flask
from config import Config

UPLOAD_FOLDER = 'C:\\Users\\ozne2\\Desktop\\Tesi\\AVevasion\\Wrapper\\AVevasion\\app\\uploads'
OUTPUT_FOLDER = 'C:\\Users\\ozne2\\Desktop\\Tesi\\AVevasion\\Wrapper\\AVevasion\\app\\Output'
GCC_COMPILER_FOLDER = 'C:\\Users\\ozne2\\Desktop\\Tesi\\AVevasion\\Wrapper\\AVevasion\\app\\Compilers\\MinGW\\bin\\gcc'
GPLUSPLUS_COMPILER_FOLDER = 'C:\\Users\\ozne2\\Desktop\\Tesi\\AVevasion\\Wrapper\\AVevasion\\app\\Compilers\\MinGW\\bin\\g++'
def create_app():
    """Construct the core application."""
    app = Flask(__name__,instance_relative_config=False)
    app.config.from_object(Config)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
    app.config['GCC_COMPILER_FOLDER'] = GCC_COMPILER_FOLDER
    app.config['GPLUSPLUS_COMPILER_FOLDER'] = GPLUSPLUS_COMPILER_FOLDER

    with app.app_context():
        import routes
        # # Import main Blueprint
        app.register_blueprint(routes.main_bp)
        return app


