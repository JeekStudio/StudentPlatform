import os, json
from PIL import Image, ImageChops

from rest_framework.test import APIClient
from django.utils import timezone
from testing.testcases import TestCase

from society.constants import SocietyType, SocietyStatus, JoinSocietyRequestStatus, ActivityRequestStatus
from society.models import JoinSocietyRequest, ActivityRequest
from society_manage.models import CreditDistribution
from society_bureau.api.services import SettingsService
from society.constants import TEST_FILE_PATH


class SocietyManageMemberTests(TestCase):
    def setUp(self):
        self.user1 = self.createUser('society1')
        self.society = self.createSociety(
            user=self.user1,
            society_id=101,
            members=None,
            society_type=SocietyType.HUMANISTIC
        )
        self.user2 = self.createUser(
            username='student'
        )
        self.student = self.createStudent(
            user=self.user2
        )

    def test_kick_member(self):
        url = '/api/society_manage/member/kick/'
        data = {
            'member_id': self.student.id
        }
        client = APIClient(enforce_csrf_checks=True)
        client.force_authenticate(self.user1)
        response = client.post(url, data=data, decode=True)
        self.assertEqual(response.status_code, 400)

        self.society.members.add(self.student)
        response = client.post(url, data=data, decode=True)
        self.assertEqual(response.status_code, 202)

        data = {
            'hello': 'ncjnb'
        }
        response = client.post(url, data=data, decode=True)
        self.assertEqual(response.status_code, 400)

        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 403)


class SocietyManageJoinRequestTests(TestCase):
    def setUp(self):
        self.student_user1 = self.createUser(
            'ncj1'
        )
        self.student1 = self.createStudent(
            user=self.student_user1
        )
        self.student_user2 = self.createUser(
            'ncj2'
        )
        self.student2 = self.createStudent(
            user=self.student_user2
        )
        self.society_user = self.createUser(
            username='101'
        )
        self.society = self.createSociety(
            user=self.society_user,
            members=None,
            society_id=101,
            society_type=SocietyType.HUMANISTIC
        )
        self.jr1 = JoinSocietyRequest.objects.create(
            society=self.society,
            member=self.student1,
            status=JoinSocietyRequestStatus.ACCEPTED
        )
        self.jr2 = JoinSocietyRequest.objects.create(
            society=self.society,
            member=self.student2
        )

    def test_list_join_requests(self):
        url = '/api/society_manage/join_request/'

        client = APIClient(enforce_csrf_checks=True)
        client.force_authenticate(self.society_user)
        response = client.get(url, decode=True)
        self.assertEqual(response.data['results'][0]['member']['name'], self.student1.name)
        self.assertEqual(response.data['results'][1]['member']['class_num'], self.student2.class_num)

        data = {
            'status': JoinSocietyRequestStatus.ACCEPTED
        }
        response = client.get(url, data=data, decode=True)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['member']['grade'], self.student1.grade)

        data = {
            'status': JoinSocietyRequestStatus.WAITING
        }
        response = client.get(url, data=data, decode=True)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['member']['grade'], self.student2.grade)

        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_update_join_request(self):
        url = '/api/society_manage/join_request/{}/'.format(self.jr1.pk)
        client = APIClient(enforce_csrf_checks=True)
        client.force_authenticate(self.society_user)
        data = {
            'status': JoinSocietyRequestStatus.DENIED
        }
        response = client.put(url, data=data, decode=True)
        self.assertEqual(response.status_code, 200)
        self.jr1.refresh_from_db()
        self.assertEqual(self.jr1.status, JoinSocietyRequestStatus.DENIED)


class SocietyManageActivityTests(TestCase):
    def setUp(self):
        self.society_user = self.createUser(
            username='101'
        )
        self.society = self.createSociety(
            user=self.society_user,
            members=None,
            society_id=101,
            society_type=SocietyType.HUMANISTIC
        )
        self.ar1 = ActivityRequest.objects.create(
            society=self.society,
            title='keep calm',
            content='pick hanzo or die',
            place='5510',
            start_time=timezone.now()
        )
        self.ar2 = ActivityRequest.objects.create(
            society=self.society,
            title='make epic shit',
            place='little forest',
            status=ActivityRequestStatus.ACCEPTED,
            start_time=timezone.now()
        )

    def test_retrieve_activity_requests(self):
        url = '/api/society_manage/activity/{}/'.format(self.ar1.pk)

        client = APIClient(enforce_csrf_checks=True)
        response = client.get(url, decode=True)
        self.assertEqual(response.status_code, 403)

        client.force_authenticate(self.society_user)
        response = client.get(url, decode=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], 'keep calm')
        self.assertEqual(response.data['content'], 'pick hanzo or die')
        self.assertEqual(response.data['place'], '5510')

    def test_list_activity_requests(self):
        url = '/api/society_manage/activity/'

        client = APIClient(enforce_csrf_checks=True)
        response = client.get(url, decode=True)
        self.assertEqual(response.status_code, 403)

        client.force_authenticate(self.society_user)
        response = client.get(url, decode=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['results'][0]['title'], 'make epic shit')
        self.assertEqual(response.data['results'][1]['title'], 'keep calm')
        self.assertEqual(response.data['results'][0]['status'], ActivityRequestStatus.ACCEPTED)

        data = {
            'status': ActivityRequestStatus.ACCEPTED
        }
        response = client.get(url, data=data, decode=True)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'make epic shit')

        data = {
            'status': ActivityRequestStatus.WAITING
        }
        response = client.get(url, data=data, decode=True)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'keep calm')

    def test_update_activity_requests(self):
        url = '/api/society_manage/activity/{}/'.format(self.ar1.pk)

        client = APIClient(enforce_csrf_checks=True)
        data = {
            'status': ActivityRequestStatus.ACCEPTED,
            'title': 'do homework',
            'place': 'principal room'
        }
        response = client.patch(url, data=data, decode=True)
        self.assertEqual(response.status_code, 403)

        client.force_authenticate(self.society_user)
        response = client.patch(url, data=data, decode=True)
        self.assertEqual(response.status_code, 200)
        self.ar1.refresh_from_db()
        self.assertEqual(self.ar1.status, ActivityRequestStatus.WAITING)  # test read_only
        self.assertEqual(self.ar1.title, 'do homework')
        self.assertEqual(self.ar1.place, 'principal room')

        url = '/api/society_manage/activity/{}/'.format(self.ar2.pk)
        data = {
            'title': 'do homework',
            'place': 'principal room'
        }
        response = client.patch(url, data=data, decode=True)
        self.assertEqual(response.status_code, 403)

    def test_create_activity_requests(self):
        url = '/api/society_manage/activity/'
        data = {
            'title': 'fudan lecture',
            'society': self.society_user.society.id,
            'content': '666',
            'place': '5106',
            'start_time': timezone.now()
        }
        client = APIClient(enforce_csrf_checks=True)
        response = client.post(url, data=data, decode=True)
        self.assertEqual(response.status_code, 403)

        client.force_authenticate(self.society_user)
        response = client.post(url, data=data, decode=True)
        self.assertEqual(response.status_code, 201)
        ar3 = ActivityRequest.objects.get(pk=response.data['id'])
        self.assertEqual(ar3.status, ActivityRequestStatus.WAITING)
        self.assertEqual(ar3.title, 'fudan lecture')
        self.assertEqual(ar3.content, '666')
        self.assertEqual(ar3.society, self.society)

    def test_destroy_activity_requests(self):
        url = '/api/society_manage/activity/{}/'.format(self.ar1.pk)

        client = APIClient(enforce_csrf_checks=True)
        response = client.delete(url, decode=True)
        self.assertEqual(response.status_code, 403)

        client.force_authenticate(self.society_user)
        response = client.delete(url, decode=True)
        self.assertEqual(response.status_code, 204)
        self.assertIsNone(ActivityRequest.objects.filter(pk=self.ar1.pk).first())


class SocietyManageCreditTests(TestCase):
    def setUp(self):
        self.society_user1 = self.createUser('su1')
        self.society_user2 = self.createUser('su2')
        self.society1 = self.createSociety(self.society_user1, members=None)
        self.society2 = self.createSociety(self.society_user2, members=None)
        self.student_user1 = self.createUser('stu1')
        self.student_user2 = self.createUser('stu2')
        self.student1 = self.createStudent(self.student_user1)
        self.student2 = self.createStudent(self.student_user2)

    def test_retrieve(self):
        url = '/api/society_manage/credit/'

        society1_cd = CreditDistribution.objects.create(
            society=self.society1,
            year=SettingsService.get('year'),
            semester=SettingsService.get('semester')
        )
        self.society1.members.set([self.student1, self.student2])
        client = APIClient(enforce_csrf_checks=True)
        client.force_authenticate(self.society_user1)

        params = {
            'year': SettingsService.get('year'),
            'semester': SettingsService.get('semester')
        }
        res = client.get(url, data=params, encode=True)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['year'], timezone.datetime.now().year)
        self.assertEqual(res.data['semester'], 1)
        self.assertEqual(len(res.data['available_receivers']), 2)
        self.assertEqual(res.data['available_receivers'][0]['name'], self.student1.name)
        self.assertEqual(res.data['open'], True)

        society1_cd.receivers.add(self.student1)
        society1_cd.refresh_from_db()
        res = client.get(url, data=params, encode=True)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data['available_receivers']), 2)
        self.assertEqual(len(res.data['receivers']), 1)

        society2_cd = CreditDistribution.objects.create(
            society=self.society2,
            year=SettingsService.get('year'),
            semester=SettingsService.get('semester')
        )
        self.society2.members.set([self.student1, self.student2])

        client.force_authenticate(self.society_user2)
        res = client.get(url, data=params, encode=True)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data['available_receivers']), 1)

        # test 404
        params = {
            'year': 1111,
            'semester': 11
        }
        res = client.get(url, data=params, encode=True)
        self.assertEqual(res.status_code, 404)

    def test_update(self):
        society1_cd = CreditDistribution.objects.create(
            society=self.society1,
            year=SettingsService.get('year'),
            semester=SettingsService.get('semester')
        )

        self.society1.members.add(self.student1)

        client = APIClient(enforce_csrf_checks=True)
        client.force_authenticate(self.society_user1)

        url = '/api/society_manage/credit/{}/'.format(society1_cd.id)
        data = {
            'receivers': [
                self.student1.id
            ]
        }
        res = client.patch(url, data=data, encode=True)
        self.assertEqual(res.status_code, 200)
        society1_cd.refresh_from_db()
        self.assertEqual(society1_cd.receivers_count, 1)
        self.assertEqual(society1_cd.receivers.first(), self.student1)

        data = {
            'receiver': []
        }
        res = client.patch(url, data=data, encode=True)
        self.assertEqual(res.status_code, 400)

        society1_cd.open = False
        society1_cd.save()
        data = {
            'receivers': [
                self.student1.id
            ]
        }
        res = client.patch(url, data=data, encode=True)
        self.assertEqual(res.status_code, 406)


class SocietyProfileTests(TestCase):
    def setUp(self):
        self.society_user1 = self.createUser(
            username='101'
        )
        self.society_user2 = self.createUser(
            username='201'
        )
        self.society1 = self.createSociety(
            user=self.society_user1,
            members=None,
            society_id=101,
            society_type=SocietyType.HUMANISTIC
        )

        self.society2 = self.createSociety(
            user=self.society_user2,
            members=None,
            society_id=201,
            society_type=SocietyType.SELFRELIANCE
        )

    def test_retrieve_profile(self):
        url = '/api/society_manage/profile/'
        client = APIClient(enforce_csrf_checks=True)

        # without login
        res = client.get(url)
        self.assertEqual(res.status_code, 403)

        # society not active
        client.force_authenticate(self.society_user1)
        res = client.get(url)
        self.assertEqual(res.status_code, 403)

        self.society1.status = SocietyStatus.ACTIVE
        self.society1.save()
        res = client.get(url)
        self.assertEqual(res.status_code, 200)
        print(res.data['id'], self.society1.pk)
        print(res.data['society_id'], self.society1.society_id)


    def test_update_profile(self):
        url1 = '/api/society_manage/profile/{}/'.format(self.society1.pk)
        url2 = '/api/society_manage/profile/{}/'.format(self.society2.pk)
        client = APIClient(enforce_csrf_checks=True)
        data = {
            'name': 'test',
            'type': SocietyType.SCIENTIFIC,
            'status': SocietyStatus.ARCHIVED
        }

        # without login
        res = client.patch(url1, data=data)
        self.assertEqual(res.status_code, 403)

        # society not active
        client.force_authenticate(self.society_user1)
        self.assertEqual(res.status_code, 403)

        self.society1.status = SocietyStatus.ACTIVE
        self.society1.save()
        self.society2.status = SocietyStatus.ACTIVE
        self.society2.save()

        # modify others' profile
        res = client.patch(url2, data=data)
        self.society2.refresh_from_db()
        self.assertEqual(self.society2.name, 'jeek1')

        res = client.patch(url1, data=data)
        self.society1.refresh_from_db()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(self.society1.name, 'test')
        self.assertEqual(self.society1.type, SocietyType.HUMANISTIC)
        self.assertEqual(self.society1.status, SocietyStatus.ACTIVE)

    def test_upload_avatar(self):
        url = '/api/society_manage/profile/upload_avatar/'
        # use 'rb' to solve encoding issue
        original_file = open(os.path.join(TEST_FILE_PATH, 'jeek.jpeg'), 'rb')
        cropped_file = open(os.path.join(TEST_FILE_PATH, 'cropped.jpeg'), 'rb')
        crop = {
            'x': 25,
            'y': 25,
            'width': 50,
            'height': 50
        }
        data = {
            'avatar': original_file,
            'crop': json.dumps(crop)
        }

        client = APIClient(enforce_csrf_checks=True)
        client.force_authenticate(self.society_user1)

        res = client.post(url, data=data, decode=True)
        self.assertEqual(res.status_code, 202)
        self.society1.refresh_from_db()

        cropped_img = Image.open(cropped_file)
        server_img = Image.open(self.society1.avatar)
        diff = ImageChops.difference(cropped_img, server_img)

        self.assertIsNone(diff.getbbox())
        original_file.close()
        cropped_file.close()
