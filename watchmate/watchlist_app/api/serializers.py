from rest_framework import serializers
from watchlist_app.models import WatchList, StreamPlatform, Reviews


class ReviewSerializer(serializers.ModelSerializer):
    
    review_user = serializers.StringRelatedField(read_only = True)
    watchlist = serializers.StringRelatedField(read_only = True)
    
    class Meta:
        model = Reviews
        fields = '__all__'

    def rating_validate(self, value):
        if value > 5 or value < 1 :
            raise serializers.ValidationError('Rating Should be Smaller Than or Equal to 5 or Bigger Than or Equal to 1')
        return value

class WatchListSerializer(serializers.ModelSerializer):

    reviews = ReviewSerializer(many = True, read_only = True)
            
    class Meta:
        model = WatchList
        fields = '__all__'
        
class StreamPlatformSerializer(serializers.ModelSerializer):
    
    watchlist = WatchListSerializer(many = True, read_only = True)
    #watchlist =  serializers.StringRelatedField(many = True, read_only = True)
    
    # url = serializers.HyperlinkedIdentityField(
    #     view_name='platform',  # this MUST match urls.py
    #     lookup_field='id'
    # )
    class Meta:
         model = StreamPlatform
         fields = '__all__'
         include = ['id']








# class MovieSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only = True)
#     name = serializers.CharField()
#     about = serializers.CharField()
#     active = serializers.BooleanField()
    
#     def create(self, validated_data):
#         return Movie.objects.create(**validated_data)
    
#     def update(self, instance, validated_data):
#         instance.name = validated_data.get('name', instance.name)
#         instance.about = validated_data.get('about', instance.about)
#         instance.active = validated_data.get('active', instance.active)
#         instance.save()
#         return instance
    
#     def validate_name(self, value):
        
#         if len(value) < 2:
#             raise serializers.ValidationError("Name is too Short")
#         else:
#             return value
    
#     def validate(self, data):
    
#         if data['name'] == data['about']:
#             raise serializers.ValidationError("Name and Discription Can't have the same values")
#         else:
#             return data
        