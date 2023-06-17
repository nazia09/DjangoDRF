from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.exceptions import ObjectDoesNotExist
from .serializers import UserSerializer
from .models import Product
from .serializers import ProductSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse
from drf_yasg.utils import swagger_auto_schema





class UserSignupView(APIView):
    """
       API endpoint for user signup.
    """

    @swagger_auto_schema(request_body=UserSerializer)
    def post(self, request):
        """
                Create a new user.

                ---
                parameters:
                  - name: username
                    type: string
                    required: true
                    description: The username of the user.
                  - name: password
                    type: string
                    required: true
                    description: The password of the user.
                  - name: country
                    type: string
                    required: true
                    description: The country of the user.
                  - name: city
                    type: string
                    required: true
                    description: The city of the user.
                  - name: postal_code
                    type: string
                    required: true
                    description: The postal code of the user.
                  - name: address
                    type: string
                    required: true
                    description: The address of the user.

                responses:
                  '201':
                    description: User created successfully.
                  '400':
                    description: Bad request. Invalid input data.
        """

        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    """
       API endpoint for user login.
    """

    @swagger_auto_schema(request_body=UserSerializer)
    def post(self, request):
        """
        Authenticate user and generate tokens.

        ---
        requestBody:
            content:
                application/json:
                    schema:
                        type: object
                        properties:
                            username:
                                type: string
                            password:
                                type: string
                        required:
                            - username
                            - password
            required: true
        responses:
            200:
                description: User authenticated successfully.
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                username:
                                    type: string
                                access_token:
                                    type: string
                                refresh_token:
                                    type: string
                                country:
                                    type: string
                                city:
                                    type: string
                                postal_code:
                                    type: string
                                address:
                                    type: string
            401:
                description: Invalid credentials.

        """
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            serializer = UserSerializer(user)
            response_data = {
                'username': user.username,
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
                'country': user.country,
                'city': user.city,
                'postal_code': user.postal_code,
                'address': user.address,
            }
            return Response(response_data, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class ProductDetailsView(APIView):
    """
     API endpoint to get details of all products.
     """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema()
    def get(self, request):
        """
                Retrieve details of all products.
        """
        try:
            product_detail = Product.objects.all()
            serializer = ProductSerializer(product_detail, many=True)
            json_data = JSONRenderer().render(serializer.data)
            return HttpResponse(json_data, content_type='application/json')
        except ObjectDoesNotExist:
            return Response("No product data found.", status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class ProductAddView(APIView):
    """
    API endpoint to add a new product.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=ProductSerializer)
    def post(self, request):
        """
                Create a new product.
        """

        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductEditView(APIView):
    """
    API endpoint to edit a product.
    """

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=ProductSerializer)
    def put(self, request, pk):


        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductDeleteView(APIView):
    """
       API endpoint to delete a product
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema()
    def delete(self, request, pk):
        """
               Delete a product

               Parameters:
                pk: The primary key of the product to delete.

               Returns:
                204: Product deleted successfully
                404: If the product with the given primary key does not exist
        """

        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        product.delete()
        return Response({'message': 'Product deleted'},status=status.HTTP_204_NO_CONTENT)


