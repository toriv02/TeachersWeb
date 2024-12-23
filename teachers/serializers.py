from rest_framework import serializers

from teachers.models import *


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model=Subject
        fields="__all__"


class RecordSerializer(serializers.ModelSerializer):
    class Meta:
        model=Record
        fields="__all__"


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model=File
        fields="__all__"


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model=Feedback
        fields="__all__"


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model=Review
        fields="__all__"



class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Document
        fields="__all__"

class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model=School
        fields="__all__"


class CustmoUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustmoUser
        fields = ['username', 'email', 'password','fio','school']
        extra_kwargs = {
            'password': {'write_only': True}
        }


    def create(self, validated_data):


        user = CustmoUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password = validated_data['password'],
            fio=validated_data['fio'],
            school=validated_data['school'], # Присваиваем объект школы
        )
        return user