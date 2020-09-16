from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Book
from app.serializers import BookModelSerializer, BookModelDeSerializer, BookModelSerializerV2


class BookAPIView(APIView):
    def get(self,request,*args,**kwargs):
        book_id = kwargs.get("id")
        if book_id:
            book_obj = Book.objects.get(pk = book_id)
            data = BookModelSerializer(book_obj).data
            return Response({
                "status":200,
                "message":"查询单个图书成功",
                "results": data
            })
        else :
            object_all = Book.objects.all()
            book_list = BookModelSerializer(object_all,many = True).data
            return Response({
                "status":200,
                "message" : "查询所有成功",
                "results": book_list
            })
    def post(self,request,*args,**kwargs):
        data = request.data
        serializer = BookModelDeSerializer(data = data)
        serializer.is_valid(raise_exception=True)
        book_obj = serializer.save()
        return Response({
            "status":201,
            "message":"创建图书成功",
            "results":BookModelSerializer(book_obj).data
        })

class BookAPIViewV2(APIView):
    def get(self,request,*args,**kwargs):
        book_id = kwargs.get("id")
        if book_id:
            book_obj = Book.objects.get(pk=book_id,is_delete=False)
            data = BookModelSerializerV2(book_obj).data
            return Response({
                "status" : 200,
                "message" : "查询单个图书成功",
                "results" : data
            })

        else:
            objects_all = Book.objects.filter(is_delete=False)
            book_list = BookModelSerializerV2(objects_all,many=True).data
            return Response({
                "status":200,
                "message":"查询所有成功",
                "results":book_list
            })

    def post(self,request,*args,**kwargs):
        request_data = request.data
        #群体增加 book_list=[{}{}{}],
        if isinstance(request_data,dict):
            many = False
        elif isinstance(request_data, list):
            many = True
        else:
            return Response({
                "status": 400,
                "message": "数据格式有误"
            })

        book_ser = BookModelSerializerV2(data=request_data, many=many)
        book_ser.is_valid(raise_exception=True)
        save = book_ser.save()

        return Response({
            "status": 200,
            "message": '添加图书成功',
            "results": BookModelSerializerV2(save, many=many).data
        })

    def delete(self, request, *args, **kwargs):
        book_id = kwargs.get("id")

        if book_id:
            ids = [book_id]
        else:
            ids = request.data.get("ids")
        response = Book.objects.filter(pk__in=ids, is_delete=False).update(is_delete=True)
        if response:
            return Response({
                "status": 200,
                "message": "删除成功"
            })
        return Response({
            "status": 400,
            "message": "删除失败或者图书不存在",
        })

    def put(self, request, *args, **kwargs):
        request_data = request.data
        book_id = kwargs.get("id")

        try:
            book_obj = Book.objects.get(pk=book_id)
        except:
            return Response({
                "status": 400,
                "message": "图书不存在",
            })

        book_ser = BookModelSerializerV2(data=request_data, instance=book_obj)
        book_ser.is_valid(raise_exception=True)
        save = book_ser.save()

        return Response({
            "status": 200,
            "message": "更新成功",
            "results": BookModelSerializerV2(save).data
        })

    def patch(self, request, *args, **kwargs):
        request_data = request.data
        book_id = kwargs.get("id")

        try:
            book_obj = Book.objects.get(pk=book_id)
        except:
            return Response({
                "status": 400,
                "message": "图书不存在",
            })

        book_ser = BookModelSerializerV2(data=request_data, instance=book_obj, partial=True)
        book_ser.is_valid(raise_exception=True)
        save = book_ser.save()

        return Response({
            "status": 200,
            "message": "更新成功",
            "results": BookModelSerializerV2(save).data
        })

