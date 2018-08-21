from flask import Flask

"""Create the flask app"""
app = Flask(__name__)
app.config["TESTING"] = True
app.url_map.strict_slashes = False
app.config['JWT_SECRET_KEY'] = 'my-key'
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access']
