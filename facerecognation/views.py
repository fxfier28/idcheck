
from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.core import serializers
from django.conf import settings
import json
import face_recognition
import uuid
from PIL import Image, ImageDraw

@api_view(["GET","POST"])
def photoWithId(request, format=None):
    #return Response({"message": "Hello, world!"})
    if request.method=='POST':
        face=request.data['photo']
        req_tolerance=float(request.data['tolerance'])

        # Load an image with an unknown face
        unknown_image = face_recognition.load_image_file(face)

        # Find all the faces and face encodings in the unknown image
        face_locations = face_recognition.face_locations(unknown_image)
        face_encodings = face_recognition.face_encodings(unknown_image, face_locations)
        unknown_face = face_recognition.face_encodings(unknown_image)[0]
        unknown_face_id = face_recognition.face_encodings(unknown_image)[1]
        # Convert the image to a PIL-format image so that we can draw on top of it with the Pillow library
        # See http://pillow.readthedocs.io/ for more about PIL/Pillow
        pil_image = Image.fromarray(unknown_image)
        # Create a Pillow ImageDraw Draw instance to draw with
        draw = ImageDraw.Draw(pil_image)
        # Loop through each face found in the unknown image
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces([unknown_face], unknown_face_id,tolerance=req_tolerance)

            name = "Unknown"

            # Draw a box around the face using the Pillow module
            draw.rectangle(((left, top), (right, bottom)), outline=(0, 0, 255))

            # Draw a label with a name below the face
            #text_width, text_height = draw.textsize(name)
            draw.rectangle(((left, bottom), (right, bottom)), fill=(0, 0, 255), outline=(0, 0, 255))
            #draw.text((left + 6, bottom - text_height - 5), name, fill=(255, 255, 255, 255))
            face_image = unknown_image[top:bottom, left:right]
            face_pil = Image.fromarray(face_image)
            face_pil.save("face"+str(uuid.uuid4())+".jpg","JPEG")
        # Remove the drawing library from memory as per the Pillow docs
        del draw
        #pil_image.save("new_image.jpeg","JPEG")
        #print(matches)
        return JsonResponse({'result': bool(matches[0])},safe=False)
        #return Response({"message": "Got some data!", "data": face})
