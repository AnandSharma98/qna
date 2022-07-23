from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register', views.registerPage, name='register'),
    path('login', views.loginPage, name='login'),
    path('logout', views.logoutPage, name='logout'),
    path('', views.homePage, name='index'),
    path('new-question', views.newQuestionPage, name='new-question'),
    path('question/<int:id>', views.questionPage, name='question'),
    path('reply', views.replyPage, name='reply'),
    path("search/", views.searchResults, name="search_results"),
    path("like/<int:pk>", views.LikeView, name="like_question"),
    path("responselike/", views.LikeViewResponse, name="like_response"),
    path('profile/', views.profile, name='users-profile'),
    path('password-reset/', views.ResetPasswordView.as_view(), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
         name='password_reset_confirm'),
         # uidb64: The user’s id encoded in base 64.
         # token: Password recovery token to check that the password is valid.
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), # inbuilt  views used
         name='password_reset_complete'),     
         # https://stackoverflow.com/questions/5931461/django-registration-templates  
]