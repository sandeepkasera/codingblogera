
from django.contrib import admin
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static



from .views import (
    post_detail_view,
    post_delete_view,
    post_list_view,
    post_create_view,
    newsFeed
  
  
)
urlpatterns = [


    path('home/',newsFeed),

    path('s/',post_list_view),
    path('create/',post_create_view),
    path('<int:post_id>/',post_detail_view),
    path('<int:post_id>/delete/',post_delete_view),

    ]
if settings.DEBUG:
    urlpatterns +=  static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)

    