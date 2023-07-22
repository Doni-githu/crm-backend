from django.urls import path
from .views import *
from django.urls import path
from rest_framework_simplejwt import views as jwt_views

app_name = 'app'


urlpatterns = [
    path("student/", student_list),
    path("student/<int:id>", student_detail),

    path("technology/", technology_list),
    path("technology/<int:id>", technology_detail),

    path("davomat/", davomat_list),
    path("davomat/<int:id>", davomat_detail),

    path("profession/", profession_list),
    path("profession/<int:id>", profession_detail),

    path("groups/", groups_list),
    path("groups/<int:id>", groups_detail),

    path("teacher/", teacher_list),
    path("teacher/<int:id>", teacher_detail),

    path('administrator/', admin_list),
    path('administrator/<int:id>', admin_detail),


    path('payment/', payment_list),
    path('payment/<int:id>/', payment_one),
        
    path('accounts/register', RegistrationView.as_view(), name='register'),
    path('accounts/login', LoginView.as_view(), name='login'),
    path('accounts/logout', LogoutView.as_view(), name='logout'),
    path('accounts/change-password', ChangePasswordView.as_view(), name='register'),
    path('accounts/user/<str:token>', get_user, name='token_refresh'),
    path('account/<int:id>/<str:role>', getUser),
    
    
    path("days/", week_list)
]