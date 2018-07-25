import json
import random

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from .models import Snippet
User = get_user_model
DUMMY_USER_NAME = 'dummy_username'


def get_dummy_user():
    return User.objects.create_user(username=DUMMY_USER_NAME)


class SnippetListTest(APITestCase):
    """
    Snippet List요청에 대한 테스트
    """

    URL = '/snippets/django_view/snippets/'

    def test_snippet_code(self):
        """
        요청 결과의 HTTP상태코드가 200인지 확인
        :return:
        """

        response = self.client.get(self.URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_snippet_list_count(self):
        """
        Snippet List를 요청시 DB에 있는 자료수와 같은 갯수가 리턴되는지 테스트
            Response(self.client.get 요청한 결과)에 온 데이터의 길이와
            Django ORM을 이용한 QuerySet의 갯수가 같은지 확인

            response.content에 ByteString타입의 JSON String이 들어있음
            테스트시 임의로 몇 개의 Snippet을 만들고 진행(테스트DB는 초기화된 상태로 시작)
        :return:
        """
        # snippet = Snippet(code='print "hello"\n')
        # snippet.save()
        user = get_dummy_user()
        for i in range(random.randint(10, 100)):
            Snippet.objects.create(
                code=f'a = {i}',
                owner=user,
            )
        # response.content 는 byte string 으로 json 형식의 파일이다.
        response = self.client.get(self.URL)

        # 파이썬 형식으로 변환 (string)
        data = json.loads(response.content)

        # response 로 받은 JSON 데이터의 길이와
        # Snippet 테이블의 자료수(COUNT)가 같은지를 테스트
        self.assertEqual(len(data), Snippet.objects.count())

    def test_snippet_list_order_by_created_descending(self):
        """
        Snippet list의 결과가 생성일자 내림차순인지 확인
        :return:
        """
        user = get_dummy_user()
        for i in range(random.randint(5, 10)):
            Snippet.objects.create(
                code=f'a = {i}',
                owner=user,
            )

        response = self.client.get(self.URL)
        data = json.loads(response.content)
        # snippets = Snippet.objects.order_by('-created')

        # response 에 전달된 JSON string 을 파싱한 Python 객체를 순회하며 'pk'값만 꺼냄
        # data_pk_list = []
        # for item in data:
        #     data_pk_list.append(item['pk'])

        # Snippet.objects.order_by('-created') QuerySet을 순회하며 각 Snippet 인스턴스의 pk 값만 꺼냄
        # snippets_pk_list = []
        # for snippet in snippets:
        #     snippets_pk_list.append(snippet.pk)

        self.assertEqual(
            # JSON으로 전달받은 데이터에서 pk만 꺼낸 리스트
            [item['pk'] for item in data],
            # DB에서 created역순으로 Pk값만 가져온 QuerySet으로 만든 리스트
            list(Snippet.objects.order_by('-created').values_list('pk', flat=True))
        )


CREATE_DATA = '''{
    "code": "print('hello, world')"
}'''
# print(type(CREATE_DATA))


class SnippetCreateTest(APITestCase):
    URL = '/snippets/generic_cbv/snippets/'
    def test_snippet_create_status_code(self):
        """
        201이 들어가는지 확인
        :return:
        """
        # response = self.client.post(
        #      '/snippets/django_view/snippets/',
        #      data=CREATE_DATA,
        #      content_type='application/json',
        # )
        # self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = get_dummy_user()
        self.client.force_authenticate(user=user)

        response = self.client.post(
            self.URL,
            data={'code': "print('hello, world')"},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_snippet_create_save_db(self):
        """
        요청 후 실제 DB에 저장되었는지(모든 필드값이 정상적으로 저장되는지 확인)
        :return:
        """
        # 생성할 Snippet에 사용될 정보
        snippet_data = {
            'title': 'SnippetTitle',
            'code': 'SnippetCode',
            'linenos': True,
            'language': 'c',
            'style': 'monokai',
        }
        user = get_dummy_user()
        self.client.force_authenticate(user=user)

        response = self.client.post(
            self.URL,
            data=snippet_data,
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = json.loads(response.content)

        # snippet_detail내의 키들을 동적으로 순회하면서 아래코드를 진행(for문)
        # self.assertEqual(data['title'], snippet_data['title'])
        # self.assertEqual(data['code'], snippet_data['code'])
        # self.assertEqual(data['linenos'], snippet_data['linenos'])
        # self.assertEqual(data['language'], snippet_data['language'])
        # self.assertEqual(data['style'], snippet_data['style'])

        for snippet_detail in snippet_data:
            self.assertEqual(data[snippet_detail], snippet_data[snippet_detail])

        self.assertEqual(data['owner'], user.username)

    def test_snippet_create_missing_code_raise_exception(self):
        """
        'code'데이터가 주어지지 않을 경우 적절한 Exception이 발생하는지 확인
        :return:
        """
        snippet_data = {
            'title': 'SnippetTitle',
            'linenos': True,
            'language': 'c',
            'style': 'monokai',
        }
        user = get_dummy_user()
        self.client.force_authenticate(user=user)

        response = self.client.post(
            self.URL,
            data=snippet_data,
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
