from django.urls import path
from .views import BookViewset, CommentViewset, FavoriteViewset, ListAuthor, ListCategory, ListPublisher


urlpatterns = [
    # books
    path('listBooks', BookViewset.as_view({'get': 'list'})),
    path('search/<str:name>', BookViewset.as_view({'get': 'search'})),
    path('searchMyBooks/<str:name>',BookViewset.as_view({'get': 'searchFromMyBooks'})),
    path('filter/<str:kind>/<str:name>', BookViewset.as_view({'get':'filterBooks'})),
    path('filterMyBooks/<str:kind>/<str:name>', BookViewset.as_view({'get':'filterFromMyBooks'})),
    # book
    path('detailsBook/<int:pk>', BookViewset.as_view({'get': 'retrieve'})),
    path('addBook', BookViewset.as_view({'post': 'create'})),
    path('updateBook/<int:pk>', BookViewset.as_view({'put': 'update'})),
    path('deleteBook/<int:pk>', BookViewset.as_view({'delete': 'destroy'})),

    # comment
    path('book/<int:bookId>/addComment', CommentViewset.as_view({'post': 'create'})),
    path('comment/delete/<int:pk>', CommentViewset.as_view({'delete': 'destroy'})),

    # favorite
    path('favorite/list', FavoriteViewset.as_view({'get': 'list'})),
    path('favorite/<int:bookId>/addBook', FavoriteViewset.as_view({'post': 'create'})),
    path('favorite/<int:bookId>/deleteBook', FavoriteViewset.as_view({'delete': 'destroy'})),

    # categories
    path('author/list', ListAuthor.as_view()),
    path('publisher/list', ListPublisher.as_view()),
    path('category/list', ListCategory.as_view()),
]