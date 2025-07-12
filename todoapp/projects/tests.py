from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from projects.models import Project, ProjectMember

User = get_user_model()

class ProjectMemberApiViewSetTestCase(APITestCase):

    def setUp(self):
        self.users = []
        for i in range(1, 9):
            user = User.objects.create_user(
                email=f"user{i}@example.com",
                password="pass123",
                first_name=f"User{i}",
                last_name=f"Test{i}"
            )
            self.users.append(user)
    
        self.project = Project.objects.create(name="Test Project", max_members=5)
        self.project2 = Project.objects.create(name="Second Project", max_members=5)
    
        ProjectMember.objects.create(project=self.project, member=self.users[0])
        ProjectMember.objects.create(project=self.project2, member=self.users[0])
        ProjectMember.objects.create(project=self.project, member=self.users[1])
        ProjectMember.objects.create(project=self.project2, member=self.users[1])
   
        
    def test_add_users_success(self):
        url = reverse('manage-add-users', kwargs={'pk': self.project.id})
        data = {"user_ids": [self.users[3].id, self.users[4].id, self.users[5].id]}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(ProjectMember.objects.filter(project=self.project).count(), 5)

    def test_add_user_exceeds_project_limit(self):
        ProjectMember.objects.create(project=self.project, member=self.users[3])
        ProjectMember.objects.create(project=self.project, member=self.users[4])
        ProjectMember.objects.create(project=self.project, member=self.users[5])

        url = reverse('manage-add-users', kwargs={'pk': self.project.id})
        data = {"user_ids": [self.users[6].id]}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Project has reached max members",
                      list(response.data['logs'].values())[0])

    def test_add_user_in_too_many_projects(self):
        url = reverse('manage-add-users', kwargs={'pk': self.project.id})
        data = {"user_ids": [self.users[0].id]} 
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['logs'][str(self.users[0].id)],
                         "User is already in 2 projects")

    def test_add_user_already_in_project(self):
        url = reverse('manage-add-users', kwargs={'pk': self.project.id})
        data = {"user_ids": [self.users[0].id]}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['logs'][str(self.users[0].id)],
                         "User is already in 2 projects")

    def test_remove_users(self):
        url = reverse('manage-remove-users', kwargs={'pk': self.project.id})
        data = {"user_ids": [self.users[0].id, self.users[1].id]}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(ProjectMember.objects.filter(project=self.project).count(), 0)

    def test_remove_non_member_user(self):
        url = reverse('manage-remove-users', kwargs={'pk': self.project.id})
        data = {"user_ids": [self.users[6].id]}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['logs'][str(self.users[6].id)],
                        "User is not a member of this project")
