from django.contrib import admin
from .models import (
    StudentProfile, Hostel, Floor, Room, HostelRequest, Allocation
)


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'matric_no', 'gender', 'level', 'created_at')
    list_filter = ('gender', 'level', 'created_at')
    search_fields = ('user__first_name', 'user__last_name', 'matric_no')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('User', {'fields': ('user',)}),
        ('Student Information', {'fields': ('matric_no', 'gender', 'level')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )


@admin.register(Hostel)
class HostelAdmin(admin.ModelAdmin):
    list_display = ('name', 'gender', 'get_available_beds', 'created_at')
    list_filter = ('gender', 'created_at')
    search_fields = ('name',)
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Hostel Details', {'fields': ('name', 'gender', 'description')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )


@admin.register(Floor)
class FloorAdmin(admin.ModelAdmin):
    list_display = ('hostel', 'floor_type')
    list_filter = ('hostel', 'floor_type')
    search_fields = ('hostel__name',)


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('floor', 'room_number', 'capacity', 'current_occupancy', 'available_beds')
    list_filter = ('floor__hostel', 'capacity', 'current_occupancy')
    search_fields = ('floor__hostel__name', 'room_number')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Room Location', {'fields': ('floor',)}),
        ('Room Details', {'fields': ('room_number', 'capacity')}),
        ('Occupancy', {'fields': ('current_occupancy',)}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )


@admin.register(HostelRequest)
class HostelRequestAdmin(admin.ModelAdmin):
    list_display = ('student', 'hostel', 'preferred_capacity', 'status', 'created_at')
    list_filter = ('status', 'hostel', 'created_at', 'preferred_capacity')
    search_fields = ('student__user__first_name', 'student__user__last_name', 'student__matric_no')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Student & Hostel', {'fields': ('student', 'hostel')}),
        ('Request Details', {'fields': ('preferred_capacity', 'note')}),
        ('Status', {'fields': ('status',)}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )
    
    actions = ['approve_requests', 'reject_requests']
    
    def approve_requests(self, request, queryset):
        """Admin action to approve requests"""
        for hostel_request in queryset.filter(status='PENDING'):
            # Find available room
            from django.db.models import F
            available_room = Room.objects.filter(
                floor__hostel=hostel_request.hostel,
                capacity=hostel_request.preferred_capacity,
                current_occupancy__lt=F('capacity')
            ).first()
            
            if not available_room:
                available_room = Room.objects.filter(
                    floor__hostel=hostel_request.hostel,
                    current_occupancy__lt=F('capacity')
                ).first()
            
            if available_room:
                allocation, created = Allocation.objects.get_or_create(
                    student=hostel_request.student,
                    defaults={'room': available_room}
                )
                
                if created:
                    available_room.current_occupancy += 1
                    available_room.save()
                
                hostel_request.status = 'APPROVED'
                hostel_request.save()
    
    approve_requests.short_description = "Approve selected requests and allocate rooms"
    
    def reject_requests(self, request, queryset):
        """Admin action to reject requests"""
        count = queryset.filter(status='PENDING').update(status='REJECTED')
        self.message_user(request, f"{count} request(s) rejected.")
    
    reject_requests.short_description = "Reject selected requests"


@admin.register(Allocation)
class AllocationAdmin(admin.ModelAdmin):
    list_display = ('student', 'room', 'date_allocated')
    list_filter = ('room__floor__hostel', 'date_allocated')
    search_fields = ('student__user__first_name', 'student__user__last_name', 'student__matric_no')
    readonly_fields = ('date_allocated',)
    
    fieldsets = (
        ('Student', {'fields': ('student',)}),
        ('Room Assignment', {'fields': ('room',)}),
        ('Additional Info', {'fields': ('notes', 'date_allocated')}),
    )
