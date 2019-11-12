import logging
from django.shortcuts import render

# Create your views here.
from urllib.parse import parse_qs

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView,CreateAPIView
from rest_framework_jwt.settings import api_settings

from oauth.execptions import QQAPIError, WEIBOAPIError
from oauth.models import OAuthUser
from oauth.serializers import QQUserSerializer, WBUserSerializer, QuestionOAuthShareSerializer
from oauth.utils import QQOAuth, WEIBOAuth

logger = logging.getLogger('django')


class QQOAuthURLView(APIView):
    """请求QQ登录的URL网址的类"""

    def get(self, request):
        next = request.query_params.get('next')
        qq_oauth = QQOAuth(state=next)
        login_url = qq_oauth.get_login_url()
        return Response({'login_url':login_url})



class QQOAuthUser(CreateAPIView):
    """请求access token的值"""
    serializer_class = QQUserSerializer

    def get(self, request):
        code = request.query_params.get('code')
        if not code:
            logger.error('缺少code参数')
            return Response({'message':'缺少code参数'},status.HTTP_400_BAD_REQUEST)
        qq_oauth = QQOAuth()
        try:
            access_token = qq_oauth.get_access_token(code)
        except QQAPIError as e:
            logger.error('access_token获取失败:%s' % e)
            return Response({'message': 'access_token获取失败'}, status.HTTP_500_INTERNAL_SERVER_ERROR)
        try:
            openid = qq_oauth.get_openid(access_token)
        except QQAPIError as e:
            logger.error('获取openid失败：%s'%e)
            return Response({'message': '获取openid失败'}, status.HTTP_500_INTERNAL_SERVER_ERROR)

        qq_user = OAuthUser.objects.filter(uid=openid).first()

        if not qq_user:
            token = qq_oauth.generate_save_user_token(openid)
            data = {'access_token':token}
            return Response(data=data)
        user = qq_user.user
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        user.token = token
        response = Response({
            'user_id':user.id,
            'username':user.username,
            'token':token
        })
        request.user = user
        return response


class WBOAuthURLView(APIView):
    """请求QQ登录的URL网址的类"""

    def get(self, request):
        next = request.query_params.get('next')
        wb_oauth = WEIBOAuth(state=next)
        login_url = wb_oauth.get_authorize_url()
        return Response({'login_url':login_url})


class WBOAuthUser(CreateAPIView):
    """请求access token的值"""
    serializer_class = WBUserSerializer

    def get(self, request):
        code = request.query_params.get('code')
        if not code:
            logger.error('缺少code参数')
            return Response({'message':'缺少code参数'},status.HTTP_400_BAD_REQUEST)
        wb_oauth = WEIBOAuth()
        try:
            (oauth_access_token, uid) = wb_oauth.get_access_token_and_uid(code)
        except QQAPIError as e:
            logger.error('access_token获取失败:%s' % e)
            return Response({'message': 'access_token获取失败'}, status.HTTP_500_INTERNAL_SERVER_ERROR)

        wb_user = OAuthUser.objects.filter(uid=uid).first()

        if not wb_user:
            token = wb_oauth.generate_save_user_token(uid)
            data = {'access_token':token, 'oauth_access_token':oauth_access_token}
            return Response(data=data)
        user = wb_user.user
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        user.token = token
        response = Response({
            'user_id':user.id,
            'username':user.username,
            'token':token,
            'oauth_access_token': oauth_access_token,
        })
        request.user = user
        return response


class QuestionOAuthShareView(GenericAPIView):
    """问题第三方分享视图"""
    serializer_class = QuestionOAuthShareSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        oauth_access_token = request.data.pop('oauth_access_token')
        content = request.data.get('content', None)
        if not content:
            return Response({'message':"错误的请求"},status=status.HTTP_400_BAD_REQUEST)
        try:
            data = WEIBOAuth().share_to_wb(oauth_access_token,content)
        except WEIBOAPIError as e:
            logger.error('access_token获取失败:%s' % e)
            return Response({'message': '分享失败'}, status.HTTP_500_INTERNAL_SERVER_ERROR)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data, status=status.HTTP_201_CREATED)

