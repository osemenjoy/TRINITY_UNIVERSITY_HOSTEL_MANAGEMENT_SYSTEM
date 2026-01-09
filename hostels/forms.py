from django import forms
from django.core.exceptions import ValidationError
from .models import HostelRequest, StudentProfile, Hostel, Room


class HostelRequestForm(forms.ModelForm):
    """Form for creating hostel requests"""
    
    # Override preferred_room to allow dynamic queryset
    preferred_room = forms.ModelChoiceField(
        queryset=Room.objects.all(),
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'id_preferred_room'
        })
    )
    
    class Meta:
        model = HostelRequest
        fields = ['hostel', 'preferred_capacity', 'preferred_room', 'note']
        widgets = {
            'hostel': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Select a hostel',
                'id': 'id_hostel'
            }),
            'preferred_capacity': forms.Select(attrs={
                'class': 'form-control',
                'id': 'id_preferred_capacity'
            }),
            'note': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Optional note about your request...'
            }),
        }
        labels = {
            'hostel': 'Select Hostel',
            'preferred_capacity': 'Preferred Room Capacity',
            'preferred_room': 'Select Specific Room (Optional)',
            'note': 'Additional Notes (Optional)',
        }
    
    def __init__(self, *args, student=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.student = student
        
        # Filter hostels by student gender
        if student:
            self.fields['hostel'].queryset = Hostel.objects.filter(gender=student.gender)
    
    def clean(self):
        """Validate the form"""
        cleaned_data = super().clean()
        
        if not self.student:
            raise ValidationError("Student profile is required")
        
        hostel = cleaned_data.get('hostel')
        preferred_capacity = cleaned_data.get('preferred_capacity')
        preferred_room = cleaned_data.get('preferred_room')
        
        # Check gender match
        if hostel and hostel.gender != self.student.gender:
            raise ValidationError(
                f"Selected hostel is for {hostel.get_gender_display()}s only, but you are registered as {self.student.get_gender_display()}."
            )
        
        # If room is selected, validate it
        if preferred_room:
            # Check room is in the selected hostel
            if preferred_room.floor.hostel != hostel:
                raise ValidationError("Selected room must be in the selected hostel")
            
            # Check room capacity matches preference
            if preferred_room.capacity != preferred_capacity:
                raise ValidationError(f"Selected room capacity ({preferred_room.capacity}) does not match preferred capacity ({preferred_capacity})")
            
            # Check room has available space
            if preferred_room.is_full():
                raise ValidationError(f"Selected room {preferred_room} is full")
        
        # Check for active requests (PENDING or APPROVED)
        active_requests = HostelRequest.objects.filter(
            student=self.student,
            status__in=['PENDING', 'APPROVED']
        )
        
        if active_requests.exists():
            raise ValidationError(
                "You already have an active hostel request. Please wait for approval or rejection before submitting another."
            )
        
        return cleaned_data