# from django.shortcuts import render, get_object_or_404
# from rest_framework.views import APIView
# from rest_framework.generics import GenericAPIView
# from rest_framework.response import Response
# from rest_framework.decorators import api_view
# from rest_framework import status
from watchlist_app.models import WatchList, StreamPlatform, Reviews
from watchlist_app.api.serializers import WatchListSerializer, StreamPlatformSerializer, ReviewSerializer
from rest_framework import generics, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from watchlist_app.api.permissions import IsAdminOrReadOnly, ReviewUserOrReadOnly



class ReviewCreate(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReviewSerializer
    
    def get_queryset(self):
        return Reviews.objects.all()
        
    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        watchlist = WatchList.objects.get(pk = pk)
        
        review_user = self.request.user
        review_queryset = Reviews.objects.filter(watchlist=watchlist, review_user=review_user)
        
        if review_queryset.exists():
            raise ValidationError("You Have Already Reviewed This Movie")
        
        rating = serializer.validated_data['rating']
        
        if watchlist.number_rating == 0 :
            watchlist.avg_rating = rating
        else:
            watchlist.avg_rating = ((watchlist.avg_rating * watchlist.number_rating) + rating) / (watchlist.number_rating + 1)
            
        watchlist.number_rating = watchlist.number_rating + 1
        
        watchlist.save(update_fields=['avg_rating', 'number_rating'])
        
        print("Before Save:", watchlist.avg_rating, watchlist.number_rating)
        watchlist.save()
        print("After Save:", watchlist.avg_rating, watchlist.number_rating)

        
        serializer.save(watchlist=watchlist, review_user=review_user) 

class ReviewList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    #queryset = Reviews.objects.all()
    serializer_class = ReviewSerializer
    
    def get_queryset(self):
        pk = self.kwargs.get('pk')
        Review = Reviews.objects.filter(watchlist = pk)
        return Review
    
class ReviewDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reviews.objects.all()
    serializer_class = ReviewSerializer 
    permission_classes = [ReviewUserOrReadOnly]


class StreamPlatformV(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer

class WatchListV(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer




# class ReviewList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    
#     queryset = Reviews.objects.all()
#     serializer_class = ReviewSerializer
    
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
        
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
    

# class ReviewDetails(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    
#     queryset = Reviews.objects.all()
#     serializer_class = ReviewSerializer
    
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
    
#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)
    
#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)


    
    
# class StreamPlatformV(viewsets.ViewSet):
    
#     def list(self, request):
#         queryset = StreamPlatform.objects.all()
#         serializer = StreamPlatformSerializer(queryset, many = True, context={'request': request})
#         return Response(serializer.data)
    
#     def retrieve(self, request, pk=None):
#         queryset = StreamPlatform.objects.all()
#         watchlist = get_object_or_404(queryset, pk=pk)
#         serializer = StreamPlatformSerializer(watchlist)
#         return Response(serializer.data)
    
#     def create(self, request):
#         serializer = StreamPlatformSerializer(data = request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)

# class StreamPlatformAV(APIView):
    
#     def get(self, request):
#         platform = StreamPlatform.objects.all()
#         serializer = StreamPlatformSerializer(platform, many = True, context={'request' : request})
#         return Response(serializer.data)
    
#     def post(self, request):
#         serializer = StreamPlatformSerializer(data = request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
# class StreamPlatformDetailsAV(APIView):
    
#     def get(self, request, id):
#         platform = StreamPlatform.objects.get(id = id)
#         serializer = StreamPlatformSerializer(platform, context={'request' : request})
#         return Response(serializer.data)
    
#     def put(self, request, id):
#         platform = StreamPlatform.objects.get(id = id)
#         serializer = StreamPlatformSerializer(platform, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
#     def delete(self, request, id):
#         platform = StreamPlatform.objects.get(id = id)
#         platform.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
            
            

            
# class WatchListAV(APIView):
    
#     def get(self, request):
#         user = WatchList.objects.all()
#         serializer = WatchListSerializer(user, many=True)
#         return Response(serializer.data)
    
#     def post(self, request):
#         serializer = WatchListSerializer(data = request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class WatchDetailsAV(APIView):
    
#     def get(self, request, id):
#         try:
#             movie = WatchList.objects.get(id = id)
#         except:
#             return Response({'Error' : 'Movie Not Found'}, status=status.HTTP_404_NOT_FOUND)
#         serializer = WatchListSerializer(movie)
#         return Response(serializer.data)
    
#     def put(self, request, id):
#         movie = WatchList.objects.get(id = id)
#         serializer = WatchListSerializer(movie, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
#     def delete(self, request, id):
#         movie = WatchList.objects.get(id = id)
#         movie.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
    
    















# @api_view(['GET', 'POST'])
# def movie_list(request):
    
#     if request.method == 'GET':
#         movies = Movie.objects.all()
#         serializer = MovieSerializer(movies, many = True)
#         return Response(serializer.data)
    
#     if request.method == 'POST':
#         serializer = MovieSerializer(data=request.data)
        
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
        
#         else:
#             return Response(serializer.errors)

# @api_view(['GET', 'PUT', 'DELETE'])
# def film(request, id):
    
#     if request.method == 'GET':
#         try:
#             movie = Movie.objects.get(id = id)
#         except:
#             return Response({'Error' : 'Movie Not Found'}, status=status.HTTP_404_NOT_FOUND)
        
#         serializer = MovieSerializer(movie)
#         return Response(serializer.data)
    
#     if request.method == 'PUT':
#         movie = Movie.objects.get(id = id)
#         serializer = MovieSerializer(movie, data=request.data)
        
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
        
#         else:
#            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     if request.method == 'DELETE':
#         movie = Movie.objects.get(id = id)
#         movie.delete()
#         return Response(status = status.HTTP_204_NO_CONTENT)
    
    
    

