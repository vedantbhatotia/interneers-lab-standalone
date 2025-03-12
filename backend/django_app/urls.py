# from django.contrib import admin
# from django.urls import path
# from django.http import HttpResponse
# from django.http import JsonResponse

# def hello_world(request):
#     name = request.GET.get("name","World")
#     return JsonResponse("updated hello world function",name)

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('hello/', hello_world),
# ]

from django.contrib import admin
from django.urls import path,include
from django.http import JsonResponse

def hello_world(request):
    name = request.GET.get("name", "World")
    return JsonResponse({"message": f"updated hello world function, {name}"})



urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', hello_world),
    path('api/',include('product.urls'))
]
