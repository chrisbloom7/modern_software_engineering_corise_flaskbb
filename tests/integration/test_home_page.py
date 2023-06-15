import pytest

# pytestmark = pytest.mark.usefixtures("application")

###################################################################
# CoRise TODO: add an integration test that uses the test client to
# load the home page ('/'). Make sure the response code is 200 and
# that the response data contains something you expect to see on the
# home page.
#
# Hint: you can get the test client by calling `application.test_client()`
# when using the application test fixture.

class TestHomePage(object):
    def test_get_index(self, application, default_settings, default_groups, default_translations):
        with application.test_client() as client:
            client = application.test_client()
            response = client.get('/')
            assert b"A lightweight forum software in Flask" in response.data

###################################################################
