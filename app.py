from flask import Flask, session
from views import register_routes
from datetime import timedelta

app = Flask(__name__)
app.permanent_session_lifetime = timedelta(minutes=20)
app.config.from_object('configuration.DevConfig')

register_routes(app)

if __name__ == '__main__':
    app.run()
