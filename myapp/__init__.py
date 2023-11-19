from flask import Flask, render_template
from dotenv import load_dotenv

from .extensions import db
import logging

def create_app():
    import os
    basedir = os.path.abspath(os.path.dirname(__file__))
    print(f"BASE DIR IS HERE - {basedir}")
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    logging.info("Starting up")

    load_dotenv()
    # DB_SERVER = os.getenv('DB_SERVER')
    SECRET_KEY = os.getenv('SECRET_KEY')

    app = Flask(__name__)
     
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
    # app.config['SQLALCHEMY_DATABASE_URI'] = DB_SERVER
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = SECRET_KEY

    
    db.init_app(app)

    from .home import homepage

    app.register_blueprint(homepage, url_prefix='/')

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("404.html"), 404
    
    @app.errorhandler(500)
    def page_not_found(e):
        return render_template("500.html"), 500
    
    return app