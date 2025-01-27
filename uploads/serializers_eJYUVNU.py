from rest_framework import serializers
from teachers.models import *
from datetime import datetime
from django.conf import settings

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model=Subject
        fields="__all__"

class RecordSerializer(serializers.ModelSerializer):
    subject=SubjectSerializer(read_only=True)
    subject_id= serializers.PrimaryKeyRelatedField(queryset=Subject.objects.all(), write_only=True, source="subject")
    author = serializers.SerializerMethodField()
    files = serializers.SerializerMethodField()

    def get_author(self, obj):
        return CustmoUserSerializer(obj.author).data if obj.author else None
    def get_files(self,obj):
      files = File.objects.filter(records_FK=obj)
      return [settings.SITE_URL + f'/api/files/{file.id}/' for file in files]
    def get_files_to_update(self,obj):
        files = File.objects.filter(records_FK=obj)
        return [  {'id':file.id, 'url': f'/api/files/{file.id}/'} for file in files ]
    def create(self, validated_data):
        if 'request' in self.context and self.context['request'].user.is_authenticated:
            validated_data['author'] = self.context['request'].user
        validated_data['time'] = datetime.now() 
        
        files_data = self.context['request'].FILES.getlist('files') 
        record = super().create(validated_data)
        
        for file_data in files_data:
           File.objects.create(records_FK_id=record.id, file=file_data)
        

        return record
    
    def update(self, instance, validated_data):
        if 'subject' in validated_data:
            subject_id = validated_data.pop('subject')
            instance.subject_id = subject_id
        
        files_data = self.context['request'].FILES.getlist('files')
        
        File.objects.filter(records_FK=instance).delete()


        for file_data in files_data:
            File.objects.create(records_FK_id=instance.id, file=file_data)
            
        validated_data['time'] = datetime.now()
        return super().update(instance, validated_data)
    
    class Meta:
        model=Record
        fields="__all__"


class FileSerializer(serializers.ModelSerializer):

     class Meta:
       model=File
       fields=['id','file']

class FeedbackSerializer(serializers.ModelSerializer):
    records_FK=RecordSerializer(read_only=True)
    records_FK_id= serializers.PrimaryKeyRelatedField(queryset=Record.objects.all(), write_only=True, source="records_FK")
    
    def create(self, validated_data):
        if 'request' in self.context and self.context['request'].user.is_authenticated:
            validated_data['moderator'] = self.context['request'].user
        validated_data['time'] = datetime.now() 
    
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data['time'] = datetime.now() 
        return super().update(instance, validated_data)
    
    class Meta:
        model=Feedback
        fields="__all__"


class ReviewSerializer(serializers.ModelSerializer):
    records_FK=RecordSerializer(read_only=True)
    records_FK_id= serializers.PrimaryKeyRelatedField(queryset=Record.objects.all(), write_only=True, source="records_FK")
    author = serializers.SerializerMethodField()

    def get_author(self, obj):
          return CustmoUserSerializer(obj.author).data if obj.author else None
    def create(self, validated_data): 
        if 'request' in self.context and self.context['request'].user.is_authenticated:
            validated_data['author'] = self.context['request'].user
        validated_data['time'] = datetime.now() 
        
        return super().create(validated_data)


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
    school = SchoolSerializer(read_only=True)

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