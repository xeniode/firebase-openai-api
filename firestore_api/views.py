from django.shortcuts import render

# Create your views here.
import firebase_admin
from firebase_admin import credentials, firestore
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

cred = credentials.Certificate('firebase-adminsdk.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

class StoreResponseView(APIView):
    def post(self, request):
        data = request.data
        if not data or not data.get('prompt') or not data.get('response'):
            return Response({'error': 'Both prompt and response are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            doc_ref = db.collection('responses').add(data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'success': True, 'doc_id': doc_ref[1].id})
