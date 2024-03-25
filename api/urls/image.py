# urls.py
from django.urls import path
from api.views.image import UploadImageView

urlpatterns = [
    path('upload_image/', UploadImageView.as_view(), name='upload_image'),
]
