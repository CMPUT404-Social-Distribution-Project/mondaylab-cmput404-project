
from rest_framework.generics import GenericAPIView
from author.serializers import AuthorSerializer
from author.models import Author
from rest_framework import response, status
from uuid import uuid4, UUID
from .serializers import AuthorSerializer
from .models import Author
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import filters
from django.shortcuts import get_list_or_404
from rest_framework_simplejwt.authentication import JWTAuthentication
JWT_authenticator = JWTAuthentication()


class UserViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'patch']
    serializer_class = AuthorSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Author.objects.all()
    # filter_backends = [filters.OrderingFilter]
    # ordering_fields = ['updated']
    # ordering = ['-updated']

    def list(self, request, pk=None):
        ''' Returns a queryset of all authors in the database
            Use: Send a GET to
                /service/authors/
        '''
        try:
            serializer = self.serializer_class(self.queryset, many=True)
            serializer = {"type": 'authors',"items":serializer.data}
            return Response(serializer, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(f"Error: {e}", status=status.HTTP_404_NOT_FOUND)

    def retrieve(self, request, pk=None):
        ''' Returns the requested author, given the UUID
            Use: Send a GET to
                /service/authors/<author_uuid>/
        '''
        # check if pk is a uuid
        try:
            UUID(pk)
            obj = Author.objects.get(uuid=pk)
            serializer = self.serializer_class(obj)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        ''' Updates an author's fields. Requires authentication token ('Authentication' header)
            Use: Send a POST to
                /service/authors/<author_uuid>/
        '''
        res = JWT_authenticator.authenticate(request)
        if res is not None:
            user, token = res;
            requesterUUID = token.payload.get('user_id').split('/')[-1]

            # if the requester is not what they say they are (aren't the actual author)
            if requesterUUID != pk:
                return Response(data="You are not the author, cannot modify.", status=status.HTTP_401_UNAUTHORIZED)
            
            obj = Author.objects.get(uuid=pk)
            serializer = self.serializer_class(obj, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
            else:
                return Response(data="Error validating data", status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data="No token was provided in the headers", status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        ''' Partially updates an author's fields with the requested given field(s)
            Requires authentication token ('Authentication' header)
            Use: Send a PATCH to
                /service/authors/<author_uuid>/
        '''
        # check if requester is actual author
        res = JWT_authenticator.authenticate(request)
        if res is not None:
            user, token = res;
            requesterUUID = token.payload.get('user_id').split('/')[-1]

            # if the requester is not what they say they are (aren't the actual author)
            if requesterUUID != pk:
                return Response(data="You are not the author, cannot modify.", status=status.HTTP_401_UNAUTHORIZED)

            # check if the requested field(s) to change exists
            for key in request.data.keys():
                print([f.name for f in Author._meta.get_fields()])
                if key not in [f.name for f in Author._meta.get_fields()]:
                    return Response(data=f"Specified field {key} does not exist", status=status.HTTP_400_BAD_REQUEST)
                elif key == "password":
                    return Response(data=f"No changy password :)", status=status.HTTP_400_BAD_REQUEST)
            
            obj = Author.objects.get(uuid=pk)
            serializer = self.serializer_class(obj, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
            else:
                return Response(data="Error validating data", status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data="No token was provided in the headers", status=status.HTTP_400_BAD_REQUEST)


