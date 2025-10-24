from flask import url_for

def test_register_page(client):
    """GET /register should return 200 and contain registration form text."""
    response = client.get(url_for('auth.register'))
    content = response.get_data(as_text=True)

    assert response.status_code == 200
    assert "Create an Account" in content

def test_register_page_fields(client):
    """Check important input fields exists."""
    content = client.get(url_for('auth.register')).get_data(as_text=True)

    for fields in ['username','password','confirm-password']:
        assert fields in content