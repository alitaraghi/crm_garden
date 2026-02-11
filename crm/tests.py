from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Client, Project, Task


User = get_user_model()


class BaseCRMTestCase(TestCase):
    """Base test case that sets up two users and some shared data."""

    def setUp(self):
        # Two users to test ownership/permissions
        self.user1 = User.objects.create_user(username="user1", password="testpass123")
        self.user2 = User.objects.create_user(username="user2", password="testpass123")

        # Clients for each user
        self.client1 = Client.objects.create(owner=self.user1, name="Client A")
        self.client2 = Client.objects.create(owner=self.user2, name="Client B")

        # Projects for each client
        self.project1 = Project.objects.create(
            owner=self.user1,
            client=self.client1,
            name="Project 1",
        )
        self.project2 = Project.objects.create(
            owner=self.user2,
            client=self.client2,
            name="Project 2",
        )

        # Tasks for each project
        self.task1 = Task.objects.create(
            owner=self.user1,
            project=self.project1,
            title="Task 1",
            status=Task.STATUS_TODO,
            priority=Task.PRIORITY_HIGH,
            due_date=date.today() - timedelta(days=1),  # overdue
        )
        self.task2 = Task.objects.create(
            owner=self.user2,
            project=self.project2,
            title="Task 2",
            status=Task.STATUS_DONE,
            priority=Task.PRIORITY_LOW,
            due_date=date.today(),
        )
class ClientListViewTests(BaseCRMTestCase):
    def test_client_list_shows_only_owned_clients(self):
        # user1 logs in
        self.client.login(username="user1", password="testpass123")

        response = self.client.get(reverse("crm:client_list"))
        self.assertEqual(response.status_code, 200)

        clients = response.context["clients"]
        self.assertEqual(clients.count(), 1)
        self.assertEqual(clients[0], self.client1)
        # Ensure client2 is not in the queryset
        self.assertNotIn(self.client2, clients)
class ProjectListViewTests(BaseCRMTestCase):
    def test_project_list_shows_only_owned_projects(self):
        self.client.login(username="user1", password="testpass123")

        response = self.client.get(reverse("crm:project_list"))
        self.assertEqual(response.status_code, 200)

        projects = response.context["projects"]
        self.assertEqual(projects.count(), 1)
        self.assertEqual(projects[0], self.project1)
        self.assertNotIn(self.project2, projects)
class TaskListViewTests(BaseCRMTestCase):
    def test_task_list_shows_only_owned_tasks(self):
        self.client.login(username="user1", password="testpass123")

        response = self.client.get(reverse("crm:task_list"))
        self.assertEqual(response.status_code, 200)

        tasks = response.context["tasks"]
        self.assertEqual(tasks.count(), 1)
        self.assertEqual(tasks[0], self.task1)
        self.assertNotIn(self.task2, tasks)
class DashboardViewTests(BaseCRMTestCase):
    def test_dashboard_uses_only_owned_data(self):
        self.client.login(username="user1", password="testpass123")

        response = self.client.get(reverse("crm:dashboard"))
        self.assertEqual(response.status_code, 200)

        # client_count should be 1 for user1
        self.assertEqual(response.context["client_count"], 1)

        # project_counts should include only project1
        project_counts = list(response.context["project_counts"])
        total_projects = sum(item["total"] for item in project_counts)
        self.assertEqual(total_projects, 1)

        # task_counts should include only task1
        task_counts = list(response.context["task_counts"])
        total_tasks = sum(item["total"] for item in task_counts)
        self.assertEqual(total_tasks, 1)

    def test_dashboard_overdue_tasks_context(self):
        self.client.login(username="user1", password="testpass123")

        response = self.client.get(reverse("crm:dashboard"))
        self.assertEqual(response.status_code, 200)

        overdue_tasks = response.context["overdue_tasks"]
        # task1 is overdue and not done -> should be present
        self.assertIn(self.task1, overdue_tasks)
        # task2 belongs to user2, should not appear
        self.assertNotIn(self.task2, overdue_tasks)
from django.contrib import messages

class ProjectDeleteViewTests(BaseCRMTestCase):
    def test_cannot_delete_completed_project(self):
        # Arrange: mark user1's project as completed
        self.project1.status = Project.STATUS_COMPLETED
        self.project1.save()

        self.client.login(username="user1", password="testpass123")

        url = reverse("crm:project_delete", kwargs={"pk": self.project1.pk})
        response = self.client.get(url, follow=True)

        # Should redirect to project detail (not actually delete)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "crm/project_detail.html")

        # Project should still exist
        self.assertTrue(Project.objects.filter(pk=self.project1.pk).exists())

    def test_can_delete_non_completed_project(self):
        # Ensure status is something deletable
        self.project1.status = Project.STATUS_PLANNED
        self.project1.save()

        self.client.login(username="user1", password="testpass123")

        url = reverse("crm:project_delete", kwargs={"pk": self.project1.pk})
        response = self.client.post(url, follow=True)

        # After successful delete, we should land on project list
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "crm/project_list.html")

        # Project should be gone
        self.assertFalse(Project.objects.filter(pk=self.project1.pk).exists())
class TaskCreateViewTests(BaseCRMTestCase):
    def test_task_create_sets_owner_and_project(self):
        self.client.login(username="user1", password="testpass123")

        url = reverse(
            "crm:task_create_for_project",
            kwargs={"project_pk": self.project1.pk},
        )

        data = {
            "title": "New Task from view",
            "description": "Test description",
            "status": Task.STATUS_TODO,
            "priority": Task.PRIORITY_MEDIUM,
            "due_date": date.today(),
        }

        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)

        # Task should have been created
        new_task = Task.objects.get(title="New Task from view")
        self.assertEqual(new_task.owner, self.user1)
        self.assertEqual(new_task.project, self.project1)
