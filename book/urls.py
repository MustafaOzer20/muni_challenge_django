from django.urls import path
from .views import BookViewset, CommentViewset


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

    #comment
    path('book/<int:bookId>/addComment', CommentViewset.as_view({'post': 'create'})),
    path('comment/delete/<int:pk>', CommentViewset.as_view({'delete': 'destroy'})),
]