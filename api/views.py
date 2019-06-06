from rest_framework import generics, permissions, status
from rest_framework.response import Response


from api.serializers import CurrencySerializer


class CreateCurrencyReportView(generics.CreateAPIView):
    serializer_class = CurrencySerializer
    permission_classes = (permissions.AllowAny,)


    def post(self, request, *args, **kwargs):
        serializer = CurrencySerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(
                    data=serializer.data,
                    status=status.HTTP_201_CREATED
                    )
        else:
            return Response(
                    data=serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                    )


