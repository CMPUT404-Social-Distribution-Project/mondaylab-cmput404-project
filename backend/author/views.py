
from rest_framework.generics import GenericAPIView
from author.serializers import AuthorSerializer
from author.models import Author
from rest_framework import response, status
from uuid import uuid4
from .serializers import AuthorSerializer
from .models import Author
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters

class AuthorApiView(GenericAPIView):
    serializer_class = AuthorSerializer
    def get(self, request):
        try:
            user = Author.objects.get(id=request.data.id)
            result = self.serializer_class(user, many=False)
            return response.Response(result.data, status=status.HTTP_200_OK)
        except Exception as e:
            return response.Response(status=status.HTTP_404_NOT_FOUND)

    # TODO: probably deprecated, using RegisterSerializer + AuthorManager to create authors instead
    # def post(self, request,):
    #     try: 
    #         serializer = self.serializer_class(data=request.data)
    #         if serializer.is_valid():
    #             host = request.build_absolute_uri('/')[:-1]
    #             id =str(host) +'/authors/'+ str(uuid4())
    #             serializer.save(id = id, url =id)
    #             return response.Response(serializer.data, status=status.HTTP_200_OK)

    #         else:
    #             return response.Response(f"Error: Data is valid", status=status.HTTP_400_BAD_REQUEST)
    #     except Exception as e:
    #         return response.Response(f"Error: {e}", status=status.HTTP_400_BAD_REQUEST)

class AuthorsApiView(GenericAPIView):
    serializer_class = AuthorSerializer
    def get(self, request):
        try:
            authors = Author.objects.all()
            result = self.serializer_class(authors, many=True)
            result= {"type": 'authors',"items":result.data}
            return response.Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return response.Response(status=status.HTTP_404_NOT_FOUND)


class UserViewSet(viewsets.ModelViewSet):
    http_method_names = ['get']
    serializer_class = AuthorSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['updated']
    ordering = ['-updated']

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Author.objects.all()

    def get_object(self):
        lookup_field_value = self.kwargs[self.lookup_field]

        obj = Author.objects.get(lookup_field_value)
        self.check_object_permissions(self.request, obj)

        return obj

