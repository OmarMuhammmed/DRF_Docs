from django.contrib import admin
from django.urls import path,include
from tickets import views
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register('clients',views.ViewSetsALl_Client)
router.register('movies',views.ViewSetsALl_Movie)
router.register('reservation',views.ViewSetsALl_Reservation)
from rest_framework.authtoken.views import obtain_auth_token
urlpatterns = [
    path('admin/', admin.site.urls),
    # 1 
    path('django/jsonresponsenomodel/',views.no_rest_no_model),
    # 2 
    path('django/jsonresponsefrommodel/',views.no_rest_from_model),
    # 3 
    path('rest/fbv/', views.FBV_List),
    # 3.1
    path('rest/fbv/<int:pk>', views.FBV_pk),
    # 4 
    path('rest/cbv/', views.ListCBV.as_view()),
    # 4.1
    path('rest/cbv/<int:pk>/', views.CbvPk.as_view()),
    # 5
    path('rest/mixins/', views.MixinsList.as_view()),
    # 5.1
    path('rest/mixins/<int:pk>/', views.MixinsPk.as_view()),
    # 6 
    path('rest/generics/', views.GenericsList.as_view()),
    # 6.1
    path('rest/generics/<int:pk>/', views.GenericsPK.as_view()),
    # 7
    path('rest/viewsets/', include(router.urls)),

    path('fbv/findmovie/',views.find_movie),

    path('fbv/createreservation/',views.create_reservation),
    
    path('api-auth/', include('rest_framework.urls')),
    # Api-Token auth 
    path('api-token-auth/',obtain_auth_token)

]
