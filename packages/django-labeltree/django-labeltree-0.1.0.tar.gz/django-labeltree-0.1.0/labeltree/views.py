from django.http import JsonResponse

# Create your views here.

def list(request):

	return JsonResponse({"status": "OK"})
