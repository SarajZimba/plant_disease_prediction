# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from api.serializers.image import ImageSerializer
import tensorflow as tf
import numpy as np 
from io import BytesIO
from solution.models import Solution

class UploadImageView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            sent_image = serializer.validated_data['image']
            image_stream = BytesIO(sent_image.read())
            model = tf.keras.models.load_model('trained_model.keras')
            image = tf.keras.preprocessing.image.load_img(image_stream, target_size=(128, 128))
            input_arr = tf.keras.preprocessing.image.img_to_array(image)
            input_arr = np.array([input_arr]) #Covert Single Image to batch
            prediction = model.predict(input_arr)
            result_index = np.argmax(prediction)

            print(result_index)

            new_result_index = result_index + 1

            solution = Solution.objects.get(pk=new_result_index)


            class_name = ['Apple___Apple_scab', 'Apple___Black_rot', 'Apple___Cedar_apple_rust', 'Apple___healthy',
                        'Blueberry___healthy', 'Cherry_(including_sour)___Powdery_mildew', 
                        'Cherry_(including_sour)___healthy', 'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot', 
                        'Corn_(maize)___Common_rust_', 'Corn_(maize)___Northern_Leaf_Blight', 'Corn_(maize)___healthy', 
                        'Grape___Black_rot', 'Grape___Esca_(Black_Measles)', 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)', 
                        'Grape___healthy', 'Orange___Haunglongbing_(Citrus_greening)', 'Peach___Bacterial_spot',
                        'Peach___healthy', 'Pepper,_bell___Bacterial_spot', 'Pepper,_bell___healthy', 
                        'Potato___Early_blight', 'Potato___Late_blight', 'Potato___healthy', 
                        'Raspberry___healthy', 'Soybean___healthy', 'Squash___Powdery_mildew', 
                        'Strawberry___Leaf_scorch', 'Strawberry___healthy', 'Tomato___Bacterial_spot', 
                        'Tomato___Early_blight', 'Tomato___Late_blight', 'Tomato___Leaf_Mold', 
                        'Tomato___Septoria_leaf_spot', 'Tomato___Spider_mites Two-spotted_spider_mite', 
                        'Tomato___Target_Spot', 'Tomato___Tomato_Yellow_Leaf_Curl_Virus', 'Tomato___Tomato_mosaic_virus',
                        'Tomato___healthy']
            
            message = {
                "name" : solution.disease_name,
                "cause": solution.cause,
                "solution" : solution.solution
            }

            return Response({'plant_disease': message})
        

        else:
            return Response(serializer.errors, status=400)
