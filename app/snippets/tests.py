import json
import random

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Snippet


class SnippetListTest(APITestCase):
    """
    Snippet List요청에 대한 테스트
    """
    def test_status_code(self):
        """
        요청 결과의 HTTP상태코드가 200인지 확인
        :return:
        """
        response = self.client.get('/snippets/django_view/snippets/')
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
        for i in range(random.randint(10, 100)):
            Snippet.objects.create(code=f'a = {i}')
        # response.content 는 byte string 으로 json 형식의 파일이다.
        response = self.client.get('/snippets/django_view/snippets/')

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
        for i in range(random.randint(5, 10)):
            Snippet.objects.create(code=f'a = {i}')

        response = self.client.get('/snippets/django_view/snippets/')
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
