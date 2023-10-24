from django.shortcuts import render
import requests
import openai
import firebase_admin
from firebase_admin import credentials, firestore
from firebase_admin import storage
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

cred = credentials.Certificate('firebase-adminsdk.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

class GetStoredResponseView(APIView):
    def get(self, request, *args, **kwargs):
        docId = request.query_params.get('docId')
        if not docId:
            return Response({'error': 'docId is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            doc = db.collection('responses').document(docId).get()
            if not doc.exists:
                return Response({'error': 'Document not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'success': True, 'openAIResponse': doc.to_dict()})

# TODO: Implement a PDF processor to pass text into OpenAI
class StoreOpenAIResponseView(APIView):
    def post(self, request):
        data = request.data
        if not data or not data.get('question') or not data.get('openAIResponse') or not data.get('conversation_history'):
            return Response({'error': 'Question, openAIResponse, and conversation_history are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            doc_ref = db.collection('responses').add(data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'success': True, 'docId': doc_ref[1].id})
         
class UploadFileView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file_obj = request.data['file']
        file_name = default_storage.save(file_obj.name, ContentFile(file_obj.read()))
        blob = storage.bucket().blob(file_name)
        blob.upload_from_filename(file_name)
        file_url = blob.public_url

        return Response({'success': True, 'fileUrl': file_url, 'message': 'File uploaded successfully.'}, status=status.HTTP_200_OK)


class ProcessFileContentView(APIView):
    def post(self, request):
        file_url = request.data.get('fileUrl')
        action = request.data.get('action')

        if not file_url or not action:
            return Response({'error': 'File URL and action are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            file_content = requests.get(file_url).text
            response = openai.Completion.create(engine="gpt-4.0-turbo", prompt=file_content, max_tokens=4096)
            processed_content = response['choices'][0]['text'].strip()
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'success': True, 'processedContent': processed_content, 'model': 'gpt-4.0-turbo'})

