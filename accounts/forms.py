from django import forms
from pydantic import ValidationError
from .models import User

class RegistrationForm(forms.ModelForm):
    
    # creating new field 
    # password = forms.PasswordInput(attrs=
    #     {'placeholder':'Enter Password',
    #     }
    # )
    
    # we will be using this instead of the above code because it might be creating probelm and we are using two password fields so it will be good if we use charfield and inside it if we pass widget=forms.PasswordField
    password = forms.CharField(widget=forms.PasswordInput(attrs=
        {'placeholder':'Repeat Password',
        })
    )
    
    # NOT WORKING
    # password2 = forms.PasswordInput(attrs=
    #     {'placeholder':'Repeat Password',
    #     'class' : 'form-control'
    #     }
    # )
    
    # IT IS ALSO NOT WORKING BECAUSE WE CAN"T USE PASSWORD FIELD DIRECTLY TWO TIMES
    # confirm_password = forms.PasswordInput(attrs=
    #     {'placeholder':'Enter Password',
    #     'class' : 'form-control'
    #     }
    # )
    
    
    # it is working becasue we haven't used 2 password fields whicch is not allowed but we can pass it ibnnto the widget if we want to use password.
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=
        {'placeholder':'Confirm Password...',
        })
    )
    
    
    # first_name = forms.CharField(widget = {'placeholder':'Enter your first name...','class':'form-control'})
    
    class Meta:
        model = User
        fields = ['first_name','last_name','phone_number','email','password','password2']
        
     # By default clean data is there but here we changing its default working like other methods (str,init etc).
    def clean(self):
        cleaned_data = super(RegistrationForm,self).clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        # confirm_password = cleaned_data.get('password2')

        if password != password2:
            raise forms.ValidationError("Password does not match.")            
        
    def __init__(self, *args, **kwargs):
        super(RegistrationForm,self).__init__(*args, **kwargs)
        
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter your first name...'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter your last name...'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter your phone number...'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter your email address...'
        
        for field in self.fields:
            
            # 'RegistrationForm' object has no attribute 'field'
            # self.field.widget.attrs['class']='form-control'
        
            self.fields[field].widget.attrs['class']='form-control'
            
            # label = self.fields[field].label or field.replace('_', ' ')
            # self.fields[field].widget.attrs['placeholder']=f'Enter {label.lower()} ...'
            
    
