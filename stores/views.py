# from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Store
from .serializers import StoreSerializer
from django.contrib.gis.db.models.functions import Distance


class ListStores(APIView):

    def get(self, request, *args, **kwargs):
        if not request.user.is_anonymous:
            ref_location = request.user.profile.location
            stores = Store.objects.annotate(distance=Distance("location", ref_location)).order_by("distance")
            serializer = StoreSerializer(stores, many=True)
            return Response(serializer.data)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
