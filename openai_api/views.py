from django.shortcuts import render

# Create your views here.
import openai
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

openai.api_key = 'your-openai-api-key'

class GenerateResponseView(APIView):
    def post(self, request):
        prompt = request.data.get('prompt')
        if not prompt:
            return Response({'error': 'Prompt is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            response = openai.Completion.create(engine="davinci", prompt=prompt, max_tokens=150)
            text = response['choices'][0]['text'].strip()
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'response': text})
