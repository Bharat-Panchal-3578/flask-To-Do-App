from flask import url_for

def test_tasks_page(client):
    """
    Test that the tasks page loads successsfully (HTTP 200).
    """
    response = client.get(url_for('dashboard.dashboard'))
    assert response.status_code == 200

def test_tasks_page_content(client):
    """
    Test for tasks or dashboard page content.
    """
    content = client.get(url_for('dashboard.dashboard')).get_data(as_text=True)

    assert "My Tasks" in content
    assert "Add Task" in content