from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
# from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.permissions import IsAuthenticated
from profiles_api import serializers
from profiles_api import models
from profiles_api import permissions

class HelloApiView(APIView):
    """Test API View"""

    serializer_class = serializers.HelloSerializer

    def get(self,request,format=None):
        """Returns a list of APIView features"""
        an_apiview = [
        "Uses HTTP methods as function (post,patch,put,delete)",
        "Is similar to a traditional django view",
        "Gives you the most control over your application logic",
        "Is mapped manually to URLs",
        ]

        return Response({'message' : 'Hello!', 'an_apiview': an_apiview})

    def post(self,request):
        """ Create a hello message with our name """
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}'
            return Response (
            {'message':message},
            201
            )
        else:
            return Response(
            serializer.errors,
            status = status.HTTP_400_BAD_REQUEST
            )

    def put(self,request,pk=None):
        """Handle updating an object"""
        return Response(
        {'message':'PUT'},
        201)

    def patch(self,request,pk=None):
        """Handle a partial update of an object"""
        return Response(
        {'message':'PATCH'},
        201
        )

    def delete(self,request,pk=None):
        """Delete an object """
        return Response(
        {'message':'DELETE'},
        201
        )

class HelloViewSet(viewsets.ViewSet):
    """test APi ViewSet"""

    serializer_class = serializers.HelloSerializer

    def list(self,request):
        """ Return a hello message """

        a_viewset = [
            "Uses actions (list,create,retrieve,update,partial update, and destroy)"
            "Automatically map to URLS using routers",
            "Provides more functionality with less code",
        ]

        return Response({'message': 'Hello!',
                        'a_viewset':a_viewset})

    def create(self,request):
        """Create a new hello messge"""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}'
            return Response (
            {'message':message},
            201
            )
        else:
            return Response(
            serializer.errors,
            status = status.HTTP_400_BAD_REQUEST
            )

    def retrieve(self,request,pk=None):
        """Handle getting an object by it's id"""
        return Response(
        {'message':'RETRIEVE',
        'http-method':'GET'},
        200)

    def update(self,request,pk=None):
        """Handle updating an object by it's id"""
        return Response(
        {'message':'UPDATE',
        'http-method':'PUT'},
        201)

    def partial_update(self,request,pk=None):
        """Handle part of an object by it's id"""
        return Response(
        {'message':'PARTIAL UPDATE',
        'http-method':'PATCH'},
        201)

    def destroy(self,request,pk=None):
        """Handle removing an object by it's id"""
        return Response(
        {'message':'DESTROY',
        'http-method':'DELETE'},
        201)

class UserprofileViewSet(viewsets.ModelViewSet):
    """Handle creating and updating profiles"""
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name','email',)

class UserLoginApiView(ObtainAuthToken):
    """Handle creating user authentiction tokens """
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class UserProfileFeedViewSet(viewsets.ModelViewSet):
    """Handles crating, reading and updating profile feed items """
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ProfileFeedItemSerializer
    queryset = models.ProfileFeedItem.objects.all()
    permission_classes = (
        permissions.UpdateOwnStatus,
        # IsAuthenticatedOrReadOnly
        IsAuthenticated
    )
    def perform_create(self,serializer):
        """Sets the user profile to thelogged in user """
        serializer.save(user_profile=self.request.user)
