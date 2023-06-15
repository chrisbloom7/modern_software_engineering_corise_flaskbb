import pytest
from playwright.sync_api import Page
from flask import url_for
from flaskbb import create_app
from flaskbb.configs.testing import TestingConfig as Config
from flaskbb.extensions import db
from flaskbb.utils.populate import create_default_groups, create_default_settings
from flaskbb.utils.translations import compile_translations

@pytest.fixture(scope="session")
def app():
    # Hint: create the app, and setup any default context like translations,
    # settings, DB, etc.
    # Hint: take a look at the tests/fixtures/app.py file for the details of
    # how to configure the application.
    application = create_app(Config)

    with application.app_context():
        db.create_all()
        create_default_groups()
        create_default_settings()
        compile_translations()

    return application

def test_load_home_page(live_server, page: Page):
    # Hint: Check out `flask.url_for` helper function to get the external url for
    # an endpoint. Then go to it using playwright's `page.goto(url)`
    url = url_for('forum.index', _external=True)
    response = page.goto(url)
    assert response.status == 200

###################################################################
