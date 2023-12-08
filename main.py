import config
from flask import Flask
from flask_migrate import Migrate
from models import db
from auth_app import auth as auth_blueprint
from main_app import main as main_blueprint
# init SQLAlchemy so we can use it later in our models

app = Flask(__name__)
app.config.update(
    SECRET_KEY="33e08edb07e6fa05800d8fc2188d76d5",
    SQLALCHEMY_DATABASE_URI=config.SQLA_DB_URI,
)
db.init_app(app)
migrate = Migrate(app, db=db)

app.register_blueprint(auth_blueprint)

app.register_blueprint(main_blueprint)



if __name__ == "__main__":
    app.run(debug=True)