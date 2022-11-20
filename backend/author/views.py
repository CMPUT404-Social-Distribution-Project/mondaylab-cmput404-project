
from rest_framework.generics import GenericAPIView
from author.serializers import AuthorSerializer
from author.models import Author
from rest_framework import response, status
from uuid import uuid4, UUID
from .serializers import AuthorSerializer
from .models import Author
from rest_framework import viewsets, filters
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import filters
from django.shortcuts import get_list_or_404
from backend.utils import isUUID, isAuthorized, check_github_valid
from backend.pagination import CustomPagination

class UserViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'patch', 'post']
    serializer_class = AuthorSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Author.objects.all()
    filter_backends = [filters.SearchFilter,]
    search_fields = ['displayName']
    pagination_class = CustomPagination

    def filter_queryset(self, queryset):
        '''Issue with overriding list() method and needing to override filter_queryset
        to get proper search filter.
        Ref: https://stackoverflow.com/questions/52366296/django-filters-does-not-work-with-the-viewset
        Answer by Sparkp1ug
        '''
        filter_backends = (filters.SearchFilter, )

        # Other condition for different filter backend goes here

        for backend in list(filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, view=self)
        return queryset

    def list(self, request, pk=None):
        ''' Returns a queryset of all authors in the database.
            Use: Send a GET to
                /service/authors/
        '''
        try:

            authorsQuerySet = self.filter_queryset(self.queryset)
            authorsPaginateQuerySet = self.paginate_queryset(authorsQuerySet)
            authorsSerializer = AuthorSerializer(authorsPaginateQuerySet, many=True, context={"request": request})
            authorsPaginationResult = self.get_paginated_response(authorsSerializer.data)
            authors = authorsPaginationResult.data.get("results")
            
            result = {
                "type": "authors",
                "items": authors
            }
            
            return Response(result, status=status.HTTP_200_OK)

            # serializer = self.serializer_class(self.filter_queryset(self.queryset), many=True, context={"request": request})
            # serializer = {"type": "authors", "items":serializer.data}
            # return Response(serializer, status=status.HTTP_200_OK)
            
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

    @action(detail=False, methods=['post'])
    def post(self, request, pk=None):
        ''' Updates an author's fields. Requires authentication token ('Authentication' header)
            Use: Send a POST to
                /service/authors/<author_uuid>/
        '''
        if not isAuthorized(request, pk): 
            return response.Response(f"Unauthorized: You are not the author", status=status.HTTP_401_UNAUTHORIZED)
        else:
            try:
                # check if the name to change is unique
                obj = Author.objects.get(uuid=pk)
                if not self.check_is_unique(request, obj):
                    return Response(data=f"Author with displayName = {request.data.get('displayName')} already exists! Choose another name", status=status.HTTP_400_BAD_REQUEST)

                # check if new github url is a valid url
                if not check_github_valid(request):
                    return Response(data=f"The given GitHub URL is not a valid URL! Make sure to not include 'www.'!", status=status.HTTP_400_BAD_REQUEST)

                serializer = self.serializer_class(obj, data=request.data)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
                else:
                    return Response(data="Error validating data", status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response(f"Error: {e}", status=status.HTTP_404_NOT_FOUND)


    def partial_update(self, request, pk=None):
        ''' Partially updates an author's fields with the requested given field(s)
            Requires authentication token ('Authentication' header)
            Use: Send a PATCH to
                /service/authors/<author_uuid>/
        '''
        if not isAuthorized(request, pk): 
            return response.Response(f"Unauthorized: You are not the author", status=status.HTTP_401_UNAUTHORIZED)
        else:

            # check if the requested field(s) to change exists
            for key in request.data.keys():
                if key not in [f.name for f in Author._meta.get_fields()]:
                    return Response(data=f"Specified field {key} does not exist", status=status.HTTP_400_BAD_REQUEST)
                elif key == "password":
                    return Response(data=f"No changy password :)", status=status.HTTP_400_BAD_REQUEST)
            
            # check if the name to change is unique
            obj = Author.objects.get(uuid=pk)
            if not self.check_is_unique(request, obj):
                return Response(data=f"Author with displayName = {request.data.get('displayName')} already exists! Choose another name", status=status.HTTP_400_BAD_REQUEST)
            
            if not check_github_valid(request):
                return Response(data=f"The given GitHub URL is not a valid URL! Make sure to not include 'www.'!", status=status.HTTP_400_BAD_REQUEST)

            serializer = self.serializer_class(obj, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
            else:
                return Response(data="Error validating data", status=status.HTTP_400_BAD_REQUEST)

    def check_is_unique(self, request, req_author):
        # check if the display name is unique
        requestedDisplayName = request.data.get("displayName")
        if requestedDisplayName != req_author.displayName:       # make sure requested name to change is not the same    
            # if the requested displayName change is not the same as before, check if the displayName is unique
            authorExists = Author.objects.filter(displayName=requestedDisplayName).first()
            if authorExists != None:
                return False
        return True


