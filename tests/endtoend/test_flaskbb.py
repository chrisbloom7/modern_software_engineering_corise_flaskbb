import pytest
from playwright.sync_api import Page
from flask import url_for
from flaskbb import create_app
from flaskbb.configs.testing import TestingConfig as Config
from flaskbb.extensions import db
from flaskbb.utils.populate import create_default_groups, create_default_settings, create_user, create_welcome_forum
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
        create_user("test", "test", "test@example.org", "member")
        create_welcome_forum()

    return application

def test_load_home_page(live_server, page: Page):
    # Hint: Check out `flask.url_for` helper function to get the external url for
    # an endpoint. Then go to it using playwright's `page.goto(url)`
    url = url_for('forum.index', _external=True)
    page.goto(url)
    assert "FlaskBB - A lightweight forum software in Flask" == page.title()

def test_create_post(live_server, page: Page):
    url = url_for('auth.login', _external=True)
    page.goto(url)
    assert "Login" in page.title()

    page.get_by_label("Username or Email address").fill("test")
    page.get_by_label("Password").fill("test")
    page.get_by_role("button", name="Login").click()
    assert not "Wrong username or password" in page.content()

    page.screenshot(path="welcome.jpeg")
    page.get_by_role("link", name="Welcome", exact=True).click()
    assert "Welcome" in page.title()

    page.screenshot(path="new_topic.jpeg")
    page.get_by_role("link", name="New Topic").click()
    assert "New Topic" in page.title()

    page.get_by_label("Topic title").fill("My Topic")
    page.get_by_label("Content").fill("Hi!")
    page.get_by_role("button", name="Post Topic").click()
    assert "My Topic" in page.title()

###################################################################
