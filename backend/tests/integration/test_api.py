"""Integration tests for API endpoints."""

import pytest
from fastapi.testclient import TestClient


class TestCreateTaskEndpoint:
    """Integration tests for POST /tasks."""

    def test_create_task_basic(self, client: TestClient):
        """Test creating a task with just a title."""
        response = client.post("/api/v1/tasks", json={"title": "Test task"})
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Test task"
        assert data["completed"] is False
        assert data["priority"] == "medium"
        assert data["tags"] == []
        assert "id" in data

    def test_create_task_with_priority(self, client: TestClient):
        """Test creating a task with priority."""
        response = client.post(
            "/api/v1/tasks",
            json={"title": "High priority", "priority": "high"},
        )
        assert response.status_code == 201
        assert response.json()["priority"] == "high"

    def test_create_task_with_tags(self, client: TestClient):
        """Test creating a task with tags."""
        response = client.post(
            "/api/v1/tasks",
            json={"title": "Tagged task", "tags": ["work", "urgent"]},
        )
        assert response.status_code == 201
        assert response.json()["tags"] == ["work", "urgent"]

    def test_create_task_empty_title_fails(self, client: TestClient):
        """Test that empty title is rejected."""
        response = client.post("/api/v1/tasks", json={"title": ""})
        assert response.status_code == 422  # Validation error

    def test_create_task_invalid_priority_fails(self, client: TestClient):
        """Test that invalid priority is rejected."""
        response = client.post(
            "/api/v1/tasks",
            json={"title": "Test", "priority": "urgent"},
        )
        assert response.status_code == 422


class TestListTasksEndpoint:
    """Integration tests for GET /tasks."""

    def test_list_tasks_empty(self, client: TestClient):
        """Test listing when no tasks exist."""
        response = client.get("/api/v1/tasks")
        assert response.status_code == 200
        assert response.json() == []

    def test_list_tasks_returns_all(self, client: TestClient):
        """Test listing returns all tasks."""
        client.post("/api/v1/tasks", json={"title": "Task 1"})
        client.post("/api/v1/tasks", json={"title": "Task 2"})

        response = client.get("/api/v1/tasks")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

    def test_list_tasks_search(self, client: TestClient):
        """Test search parameter."""
        client.post("/api/v1/tasks", json={"title": "Buy groceries"})
        client.post("/api/v1/tasks", json={"title": "Call mom"})

        response = client.get("/api/v1/tasks?search=groceries")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert "groceries" in data[0]["title"]

    def test_list_tasks_filter_status(self, client: TestClient):
        """Test status filter."""
        # Create and complete one task
        response = client.post("/api/v1/tasks", json={"title": "Task 1"})
        task_id = response.json()["id"]
        client.patch(f"/api/v1/tasks/{task_id}/complete")

        client.post("/api/v1/tasks", json={"title": "Task 2"})

        # Filter by incomplete
        response = client.get("/api/v1/tasks?status=incomplete")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["completed"] is False

    def test_list_tasks_filter_priority(self, client: TestClient):
        """Test priority filter."""
        client.post("/api/v1/tasks", json={"title": "High", "priority": "high"})
        client.post("/api/v1/tasks", json={"title": "Low", "priority": "low"})

        response = client.get("/api/v1/tasks?priority=high")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["priority"] == "high"

    def test_list_tasks_filter_tag(self, client: TestClient):
        """Test tag filter."""
        client.post("/api/v1/tasks", json={"title": "Work", "tags": ["work"]})
        client.post("/api/v1/tasks", json={"title": "Home", "tags": ["home"]})

        response = client.get("/api/v1/tasks?tag=work")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert "work" in data[0]["tags"]

    def test_list_tasks_sort_priority(self, client: TestClient):
        """Test sort by priority."""
        client.post("/api/v1/tasks", json={"title": "Low", "priority": "low"})
        client.post("/api/v1/tasks", json={"title": "High", "priority": "high"})

        response = client.get("/api/v1/tasks?sort=priority")
        assert response.status_code == 200
        data = response.json()
        assert data[0]["priority"] == "high"
        assert data[1]["priority"] == "low"

    def test_list_tasks_sort_alpha(self, client: TestClient):
        """Test sort alphabetically."""
        client.post("/api/v1/tasks", json={"title": "Zebra"})
        client.post("/api/v1/tasks", json={"title": "Apple"})

        response = client.get("/api/v1/tasks?sort=alpha")
        assert response.status_code == 200
        data = response.json()
        assert data[0]["title"] == "Apple"
        assert data[1]["title"] == "Zebra"


class TestGetTaskEndpoint:
    """Integration tests for GET /tasks/{id}."""

    def test_get_task_exists(self, client: TestClient):
        """Test getting an existing task."""
        response = client.post("/api/v1/tasks", json={"title": "Test task"})
        task_id = response.json()["id"]

        response = client.get(f"/api/v1/tasks/{task_id}")
        assert response.status_code == 200
        assert response.json()["title"] == "Test task"

    def test_get_task_not_found(self, client: TestClient):
        """Test getting a non-existent task."""
        response = client.get("/api/v1/tasks/999")
        assert response.status_code == 404


class TestUpdateTaskEndpoint:
    """Integration tests for PUT /tasks/{id}."""

    def test_update_task_title(self, client: TestClient):
        """Test updating task title."""
        response = client.post("/api/v1/tasks", json={"title": "Original"})
        task_id = response.json()["id"]

        response = client.put(
            f"/api/v1/tasks/{task_id}",
            json={"title": "Updated"},
        )
        assert response.status_code == 200
        assert response.json()["title"] == "Updated"

    def test_update_task_priority(self, client: TestClient):
        """Test updating task priority."""
        response = client.post("/api/v1/tasks", json={"title": "Test"})
        task_id = response.json()["id"]

        response = client.put(
            f"/api/v1/tasks/{task_id}",
            json={"priority": "high"},
        )
        assert response.status_code == 200
        assert response.json()["priority"] == "high"

    def test_update_task_not_found(self, client: TestClient):
        """Test updating a non-existent task."""
        response = client.put("/api/v1/tasks/999", json={"title": "Test"})
        assert response.status_code == 404

    def test_update_task_no_changes(self, client: TestClient):
        """Test update with no changes fails."""
        response = client.post("/api/v1/tasks", json={"title": "Test"})
        task_id = response.json()["id"]

        response = client.put(f"/api/v1/tasks/{task_id}", json={})
        assert response.status_code == 400


class TestDeleteTaskEndpoint:
    """Integration tests for DELETE /tasks/{id}."""

    def test_delete_task_exists(self, client: TestClient):
        """Test deleting an existing task."""
        response = client.post("/api/v1/tasks", json={"title": "To delete"})
        task_id = response.json()["id"]

        response = client.delete(f"/api/v1/tasks/{task_id}")
        assert response.status_code == 204

        # Verify deleted
        response = client.get(f"/api/v1/tasks/{task_id}")
        assert response.status_code == 404

    def test_delete_task_not_found(self, client: TestClient):
        """Test deleting a non-existent task."""
        response = client.delete("/api/v1/tasks/999")
        assert response.status_code == 404


class TestToggleCompleteEndpoint:
    """Integration tests for PATCH /tasks/{id}/complete."""

    def test_toggle_complete(self, client: TestClient):
        """Test toggling completion status."""
        response = client.post("/api/v1/tasks", json={"title": "Test"})
        task_id = response.json()["id"]
        assert response.json()["completed"] is False

        response = client.patch(f"/api/v1/tasks/{task_id}/complete")
        assert response.status_code == 200
        assert response.json()["completed"] is True

    def test_toggle_complete_back(self, client: TestClient):
        """Test toggling back to incomplete."""
        response = client.post("/api/v1/tasks", json={"title": "Test"})
        task_id = response.json()["id"]

        client.patch(f"/api/v1/tasks/{task_id}/complete")  # Complete
        response = client.patch(f"/api/v1/tasks/{task_id}/complete")  # Uncomplete
        assert response.status_code == 200
        assert response.json()["completed"] is False

    def test_toggle_complete_not_found(self, client: TestClient):
        """Test toggling non-existent task."""
        response = client.patch("/api/v1/tasks/999/complete")
        assert response.status_code == 404


class TestAddTagEndpoint:
    """Integration tests for POST /tasks/{id}/tags."""

    def test_add_tag(self, client: TestClient):
        """Test adding a tag."""
        response = client.post("/api/v1/tasks", json={"title": "Test"})
        task_id = response.json()["id"]

        response = client.post(
            f"/api/v1/tasks/{task_id}/tags",
            json={"tag": "work"},
        )
        assert response.status_code == 200
        assert "work" in response.json()["tags"]

    def test_add_tag_not_found(self, client: TestClient):
        """Test adding tag to non-existent task."""
        response = client.post("/api/v1/tasks/999/tags", json={"tag": "work"})
        assert response.status_code == 404


class TestRemoveTagEndpoint:
    """Integration tests for DELETE /tasks/{id}/tags/{tag}."""

    def test_remove_tag(self, client: TestClient):
        """Test removing a tag."""
        response = client.post(
            "/api/v1/tasks",
            json={"title": "Test", "tags": ["work", "home"]},
        )
        task_id = response.json()["id"]

        response = client.delete(f"/api/v1/tasks/{task_id}/tags/work")
        assert response.status_code == 200
        assert "work" not in response.json()["tags"]
        assert "home" in response.json()["tags"]

    def test_remove_tag_not_found(self, client: TestClient):
        """Test removing tag from non-existent task."""
        response = client.delete("/api/v1/tasks/999/tags/work")
        assert response.status_code == 404


class TestHealthEndpoint:
    """Integration tests for GET /health."""

    def test_health_check(self, client: TestClient):
        """Test health check returns healthy status."""
        response = client.get("/api/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
