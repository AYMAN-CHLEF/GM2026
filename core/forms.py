from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile

# --- نماذج التسجيل ---
class BaseRegisterForm(UserCreationForm):
    WIDGET_ATTRS = {'class': 'w-full p-3 border rounded-xl'}

    first_name = forms.CharField(label="الاسم", max_length=30, required=True, widget=forms.TextInput(attrs=WIDGET_ATTRS))
    last_name = forms.CharField(label="اللقب", max_length=30, required=True, widget=forms.TextInput(attrs=WIDGET_ATTRS))
    email = forms.EmailField(label="البريد الإلكتروني", max_length=150, required=True, widget=forms.EmailInput(attrs=WIDGET_ATTRS))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'email')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        email = email.strip().casefold()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("هذا البريد الإلكتروني مسجل بالفعل.")
        return email

    def save(self, commit=True, user_type='student'):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email'].strip().casefold()
        user.username = user.email
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            # حفظ الحقول الإضافية في ملف التعريف تلقائياً عند التسجيل
            UserProfile.objects.update_or_create(
                user=user, 
                defaults={
                    'user_type': user_type,
                    'first_name_ar': self.cleaned_data['first_name'],
                    'last_name_ar': self.cleaned_data['last_name']
                }
            )
        return user


class PaymentReceiptForm(forms.Form):
    cpc_image = forms.ImageField(label='وصل الدفع')

    def clean_cpc_image(self):
        image = self.cleaned_data['cpc_image']
        if image.size > 5 * 1024 * 1024:
            raise forms.ValidationError('يجب ألا يتجاوز حجم صورة الوصل 5 ميغابايت.')
        return image

class StudentRegisterForm(BaseRegisterForm):
    def save(self, commit=True):
        return super().save(commit=commit, user_type='student')

class GISRegisterForm(BaseRegisterForm):
    def save(self, commit=True):
        return super().save(commit=commit, user_type='gis_trainee')

# --- نموذج تحديث الملف الشخصي الشامل (بيانات الملف الشخصي والأسماء الثنائية) ---
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'first_name_ar', 'last_name_ar', 
            'first_name_en', 'last_name_en', 
            'level', 'phone_number', 'bio'
        ]
        widgets = {
            'first_name_ar': forms.TextInput(attrs={'class': 'w-full p-3 bg-gray-50 border border-gray-200 rounded-xl outline-none focus:border-dzGold transition-all'}),
            'last_name_ar': forms.TextInput(attrs={'class': 'w-full p-3 bg-gray-50 border border-gray-200 rounded-xl outline-none focus:border-dzGold transition-all'}),
            'first_name_en': forms.TextInput(attrs={'class': 'w-full p-3 bg-gray-50 border border-gray-200 rounded-xl outline-none focus:border-dzGold transition-all text-left', 'dir': 'ltr'}),
            'last_name_en': forms.TextInput(attrs={'class': 'w-full p-3 bg-gray-50 border border-gray-200 rounded-xl outline-none focus:border-dzGold transition-all text-left', 'dir': 'ltr'}),
            'level': forms.Select(attrs={'class': 'w-full p-3 bg-gray-50 border border-gray-200 rounded-xl outline-none focus:border-dzGold transition-all'}),
            'phone_number': forms.TextInput(attrs={'class': 'w-full p-3 bg-gray-50 border border-gray-200 rounded-xl outline-none focus:border-dzGold transition-all'}),
            'bio': forms.Textarea(attrs={'class': 'w-full p-3 bg-gray-50 border border-gray-200 rounded-xl outline-none focus:border-dzGold transition-all', 'rows': 3}),
        }

# --- نموذج تحديث الصورة الشخصية منفصلاً لمنع أي تداخل ---
class ProfileImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile 
        fields = ['profile_image']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'profile_image' in self.fields:
            self.fields['profile_image'].required = False

# --- نماذج تحديث الحساب الأساسية (اختيارية للمستخدم الأساسي) ---
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        # Changing the login email requires its own confirmation flow.
        fields = ['first_name', 'last_name']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'w-full p-3 bg-gray-50 border border-gray-200 rounded-xl outline-none focus:border-dzGold transition-all'}),
            'last_name': forms.TextInput(attrs={'class': 'w-full p-3 bg-gray-50 border border-gray-200 rounded-xl outline-none focus:border-dzGold transition-all'}),
        }

class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_image']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'profile_image' in self.fields:
            self.fields['profile_image'].required = False
