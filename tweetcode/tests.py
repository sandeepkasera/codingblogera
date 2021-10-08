from django.contrib.auth import get_user_model
from django.test import TestCase

from rest_framework.test import APIClient


from .models import Posts
# Create your tests here.
User = get_user_model()


class PostTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='cfe', password='somepassword')
        self.userb = User.objects.create_user(username='cfe2', password='somepassword2')
        post_obj = Posts.objects.create(content="my first tweet", user=self.user)
        post_obj = Posts.objects.create(content="my first tweet", user=self.user)
        post_obj = Posts.objects.create(content="my first tweet", user=self.userb)
        self.currentCount = Posts.objects.all().count()

    def test_post_created(self):
        post_obj = Posts.objects.create(content="my second tweet", user=self.user)
        self.assertEqual(post_obj.id, 4)
        self.assertEqual(post_obj.user, self.user)

    def get_client(self):
        client = APIClient()
        client.login(username=self.user, password='somepassword')
        return client

    def test_post_list(self):
        client = self.get_client()
        response = client.get("/api/posts/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 3)
        
  

  

        response = client.post("/api/posts/action/", {"id":2, "action":"unlike"})
        self.assertEqual(response.status_code, 200)



    def test_post_create_api_view(self):
        request_data = {"content": "This is my test post"}
        client = self.get_client()
        response = client.post("/api/posts/create/",request_data)
        self.assertEqual(response.status_code, 201)
        response_data = response.json()
        new_post_id = response_data.get("id")
        self.assertEqual(self.currentCount+1, new_post_id)


    def test_post_detail_api_view(self):
        client = self.get_client()
        response = client.get("/api/posts/1/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        _id = data.get("id")
        self.assertEqual(_id, 1)

    def test_post_delete_api_view(self):
        client = self.get_client()
        response = client.delete("/api/posts/1/delete/")
        self.assertEqual(response.status_code, 200)
        
        client = self.get_client()
        response = client.delete("/api/posts/1/delete/")
        self.assertEqual(response.status_code, 404)
        
        response_incorrect_owner = client.delete("/api/posts/3/delete/")
        self.assertEqual(response_incorrect_owner.status_code, 401)
       


      
        
        