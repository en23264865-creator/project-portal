import os
from flask import Flask, send_from_directory
from flask_cors import CORS
from config import Config
from models import db, bcrypt, jwt


def run_seed(app):
    with app.app_context():
        try:
            from models import User
            if User.query.count() > 0:
                print('✅ Database already has data — skipping seed.')
                return
            print('🌱 Empty database — seeding now...')
            import seed as seed_module
            seed_module.seed()
        except Exception as e:
            print(f'❌ Seed failed: {e}')
            import traceback
            traceback.print_exc()


def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    CORS(app)

    from routes.auth        import auth_bp
    from routes.projects    import projects_bp
    from routes.users       import users_bp
    from routes.evaluations import evaluations_bp
    from routes.progress    import progress_bp
    from routes.comments    import comments_bp
    from routes.export      import export_bp

    app.register_blueprint(auth_bp,        url_prefix='/auth')
    app.register_blueprint(projects_bp,    url_prefix='/projects')
    app.register_blueprint(users_bp,       url_prefix='/users')
    app.register_blueprint(evaluations_bp, url_prefix='/evaluations')
    app.register_blueprint(progress_bp,    url_prefix='/progress')
    app.register_blueprint(comments_bp,    url_prefix='/comments')
    app.register_blueprint(export_bp,      url_prefix='/export')

    with app.app_context():
        db.create_all()

        from models import User

        if User.query.count() == 0:
            from seed import seed
            seed()

    @app.route('/')
    def index():
        return send_from_directory('templates', 'index.html')

    return app


app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
