import os
import pytest

from flask_skeleton.rest_api import (create_app,
 TEST_FLAG_EV, TEST_ENDPOINTS_MODULE_EV)


@pytest.fixture
def client(test_config):
    """Test client for REST API"""
    os.environ[TEST_FLAG_EV] = "True"
    os.environ[TEST_ENDPOINTS_MODULE_EV] = 'flask_skeleton.rest_api.endpoints_1'
    # NOTE: Must set above env vars first so that when app
    # is created it pulls those values and app is created in test mode
    app = create_app()
    app.config["config"] = test_config
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


class Test_REST_API_Endpoints_1:
    """ """
    def test_index(self, client):
        """Tests rest_api.endpoints_1.index()"""
        r = client.get("/")
        assert "Redirecting..." in str(r.data)
        assert r.status_code == 302
    
    def test_endpoint_0(self, client):
        """ """
        assert 0
    
    def test_endpoint_1(self, client):
        """ """
        assert 0

    def test_endpoint_3(self, client):
        """ """
        assert 0

    # More tests
    #     .
    #     .
    #     .