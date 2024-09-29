import pytest
from flask import url_for
from your_app import db
from your_app.models import Task

@pytest.fixture
def task(authenticated_user):
    """Fixture to create a task for the authenticated user."""
    task = Task(title="Initial Task", content="Initial Content", priority=1, user_id=authenticated_user.id)
    db.session.add(task)
    db.session.commit()
    return task

### 1. Test Content and Priority Updates ###
def test_update_task_content_and_priority(client, authenticated_user, task):
    """Test that the task's content and priority can be updated."""
    response = client.post(url_for('tasks.update_task', task_id=task.id), data={
        'title': 'Updated Task',
        'content': 'Updated Content',
        'priority': 2
    }, follow_redirects=True)

    # Fetch the updated task from the database
    updated_task = Task.query.get(task.id)

    # Verify the task was updated
    assert updated_task.title == 'Updated Task'
    assert updated_task.content == 'Updated Content'
    assert updated_task.priority == 2
    assert b'Task updated successfully' in response.data

### 2. Test Markdown Processing and Sanitization ###
def test_update_task_markdown_processing(client, authenticated_user, task):
    """Test that Markdown is processed and sanitized on task updates."""
    response = client.post(url_for('tasks.update_task', task_id=task.id), data={
        'content': '## Heading **bold text** <script>alert("XSS")</script>'
    }, follow_redirects=True)

    updated_task = Task.query.get(task.id)

    # Verify that Markdown was preserved but the script tag was sanitized
    assert '<script>' not in updated_task.content  # Sanitization check
    assert '## Heading' in updated_task.content  # Markdown syntax is preserved

### 3. Test Timestamp Update Verification ###
def test_update_task_timestamp(client, authenticated_user, task):
    """Test that the task's updated_at timestamp is updated when the task is modified."""
    old_timestamp = task.updated_at

    # Update the task
    response = client.post(url_for('tasks.update_task', task_id=task.id), data={
        'content': 'Updated Content'
    }, follow_redirects=True)

    updated_task = Task.query.get(task.id)

    # Verify that the timestamp was updated
    assert updated_task.updated_at > old_timestamp

### 4. Test Error Handling for Invalid Inputs ###
def test_update_task_invalid_input(client, authenticated_user, task):
    """Test that invalid input, such as an empty title, returns appropriate errors."""
    response = client.post(url_for('tasks.update_task', task_id=task.id), data={
        'title': '',  # Invalid title (empty)
        'content': 'Updated Content'
    }, follow_redirects=True)

    # Verify that an error message is shown and the task is not updated
    assert b'Title is required' in response.data  # Assuming your form validation returns this message
    assert response.status_code == 200  # The request should complete successfully but with an error

### 5. Test Unauthorized Access to Update ###
def test_update_task_unauthorized_access(client, another_user, task):
    """Test that a user who is not the task owner cannot update the task."""
    # Try to update the task as another user (who is not the owner)
    client.login(another_user)  # Assuming you have a helper to log in as another user
    response = client.post(url_for('tasks.update_task', task_id=task.id), data={
        'title': 'New Title',
        'content': 'New Content'
    }, follow_redirects=True)

    # Ensure the user receives a forbidden response
    assert response.status_code == 403  # Forbidden status code
    assert Task.query.get(task.id).title == 'Initial Task'  # Task should remain unchanged
