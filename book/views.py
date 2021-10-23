from rest_framework import viewsets
from rest_framework.views import APIView
from book.models import Author, Category, Comment, Book, Favorite, Publisher
from book.serializers import BookSerializer, CommentSerializer, FavoriteSerializer
from django.shortcuts import get_object_or_404, render
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed,PermissionDenied
from user.models import User
import jwt

# Create your views here.
def getUser(request):
    token = request.COOKIES.get('jwt')
        
    if not token:
        raise AuthenticationFailed('Unauthenticated!')

    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated!')

    user = User.objects.filter(id = payload['id']).first()
    return user

def getFilter(kind, name, user=None):
    if kind == "author":
        if user == None:
            queryset = Book.objects.filter(author=name)
        else:
            queryset = Book.objects.filter(author=name, user=user)
    elif kind == "publisher":
        if user == None:
            queryset = Book.objects.filter(publisher=name)
        else:
            queryset = Book.objects.filter(publisher=name, user=user)
    elif kind == "category":
        if user == None:
            queryset = Book.objects.filter(category=name)
        else:
            queryset = Book.objects.filter(category=name, user=user)
    else:
        return Response({
            "message": "invalid url"
        })
    return queryset

class BookViewset(viewsets.ModelViewSet):
    #queryset = Book.objects.all()
    serializer_class = BookSerializer
    def list(self, request):
        queryset = Book.objects.all()
        serializer = BookSerializer(queryset, many=True)
        return Response(serializer.data)

    def search(self, request, name=None):
        queryset = Book.objects.filter(name__contains=name)
        serializer = BookSerializer(queryset, many=True)
        return Response(serializer.data)

    def searchFromMyBooks(self, request, name=None):
        user = getUser(request)
        queryset = Book.objects.filter(name__contains=name, user=user)
        serializer = BookSerializer(queryset, many=True)
        return Response(serializer.data)

    def filterBooks(self, request, kind=None, name=None):
        queryset = getFilter(kind, name)
        serializer = BookSerializer(queryset, many=True)
        if serializer.data == []:
            return Response({
                "detail": "Bulunamadı."
            })
        return Response(serializer.data)
    
    def filterFromMyBooks(self, request, kind=None, name=None):
        user = getUser(request)
        queryset = getFilter(kind, name, user)
        serializer = BookSerializer(queryset, many=True)
        if serializer.data == []:
            return Response({
                "detail": "Bulunamadı."
            })
        return Response(serializer.data)
        

    def create(self, request):
        user = getUser(request)
        request.data['user'] = user.id
        serializer = BookSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        book = get_object_or_404(Book, id=pk)
        comments = Comment.objects.filter(book=book)
        comments_serializer = CommentSerializer(comments, many=True)
        serializer = BookSerializer(book)
        data = serializer.data
        data['comments'] = comments_serializer.data
        return Response(data)

    def update(self, request, pk=None):
        user = getUser(request)
        book = get_object_or_404(Book, id=pk)

        if user.id != book.user.id:
            raise PermissionDenied("You are not allowed to do this action!")

        request.data['user'] = user.id
        request.data['id'] = pk
        serializer = BookSerializer(data=request.data, instance=book)

        if serializer.is_valid():
            serializer.save()

        return Response(serializer.data)
    
    def destroy(self, request, pk=None):
        user = getUser(request)
        book = get_object_or_404(Book, id=pk)
        if user.id != book.user.id:
            raise PermissionDenied("You are not allowed to do this action!")
        book.delete()
        return Response({
            "messages":"success"
        })


class CommentViewset(viewsets.ModelViewSet):
    #queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    def create(self, request, bookId=None):
        user = getUser(request)
        book = get_object_or_404(Book, id=bookId)
        request.data['user'] = user.id
        request.data['book'] = bookId
        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        user = getUser(request)
        comment = get_object_or_404(Comment, id=pk)
        if user.id != comment.user.id:
            raise PermissionDenied("You are not allowed to do this action!")
        comment.delete()
        return Response({
            "messages":"success"
        })

class FavoriteViewset(viewsets.ModelViewSet):
    serializer_class = FavoriteSerializer

    def list(self, request):
        user = getUser(request)
        queryset = Favorite.objects.filter(user=user)
        serializer = FavoriteSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, bookId=None):
        user = getUser(request)
        book = get_object_or_404(Book, id=bookId)
        request.data['user'] = user.id
        request.data['book'] = bookId
        serializer = FavoriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def destroy(self, request, bookId=None):
        user = getUser(request)
        favorite_book = get_object_or_404(Favorite, id=bookId)
        if user.id != favorite_book.user.id:
            raise PermissionDenied("You are not allowed to do this action!")
        favorite_book.delete()
        return Response({
            "messages":"success"
        })



class ListAuthor(APIView):
    def get(self, request):
        authors = [author.full_name for author in Author.objects.all()]
        return Response(authors)

class ListPublisher(APIView):
    def get(self, request):
        publishers = [publisher.name for publisher in Publisher.objects.all()]
        return Response(publishers)

class ListCategory(APIView):
    def get(self, request):
        categories = [category.name for category in Category.objects.all()]
        return Response(categories)