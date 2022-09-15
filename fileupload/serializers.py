from rest_framework import serializers

from .models import *


class FileListSerializer(serializers.Serializer):
    files = serializers.ListField(
        child = serializers.FileField(max_length = 1000000, allow_empty_file=False, use_url=False),
        write_only=True
    )    

    folder_id = serializers.UUIDField(read_only=True)
    
    def create(self, validated_data):
        folder = Folder.objects.create()
        files = validated_data.get('files')
        for file in files:
            file_obj = File.objects.create(folder=folder, file=file)
            
        return {'folder_id': folder.uid}