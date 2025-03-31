from flask import Flask
import webbrowser

# Routes
from routes.index import app_routes

app = Flask(__name__)

# Register the blueprint
app.register_blueprint(app_routes, url_prefix='/')


def main():
    # Opens the tool in browser
    webbrowser.open("http://localhost:5001")
    # Creating Web Server
    app.run(debug=True, port=5001)


if __name__ == '__main__':
    main()
