from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db import models
from django.db.models import Q
from django.core.exceptions import ValidationError
from .models import (
    StudentProfile, Hostel, HostelRequest, Allocation, Room
)
from .forms import HostelRequestForm


def is_student(user):
    """Check if user is a student"""
    return hasattr(user, 'student_profile')


def is_admin(user):
    """Check if user is admin/staff"""
    return user.is_staff


@login_required
def profile(request):
    """Redirect to appropriate dashboard based on user role"""
    if is_admin(request.user):
        return redirect('allocation_overview')
    elif is_student(request.user):
        return redirect('student_dashboard')
    else:
        return redirect('home')


def student_dashboard(request):
    """Student dashboard showing request status and allocation"""
    if not request.user.is_authenticated:
        messages.info(request, "Please log in to view your dashboard.")
        return redirect('login')
    
    try:
        student = request.user.student_profile
    except StudentProfile.DoesNotExist:
        messages.error(request, "Student profile not found. Please contact administration.")
        return redirect('admin:index')
    
    # Get current request
    current_request = HostelRequest.objects.filter(
        student=student,
        status__in=['PENDING', 'APPROVED']
    ).first()
    
    # Get allocation if exists
    allocation = Allocation.objects.filter(student=student).first()
    
    context = {
        'student': student,
        'current_request': current_request,
        'allocation': allocation,
        'status_color': {
            'PENDING': 'warning',
            'APPROVED': 'success',
            'REJECTED': 'danger',
        }
    }
    
    return render(request, 'hostels/student_dashboard.html', context)


@login_required
def request_hostel(request):
    """Submit a hostel request"""
    try:
        student = request.user.student_profile
    except StudentProfile.DoesNotExist:
        messages.error(request, "Student profile not found. Please contact administration.")
        return redirect('admin:index')
    
    # Check if student already has an active request
    active_request = HostelRequest.objects.filter(
        student=student,
        status__in=['PENDING', 'APPROVED']
    ).first()
    
    if active_request:
        messages.warning(
            request,
            f"You already have an active request for {active_request.hostel.name} (Status: {active_request.get_status_display()})"
        )
        return redirect('student_dashboard')
    
    if request.method == 'POST':
        form = HostelRequestForm(request.POST, student=student)
        if form.is_valid():
            # Manually create the hostel request to avoid RelatedObjectDoesNotExist
            hostel_request = HostelRequest(
                student=student,
                hostel=form.cleaned_data['hostel'],
                preferred_capacity=form.cleaned_data['preferred_capacity'],
                preferred_room=form.cleaned_data.get('preferred_room'),
                note=form.cleaned_data.get('note', '')
            )
            
            try:
                hostel_request.full_clean()
                hostel_request.save()
                messages.success(
                    request,
                    "Hostel request submitted successfully! Status: Pending approval"
                )
                return redirect('student_dashboard')
            except ValidationError as e:
                messages.error(request, str(e))
                # Create a fresh form to avoid errors
                form = HostelRequestForm(student=student)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = HostelRequestForm(student=student)
    
    # Get available hostels for student
    available_hostels = Hostel.objects.filter(gender=student.gender)
    
    context = {
        'form': form,
        'available_hostels': available_hostels,
        'student': student,
    }
    
    return render(request, 'hostels/request_hostel.html', context)


@user_passes_test(is_admin)
def admin_requests(request):
    """Admin view for managing hostel requests"""
    # Get filters
    hostel_filter = request.GET.get('hostel', '')
    status_filter = request.GET.get('status', '')
    
    # Base queryset
    requests_qs = HostelRequest.objects.select_related(
        'student', 'student__user', 'hostel'
    ).order_by('-created_at')
    
    # Apply filters
    if hostel_filter:
        requests_qs = requests_qs.filter(hostel__id=hostel_filter)
    
    if status_filter:
        requests_qs = requests_qs.filter(status=status_filter)
    
    # Get all hostels for filter dropdown
    hostels = Hostel.objects.all()
    
    context = {
        'requests': requests_qs,
        'hostels': hostels,
        'status_choices': HostelRequest.STATUS_CHOICES,
        'selected_hostel': hostel_filter,
        'selected_status': status_filter,
        'total_requests': requests_qs.count(),
        'pending_count': requests_qs.filter(status='PENDING').count(),
        'approved_count': requests_qs.filter(status='APPROVED').count(),
        'rejected_count': requests_qs.filter(status='REJECTED').count(),
    }
    
    return render(request, 'hostels/admin_requests.html', context)


@user_passes_test(is_admin)
def approve_request(request, request_id):
    """Approve a hostel request and allocate a room"""
    hostel_request = get_object_or_404(HostelRequest, id=request_id)
    
    if request.method == 'POST':
        student = hostel_request.student
        
        # Find available room matching capacity
        available_room = Room.objects.filter(
            floor__hostel=hostel_request.hostel,
            capacity=hostel_request.preferred_capacity,
        ).exclude(allocations__student=student).filter(
            current_occupancy__lt=models.F('capacity')
        ).first()
        
        if not available_room:
            # Try to find any available room in the hostel
            available_room = Room.objects.filter(
                floor__hostel=hostel_request.hostel,
            ).exclude(allocations__student=student).filter(
                current_occupancy__lt=models.F('capacity')
            ).first()
        
        if available_room:
            # Create allocation
            allocation, created = Allocation.objects.get_or_create(
                student=student,
                defaults={'room': available_room}
            )
            
            if created:
                # Update room occupancy
                available_room.current_occupancy += 1
                available_room.save()
            else:
                # Update existing allocation
                old_room = allocation.room
                if old_room != available_room:
                    old_room.current_occupancy = max(0, old_room.current_occupancy - 1)
                    old_room.save()
                    
                    allocation.room = available_room
                    allocation.save()
                    
                    available_room.current_occupancy += 1
                    available_room.save()
            
            # Update request status
            hostel_request.status = 'APPROVED'
            hostel_request.save()
            
            messages.success(
                request,
                f"Request approved! {student.user.get_full_name()} allocated to {available_room}"
            )
        else:
            messages.error(
                request,
                f"No available rooms in {hostel_request.hostel.name} matching capacity {hostel_request.preferred_capacity}"
            )
        
        return redirect('admin_requests')
    
    return redirect('admin_requests')


@user_passes_test(is_admin)
def reject_request(request, request_id):
    """Reject a hostel request"""
    hostel_request = get_object_or_404(HostelRequest, id=request_id)
    
    if request.method == 'POST':
        hostel_request.status = 'REJECTED'
        hostel_request.save()
        
        messages.success(
            request,
            f"Request rejected for {hostel_request.student.user.get_full_name()}"
        )
    
    return redirect('admin_requests')


@user_passes_test(is_admin)
def allocation_overview(request):
    """Admin view for allocation overview"""
    # Get all allocations
    allocations = Allocation.objects.select_related(
        'student', 'student__user', 'room', 'room__floor', 'room__floor__hostel'
    ).order_by('-date_allocated')
    
    # Get hostel statistics
    hostels = Hostel.objects.all()
    hostel_stats = []
    
    for hostel in hostels:
        total_capacity = sum(
            room.capacity for room in Room.objects.filter(floor__hostel=hostel)
        )
        occupied = sum(
            room.current_occupancy for room in Room.objects.filter(floor__hostel=hostel)
        )
        available = total_capacity - occupied
        
        hostel_stats.append({
            'hostel': hostel,
            'total_capacity': total_capacity,
            'occupied': occupied,
            'available': available,
            'percentage': int((occupied / total_capacity * 100) if total_capacity > 0 else 0),
        })
    
    context = {
        'allocations': allocations,
        'hostel_stats': hostel_stats,
        'total_allocations': allocations.count(),
    }
    
    return render(request, 'hostels/allocation_overview.html', context)


@login_required
def get_available_rooms(request):
    """AJAX endpoint to get available rooms for a hostel and capacity"""
    import json
    from django.http import JsonResponse
    
    hostel_id = request.GET.get('hostel_id')
    capacity = request.GET.get('capacity')
    
    if not hostel_id or not capacity:
        return JsonResponse({'error': 'Missing parameters'}, status=400)
    
    try:
        capacity = int(capacity)
        hostel = Hostel.objects.get(id=hostel_id)
    except (Hostel.DoesNotExist, ValueError):
        return JsonResponse({'error': 'Invalid hostel or capacity'}, status=400)
    
    # Get available rooms with the specified capacity
    rooms = Room.objects.filter(
        floor__hostel=hostel,
        capacity=capacity
    ).exclude(
        current_occupancy__gte=models.F('capacity')
    ).select_related('floor').values('id', 'room_number', 'floor__floor_type', 'capacity', 'current_occupancy')
    
    rooms_list = [
        {
            'id': room['id'],
            'label': f"{hostel.name} {room['floor__floor_type']} {room['room_number']} ({room['current_occupancy']}/{room['capacity']})",
            'room_number': room['room_number'],
            'floor': room['floor__floor_type'],
            'occupancy': room['current_occupancy'],
            'capacity': room['capacity'],
        }
        for room in rooms
    ]
    
    return JsonResponse({'rooms': rooms_list})

