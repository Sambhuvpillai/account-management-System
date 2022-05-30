from django.urls import path,include
from .import views


urlpatterns = [
    path('',views.index,name='index'),
    path('register',views.register,name='register'),
    path('sign_up',views.sign_up,name='sign_up'),
    path('load_loginpage',views.load_loginpage,name='load_loginpage'),
    path('userlogin',views.userlogin,name='userlogin'),
    path('load_admin_home',views.load_admin_home,name='load_admin_home'),
    path('load_user_home',views.load_user_home,name='load_user_home'),
    path('emp_details/<int:pk>',views.emp_details,name='emp_details'),
    path('user_profile',views.user_profile,name='user_profile'),
    path('editpage',views.editpage,name='editpage'),
    path('edit_profile',views.edit_profile,name='edit_profile'),
    path('logout',views.logout,name='logout'),
    path('delete_user/<int:pk>',views.delete_user,name='delete_user'),
    path('apply_leave',views.apply_leave,name='apply_leave'),
    path('submit_leave',views.submit_leave,name='submit_leave'),
    
    
    path('load_leave_requests',views.load_leave_requests,name='load_leave_requests'),
    path('aprove_leave_req',views.aprove_leave_req,name='aprove_leave_req'),
    path('aprove_leave/<int:pk>',views.aprove_leave,name='aprove_leave'),
    path('applied_leaves',views.applied_leaves,name='applied_leaves'),
    path('emp_aproved_leaves',views.emp_aproved_leaves,name='emp_aproved_leaves'),
    path('delete_leave/<int:pk>',views.delete_leave,name='delete_leave'),
    
    
]