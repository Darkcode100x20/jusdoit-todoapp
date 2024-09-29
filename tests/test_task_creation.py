import pytest
from flask import url_for
from your_app import db
from your_app.models import Task

@pytest.fixture
def authenticated_user(client, user_factory):
    """Fixture to create and log in an authenticated user."""
    user = user_factory()
    client.login(user)  # Assuming you have a helper function to log in users
    return user

### 1. Test Input Validation ###
def test_create_task_input_validation(client, authenticated_user):
    """Test that invalid task data returns an error."""
    # Example of invalid input: empty title and content
    response = client.post(url_for('tasks.create_task'), data={
        'title': '',
        'content': '',
        'priority': 1
    }, follow_redirects=True)

    # Assuming flash messages for validation errors
    assert b'Title is required' in response.data
    assert b'Content is required' in response.data
    assert response.status_code == 200  # Form re-render with errors

### 2. Test Markdown Processing and Sanitization ###
def test_create_task_markdown_processing(client, authenticated_user):
    """Test that markdown input is processed and sanitized properly."""
    task_data = {
        'title': 'New Task with Markdown',
        'content': '## Heading **bold text** <script>alert("XSS")</script>',
        'priority': 2
    }

    response = client.post(url_for('tasks.create_task'), data=task_data, follow_redirects=True)

    # Check that task was created successfully
    assert b'Task created successfully' in response.data

    # Fetch the task from the database
    task = Task.query.filter_by(title='New Task with Markdown').first()

    # Verify Markdown was processed and script was sanitized
    assert task is not None
    assert '<script>' not in task.content  # Ensure script tags were sanitized
    assert '## Heading' in task.content  # Check if Markdown syntax was preserved

### 3. Test Database Interaction ###
def test_create_task_database_interaction(client, authenticated_user):
    """Test that a task is correctly added to the database upon creation."""
    task_data = {
        'title': 'Task 1',
        'content': 'Task content for testing',
        'priority': 1
    }

    response = client.post(url_for('tasks.create_task'), data=task_data, follow_redirects=True)

    # Fetch the task from the database
    task = Task.query.filter_by(title='Task 1').first()

    # Verify the task was successfully added to the database
    assert task is not None
    assert task.content == 'Task content for testing'
    assert task.priority == 1
    assert b'Task created successfully' in response.data

### 4. Test Error Handling (Database Error) ###
def test_create_task_database_error_handling(client, authenticated_user, mocker):
    """Test that an error is handled gracefully if database commit fails."""
    task_data = {
        'title': 'Task with DB Error',
        'content': 'This will cause an error',
        'priority': 2
    }

    # Mock the database session to throw an error on commit
    mocker.patch('your_app.db.session.commit', side_effect=Exception('DB Error'))

    response = client.post(url_for('tasks.create_task'), data=task_data, follow_redirects=True)

    # Ensure the task is not in the database due to the commit failure
    task = Task.query.filter_by(title='Task with DB Error').first()
    assert task is None

    # Verify error message is shown to the user
    assert b'An error occurred while creating the task' in response.data
    assert response.status_code == 200
