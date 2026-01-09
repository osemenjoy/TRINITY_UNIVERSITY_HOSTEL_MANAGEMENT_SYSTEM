from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class StudentProfile(models.Model):
    """Student profile linked to Django User model"""
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    
    LEVEL_CHOICES = [
        ('100', '100 Level'),
        ('200', '200 Level'),
        ('300', '300 Level'),
        ('400', '400 Level'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    matric_no = models.CharField(max_length=20, unique=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    level = models.CharField(max_length=3, choices=LEVEL_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()} ({self.matric_no})"
    
    class Meta:
        verbose_name = "Student Profile"
        verbose_name_plural = "Student Profiles"


class Hostel(models.Model):
    """Hostel model"""
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    
    name = models.CharField(max_length=100, unique=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.get_gender_display()})"
    
    class Meta:
        verbose_name = "Hostel"
        verbose_name_plural = "Hostels"
        ordering = ['name']
    
    def get_available_beds(self):
        """Get total available beds in hostel"""
        total_capacity = 0
        total_occupied = 0
        
        for floor in self.floors.all():
            for room in floor.rooms.all():
                total_capacity += room.capacity
                total_occupied += room.current_occupancy
        
        return max(0, total_capacity - total_occupied)


class Floor(models.Model):
    """Floor in a hostel"""
    FLOOR_CHOICES = [
        ('GF', 'Ground Floor'),
        ('FF', 'First Floor'),
        ('SF', 'Second Floor'),
    ]
    
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE, related_name='floors')
    floor_type = models.CharField(max_length=2, choices=FLOOR_CHOICES)
    
    def __str__(self):
        return f"{self.hostel.name} - {self.get_floor_type_display()}"
    
    class Meta:
        verbose_name = "Floor"
        verbose_name_plural = "Floors"
        unique_together = ('hostel', 'floor_type')
        ordering = ['hostel', 'floor_type']


class Room(models.Model):
    """Room in a floor"""
    CAPACITY_CHOICES = [
        (2, '2 persons'),
        (4, '4 persons'),
        (6, '6 persons'),
    ]
    
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE, related_name='rooms')
    room_number = models.CharField(max_length=10)
    capacity = models.IntegerField(choices=CAPACITY_CHOICES)
    current_occupancy = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.floor.hostel.name} {self.floor.get_floor_type_display()} - Room {self.room_number} ({self.current_occupancy}/{self.capacity})"
    
    class Meta:
        verbose_name = "Room"
        verbose_name_plural = "Rooms"
        unique_together = ('floor', 'room_number')
        ordering = ['floor', 'room_number']
    
    def is_full(self):
        """Check if room is at full capacity"""
        return self.current_occupancy >= self.capacity
    
    def available_beds(self):
        """Get available beds in room"""
        return max(0, self.capacity - self.current_occupancy)
    
    def clean(self):
        if self.current_occupancy > self.capacity:
            raise ValidationError("Occupancy cannot exceed capacity")


class HostelRequest(models.Model):
    """Student hostel request"""
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]
    
    CAPACITY_CHOICES = [
        (2, '2 persons'),
        (4, '4 persons'),
        (6, '6 persons'),
    ]
    
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='hostel_requests')
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE, related_name='requests')
    preferred_capacity = models.IntegerField(choices=CAPACITY_CHOICES)
    preferred_room = models.ForeignKey(Room, on_delete=models.SET_NULL, blank=True, null=True, related_name='room_requests')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.student} - {self.hostel.name} ({self.get_status_display()})"
    
    class Meta:
        verbose_name = "Hostel Request"
        verbose_name_plural = "Hostel Requests"
        ordering = ['-created_at']
    
    def clean(self):
        """Validate request"""
        # Skip validation if student or hostel is not set (form will handle this)
        if not self.student_id or not self.hostel_id:
            return
        
        # Check gender match
        if self.hostel.gender != self.student.gender:
            raise ValidationError(
                f"Hostel gender ({self.hostel.get_gender_display()}) must match student gender ({self.student.get_gender_display()})"
            )
        
        # Check for active requests (PENDING or APPROVED)
        active_requests = HostelRequest.objects.filter(
            student=self.student,
            status__in=['PENDING', 'APPROVED']
        ).exclude(pk=self.pk)
        
        if active_requests.exists():
            raise ValidationError("Student already has an active hostel request")


class Allocation(models.Model):
    """Room allocation for a student"""
    student = models.OneToOneField(StudentProfile, on_delete=models.CASCADE, related_name='allocation')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='allocations')
    date_allocated = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.student} - {self.room}"
    
    class Meta:
        verbose_name = "Allocation"
        verbose_name_plural = "Allocations"
        ordering = ['-date_allocated']
    
    def clean(self):
        """Validate allocation"""
        if self.room.is_full():
            raise ValidationError("Room is at full capacity")
        
        # Check gender match
        if self.room.floor.hostel.gender != self.student.gender:
            raise ValidationError("Student gender must match hostel gender")
