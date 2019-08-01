from django.urls import path
from . import views
# Определите и зарегистрируйте конвертер для определения даты в урлах и наоборот урла по датам


urlpatterns = [
    # Определите схему урлов с привязкой к отображениям .views.file_list и .views.file_content
    path('', views.file_list,  name='file_list'),
    path('<date>/', views.file_list, name='file_list'),
    path('file/<name>/', views.file_content, name='file_content'),
]
