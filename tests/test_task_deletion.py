import pytest
from flask import url_for
from your_app import db
from your_app.models import Task

@pytest.fixture
def task(authenticated_user):
    task = Task(title="Task to delete", content="Content", user_id=authenticated_user.id)
    db.session.add(task)
    db.session.commit()
    return task

def test_delete_task_authorization(client, authenticated_user, another_user, task):
    """Test that only the owner of the task can delete it."""
    # Attempt deletion as another user
    client.login(another_user)
    response = client.post(url_for('tasks.delete_task', task_id=task.id), follow_redirects=True)
    assert response.status_code == 403
    assert Task.query.get(task.id) is not None

def test_delete_task_removal(client, authenticated_user, task):
    """Test that a task is correctly removed from the database upon deletion."""
    response = client.post(url_for('tasks.delete_task', task_id=task.id), follow_redirects=True)
    assert Task.query.get(task.id) is None
    assert b'Task deleted successfully' in response.data

def test_delete_task_not_found(client, authenticated_user):
    """Test that attempting to delete a non-existent task returns an error."""
    response = client.post(url_for('tasks.delete_task', task_id=9999), follow_redirects=True)
    assert response.status_code == 404
    assert b'Task not found' in response.data
