from django.shortcuts import render
from django.http import JsonResponse, Http404
from rest_framework.response import Response
from .models import Client, Movie, Reservation
from rest_framework.decorators import api_view,  permission_classes,authentication_classes
from .serializers import ClientSerializer, MovieSerializer, ReservationSerializer
from rest_framework import status, filters, generics, mixins,viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly,AllowAny,IsAuthenticated
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import BasicAuthentication, TokenAuthentication,SessionAuthentication
from .pagination import TicketPagination
from rest_framework.filters import SearchFilter
from django.contrib.auth.models import User 
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .permissions import Check_API_KEY_Auth
class ExampleAuthentication(BaseAuthentication):
    def authenticate(self, request):
        username = request.META.get('X_USERNAME')
        if not username : 
            return None 
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise AuthenticationFailed('User not found')  

        return (user, None)  

class ExampleView(APIView):
    permission_classes = [Check_API_KEY_Auth]

    # Logic you want .....
    # GET, POST, PUT, PATCH, DELETE 
    pass 

@api_view(['GET'])
@permission_classes((Check_API_KEY_Auth,))
def example_view(request):
    # Logic 
    pass 


# without RF and no model query FBV 
def no_rest_no_model(request):
    clients = [
        {
            'id': 1 ,
            'name':'omar' ,
            'phone': 111111 ,
        },
        {
            'id': 2 ,
            'name':'Muhammed' ,
            'phone': 22222 ,
        },

    ]
    return JsonResponse(clients,safe=False)
    # this is the best way when your data is static 


# model data default django without rest 
def no_rest_from_model(request):
    data = Client.objects.all()
    response = {
        'clients':list(data.values('id','name','phone')),
    }
    return JsonResponse(response, safe=False)

# list ==> GET 
# create ==> POST
# Updata ==> PUT
# Delete, destroy ==> DELETE
# _______________________________________

# Function Based Views
# GET,POST 
@api_view(['GET','POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def FBV_List(request):
    #GET
    if request.method == 'GET':
        clients = Client.objects.all()
        serializer = ClientSerializer(clients, many=True)
        return Response(serializer.data)
    #POST
    elif request.method == 'POST':
        serializer = ClientSerializer(data=request.data) # Create
        print('Not valid')
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# GET, PUT, DELETE
@api_view(['GET','PUT','DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def FBV_pk(request, pk):
    try:
      client = Client.objects.get(pk = pk) # to access data with pk queryset 
    except Client.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
      
    # GET
    if request.method == 'GET':
        serializer = ClientSerializer(client)
        return Response(serializer.data)
    # PUT
    elif request.method == 'PUT':
        serializer = ClientSerializer( client,data=request.data) # Update Must acesss data  
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # DELETE 
    elif request.method == 'DELETE':
        client.delete()
        return Response( status=status.HTTP_204_NO_CONTENT)


# Class Based Views 
# List and Create (GET,POST)

class ListCBV(APIView):
    def get(self,request) :
        clients = Client.objects.all()
        serializer = ClientSerializer(clients,many=True)
        return Response(serializer.data)
    
    def post(self,request) :
        serializer = ClientSerializer(data=request.data) # Create
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(f'Invalid data: {serializer.errors}')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

# Class Based Views 
# GET, PUT, DELETE
# OOP
class CbvPk(APIView):
    
    def get_object(self,pk):
        try:
            return Client.objects.get(pk=pk)
        except Client.DoesNotExist:
            raise Http404 
        
    def get(self,request,pk):
        client= self.get_object(pk) # access object in self 
        serializer = ClientSerializer(client) # becuse to accec one client no many
        return Response(serializer.data) 
    
    def put(self,request,pk):
        client= self.get_object(pk) # access object in self 
        serializer = ClientSerializer(client,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        client = self.get_object(pk)
        client.delete()
        return Response( status=status.HTTP_204_NO_CONTENT)
    

# Mixins
# Mixins List 

class MixinsList(mixins.ListModelMixin, 
                 mixins.CreateModelMixin,
                 generics.GenericAPIView
                 ):
    queryset = Client.objects.all()
    serializer_class =  ClientSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self,request):
        return self.list(request)
        
    def post(self,request):
        return self.create(request)


class MixinsPk(mixins.RetrieveModelMixin,
               mixins.UpdateModelMixin,
               mixins.DestroyModelMixin,
               generics.GenericAPIView):
    
    queryset = Client.objects.all()
    serializer_class =  ClientSerializer
    
    def get(self,request,pk):
        return self.retrieve(request)
        
    def put(self,request,pk):
        return self.update(request)
    
    def delete(self,request,pk):
        return self.destroy(request)
    

# Generics
# GET,POST 

class GenericsList(generics.ListCreateAPIView):
    queryset = Client.objects.all()
    serializer_class =  ClientSerializer
    pagination_class = TicketPagination
    filter_backends = [SearchFilter]
    search_fields = ['name', 'phone']
    


class GenericsPK(generics.RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all()
    serializer_class =  ClientSerializer


# viewsets
class ViewSetsALl_Client(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class =  ClientSerializer

class ViewSetsALl_Movie(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class =  MovieSerializer

class ViewSetsALl_Reservation(viewsets.ModelViewSet):
    # how to use select_related
    queryset = Reservation.objects.select_related('client')
    serializer_class =  ReservationSerializer

# find Movie
@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def find_movie(request):
    movies = Movie.objects.filter(
        movie = request.data['movie'],
        hall = request.data['hall']
    )
    serializer = MovieSerializer(movies, many=True)

    return Response(serializer.data)

# Create new reservation 
@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def create_reservation(request):
    # 1. Get the movie object from the database
    movie = Movie.objects.get(
        hall = request.data['hall'],
        movie = request.data['movie'],
    )
    # 2. Create a new client object and save it to the database
    client = Client()
    client.name = request.data['name']
    client.phone = request.data['phone']
    client.save()

    # 3. Create a new reservation object and save it to the database
    reservation = Reservation()
    reservation.client = client
    reservation.movie = movie
    reservation.save()
    # 4. Return a response indicating the reservation was created successfully
    return Response(status=status.HTTP_201_CREATED)