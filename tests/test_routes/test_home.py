import pytest
from flask import url_for

def test_home_page(client):
    """
    Test the home page route.
    Check if the status code is 200 and page content is correct.
    """
    response = client.get(url_for('home.home'))

    assert response.status_code == 200

def test_home_page_content(client):
    """
    Test the home page content.
    Check if the response data contains some home page content by testing some text from home page"
    """
    response = client.get(url_for('home.home'))
    content = response.get_data(as_text=True)

    assert "Welcome to Task Manager" in content
    assert "Get Started" in content
    assert "Login" in content