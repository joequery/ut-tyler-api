from flask import Flask
import v1.api
import os

# App configuration
app = Flask(__name__)
app.register_blueprint(v1.api.v1)

# FLASK_ENV environment variable can be 'development' or 'production'
if "FLASK_ENV" in os.environ.keys():
    FLASK_ENV = os.environ["FLASK_ENV"]
    if FLASK_ENV == "production":
        app.debug = False
else:
    FLASK_ENV = "development"
    app.debug = True

if __name__ == "__main__":
  if FLASK_ENV == "production":
      app.run()
  else:
      app.run(host="0.0.0.0")
