from flask import url_for

def test_login_page(client):
    """
    Test that the login page loads successfully (HTTP 200) and contains expected text content.
    """
    response = client.get(url_for('auth.login'))
    content = response.get_data(as_text=True)

    assert response.status_code == 200
    assert '<h2 class="auth-title">Login</h2>' in content

def test_login_page_content(client):
    """
    Verify that the login page includes required fields.
    """
    content = client.get(url_for('auth.login')).get_data(as_text=True)

    for fields in ['username','password']:
        assert fields in content