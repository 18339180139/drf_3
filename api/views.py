from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.
from api.models import Employee
from api.serializers import EmployeeSerializer, EmployeeDeSerializer


class EmployeeAPIViews(APIView):
    def get(self,request,*args,**kwargs):
        user_id = kwargs.get('id')
        if user_id:
            emp_obj = Employee.objects.get(pk=user_id)
            emp_ser = EmployeeSerializer(emp_obj).data
            print(emp_ser,type(emp_ser))
            return Response({
                "status":200,
                'message':"查询单个用户成功",
                "result":emp_ser
            })
        else :
            object_all = Employee.objects.all()
            all_data = EmployeeSerializer(object_all,many=True).data
            return Response({
                "status":200,
                "message":"查询所有用户成功",
                "results":all_data,
            })
    def post(self,request,*args,**kwargs):
        user_data = request.data
        print(user_data)
        if not isinstance(user_data,dict) or user_data == {}:
            return Response({
                "status":status.HTTP_400_BAD_REQUEST,
                "message":"请求数据格式有误"
            })
        serializer = EmployeeDeSerializer(data=user_data)
        if serializer.is_valid():
            emp_obj = serializer.save()
            return Response({
                "status":status.HTTP_200_OK,
                "message":"用户保存成功",
                "result":EmployeeSerializer(emp_obj).data
            })
        return Response({
            "status":status.HTTP_400_BAD_REQUEST,
            "message":serializer.errors
        })