from django.urls import  path
from . import views

urlpatterns = [
    # Autenticacion
    # path('sessionauth/', views.login_view_session_auth, name='sessionauth'),
    path('test_orm', views.db_orm_test, name='test_orm')
]