from django.urls import path
from .views import  UserSignupView, UserLoginView, ProductAddView, ProductEditView, ProductDeleteView ,ProductDetailsView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView



urlpatterns = [
    path('signup/', UserSignupView.as_view(), name='signup'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('product/add/', ProductAddView.as_view(), name='add_product'),
    path('product/edit/<int:pk>/', ProductEditView.as_view(), name='update_product'),
    path('product/delete/<int:pk>/', ProductDeleteView.as_view(), name='delete_product'),
    path('product/details/', ProductDetailsView.as_view(), name='detail_product'),



]

