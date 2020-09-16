from rest_framework import exceptions
from rest_framework.serializers import ModelSerializer

from api.models import Book, Press



class BookModelSerializer(ModelSerializer):
    class Meta:
        model = Book
        fields = ("book_name","price","publish","authors","press_address","author_list")
class PressModelSerializer(ModelSerializer):
    class Meta:
        model = Press
        fields = ("press_name","address","img")
class BookModelDeSerializer(ModelSerializer):

    class Meta:
        model = Book
        fields = ("book_name","price","publish","authors")
        extra_kwargs = {
            "book_name":{
                "max_length":18,
                "min_length":2,
                "error_messages":{
                    "max_length":"你妈喊你吃饭不费劲吗？写短点",
                    "min_length":"你真短，缺你那点墨水吗？写长点"
                }
            },
            "price":{
                "required":True,
                "decimal_places":2,
            }
        }
        def validate(self,attrs):
            name = attrs.get("book_name")
            book = Book.objects.filter(book_name=name)
            if len(book)>0:
                raise exceptions.ValidationError("图书名已存在")
        def validate_price(self,obj):
            print(type(obj),"1111")
            if obj > 1000:
                raise  exceptions.ValidationError("价格最多不能超过1000")
            return obj
class BookModelSerializerV2(ModelSerializer):
    class Meta:
        model = Book
        fields = ("book_name","price","pic","publish","authors")
        extra_kwargs = {
            "book_name": {
                "max_length": 18,
                "min_length": 2,
            },
            "publish": {
                "write_only": True,
            },
            "authors": {
                "write_only": True,
            },
            "pic": {
                "read_only": True
            }
        }


    def validate(self, attrs):
        name = attrs.get("book_name")
        book = Book.objects.filter(book_name=name)
        if len(book) > 0:
            raise exceptions.ValidationError('图书名已存在')

        return attrs

    def validate_price(self, obj):
        if obj > 1000:
            raise exceptions.ValidationError("价格最多不能超过10000")
        return obj

    def update(self, instance, validated_data):
        book_name = validated_data.get("book_name")
        instance.book_name = book_name
        instance.save()
        return instance