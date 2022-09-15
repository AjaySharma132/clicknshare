from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import cloudinary
import pyshorteners

shortner_obj = pyshorteners.Shortener()


from .serializers import *

class UploadFile(APIView):
    # upload file on drive
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            
            data = request.data
            serializer = FileListSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'success': True, 
                    'message': 'file uploaded successfully',
                    'folder_id': serializer.data.get('folder_id')
                })
            else:
                return Response({
                    'success': False, 
                    'message': 'something went wrong, please try again later',
                    'error': serializer.errors
                })
            
        except Exception as e:
            print(e)
            return Response({
                'success': False,
                'message': 'Something went wrong, please try again later',
            })
            

class FetchUrl(APIView):
    # get short url for uploaded files
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            folder_uid = request.GET.get('folder_id')
            if folder_uid:
                folder_name = request.GET.get('folder_name', folder_uid)
                download_url = cloudinary.utils.download_folder(f'media/{folder_uid}', use_original_filename=True, target_public_id=folder_name)
                shorten_url = shortner_obj.tinyurl.short(download_url)
            else:
                return Response({'success': False, 'message': 'folder_id query parameter missing'})
        except Exception as e:
            print(e)
            return Response({'success': False, 'message': 'Something went wrong, please try again later'})
        return Response({'success': True, 'url': shorten_url})
        