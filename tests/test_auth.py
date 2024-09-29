def test_delete_task_authorization(client, authenticated_user, another_user):
    """Test that only the owner of the task can delete it."""
    # Create a task by the authenticated user
    task = Task(title="Task to delete", content="Content", user_id=authenticated_user.id)
    db.session.add(task)
    db.session.commit()

    # Try to delete it as another user (not the task owner)
    client.login(another_user)  # Assuming there's a helper to log in users
    response = client.post(url_for('tasks.delete_task', task_id=task.id), follow_redirects=True)

    # Ensure that deletion is unauthorized
    assert response.status_code == 403  # Or another appropriate status code
    assert Task.query.filter_by(id=task.id).first() is not None  # Task still exists
