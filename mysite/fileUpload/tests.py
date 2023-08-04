from unittest.mock import patch
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User 

# Create your tests here.

class RequiresLogin(TestCase):
    def test_upload(self):
        response = self.client.get(reverse("fileUpload:upload"))
        self.assertEqual(response.status_code,302)
        self.assertEqual(response.url,"/users/login/?next=/fileUpload/upload")
    def test_list(self):
        response = self.client.get(reverse("fileUpload:list"))
        self.assertEqual(response.status_code,302)
        self.assertEqual(response.url,"/users/login/?next=/fileUpload/list")

class LoginTry(TestCase):
    def setUp(self):
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(username='testuser2', password='2HJ1vRV0Z&3iD')

        
        test_user1.save()
        test_user2.save()

    @patch('fileUpload.api.sendImageAPI')
    def test_login1(self, mock_get):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse("fileUpload:list"))
        self.assertEqual(response.status_code,200)


        arg_nofile = {"desc":"No File"}
        response = self.client.post(reverse("fileUpload:upload"),data = arg_nofile)
        self.assertEqual(response.status_code,200)
        self.assertContains(response,"This field is required.")

        #upload actual file
        arg_file = {"desc":"file_added","files":open("test_data/test_img_1.png")}
        

        mock_get.return_value.json.return_value = {'is_success': True, 'img_num': 1, 'timestamp' : "2023-08-04 10:56:56"}

        
        response = self.client.post(reverse("fileUpload:upload"),data = arg_file)
        #print(response.content)
        response.charset = 'utf-8'
        self.assertEqual(response.status_code,200)
        self.assertNotContains(response,"This field is required.")


        
