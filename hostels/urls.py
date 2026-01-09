from django.urls import path
from . import views

urlpatterns = [
    # Profile/redirect
    path('accounts/profile/', views.profile, name='profile'),
    
    # Student URLs
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('student/request-hostel/', views.request_hostel, name='request_hostel'),
    
    # AJAX endpoints
    path('api/rooms/', views.get_available_rooms, name='get_available_rooms'),
    
    # Admin URLs
    path('admin/requests/', views.admin_requests, name='admin_requests'),
    path('admin/approve/<int:request_id>/', views.approve_request, name='approve_request'),
    path('admin/reject/<int:request_id>/', views.reject_request, name='reject_request'),
    path('admin/allocations/', views.allocation_overview, name='allocation_overview'),
]
