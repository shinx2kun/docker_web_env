from django.shortcuts import render
# from rest_framework import generics
from .models import ProcedureManual
from .serializers import ProcedureManualSerializer

# Create your views here.
# class ListProcedureManual(generics.ListAPIView):
#     queryset = ProcedureManual.objects.all()
#     serializer_class = ProcedureManualSerializer

# class DetailProcedureManual(generics.RetrieveAPIView):
#     queryset = ProcedureManual.objects.all()
#     serializer_class = ProcedureManualSerializer