from django.urls import path
from .views import user_list,htmx_list,user_search
from .api import user_list_api

urlpatterns = [
    path("", user_list),
    path("htmx/", htmx_list),
    path("search/", user_search),
    path("api/", user_list_api),
]