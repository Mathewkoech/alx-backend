#!/usr/bin/env python3
"""A Basic Flask app.
"""
import pytz
from flask_babel import Babel
from flask import Flask, render_template, request, g
from typing import Union, Dict


users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


class Config:
    """Represents a Flask Babel configuration.
    """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
app.url_map.strict_slashes = False
babel = Babel(app)


@babel.localeselector
def get_locale() -> str:
    """Retrieves the locale for a web page.
    """
    " locale from URL parameters"
    locale = request.args.get('locale')
    if locale in app.config['LANGUAGES']:
        return locale

    " locale from user settings"
    if g.user and g.user['locale'] in app.config['LANGUAGES']:
        return g.user['locale']

    " locale from request headers"
    header_locale = request.headers.get('locale', '')
    if header_locale in app.config['LANGUAGES']:
        return header_locale

    " default locale"
    return request.accept_languages.best_match(app.config["LANGUAGES"])


def get_user() -> Union[Dict, None]:
    """ Retrieves the user dict if found otherwise None
    """
    user_id = request.args.get('login_as')
    if user_id:
        return users.get(int(user_id))
    return None


@app.before_request
def before_request():
    """ finds a user and is run before all other function
    """
    user = get_user()
    g.user = user


@babel.timezoneselector
def get_timezone():
    """ Infers appropriate time zone
    """

    " timezone from url parameters"
    timezone = request.args.get("timezone", '').strip()
    if not timezone and g.user:
        timezone = g.user['timezone']
    try:
        return pytz.timezone(timezone).zone
    except pytz.exceptions.UnknownTimeZoneError:
        return app.config['BABEL_DEFAULT_TIMEZONE']


@app.route('/')
def get_index() -> str:
    """The home page.
    """
    return render_template('7-index.html')


""" make get_locale available in jinja templates
"""
app.jinja_env.globals['get_locale'] = get_locale


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
