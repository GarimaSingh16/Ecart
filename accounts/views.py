from django.http import HttpRequest
from django.shortcuts import redirect, render
from .forms import RegistrationForm
from .models import User
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.decorators import login_required

# ++++++++++++++++++++++++++++++++++++++++++ ==================   User Verification/Authentication through mail ================= +++++++++++++++++++++++++++++++++++++++++
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

from carts.views import _cart_id
from carts.models import Cart,CartItem
import requests

# Create your views here.

def register(request):    
    # form = RegistrationForm()
    
    if request.method =='POST':
        form = RegistrationForm(request.POST)
        # it will contain all the details of the forms which we will get from post request
        
        
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']   
            phone_number = form.cleaned_data['phone_number']   
            email = form.cleaned_data['email']   
            password = form.cleaned_data['password']   
            username = email.split('@')[0]
            # here we are taking the part before the @ and storing it as username because it is unique in nature as same mail address can't be generated
            
            # remember we have created a create_user() method inside the models.py which is used to save the user and return the user after creation.
            # def create_user(self,first_name,last_name,email,username,password=None,password2=None):
            # it is taking arguments so we need to pass all these arguments as there is no defualt value or arguments there , it is mandatory to pass them except password2
            
            user = User.objects.create_user(first_name=first_name,last_name=last_name,email=email,username=username,password=password)
            # it will return the user after saving the detail
            
            user.phone_number = phone_number
            user.save()
            
            # ++++++++++++++++++++++++++++++++++++++  ========================User Login after registration (directly without verification) ===========================+++++++++++++++++++++++++++++++++++++++++
            # user = auth.authenticate(email=email,password=password)
            # auth.login(request,user)
            
            
            
            # ++++++++++++++++++++++++++++++++++++++ ========================  User Verification/Activation [through email] ======================== ++++++++++++++++++++++++++++++++++++
            
            current_site = get_current_site(request)
            mail_subject = "Please activate your account"
            message = render_to_string('accounts/account_verification_email.html',{
                'user': user,
                'domain': current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()
            
            
            # messages.success(request,f'Thank you for registering with us. We have send you a verification email to you email : {email} address . Please verify it.')
            # return redirect('register')
            
            
            # +++++++++ after using activation (for making it more better) . Here we will not show login form instead of that we will show a message just after registration so that is why we are doing it. +++++++++++
            return redirect('/accounts/login/?command=verification&email='+email)
            # here : command=verification , it can be anything
            # for this we will make change in login.html also
            
            
            # messages.success(request,"Welcome, now you are the member of this family")
            
            # return redirect('home')
            
    else:      
        form = RegistrationForm()
    return render(request,'accounts/register.html',{'form':form})
    
    
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = auth.authenticate(email=email,password=password)
        
        if user :
            
            try:
                
                cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cart_items_exists = CartItem.objects.filter(cart=cart).exists()
                print(is_cart_items_exists)
                
                if is_cart_items_exists:
                    cart_items = CartItem.objects.filter(cart=cart)
                
                # ++++++++++++ Getting the product variation by cart id ++++++++++++++++
                    product_variation = []
                    for cart_item in cart_items:
                        variation = cart_item.variation.all()
                        
                        product_variation.append(list(variation))
                        
                        
                # ++++++++++++++ Get the cart items from the user to access his product variation ++++++++++++++++++++++++++++
                    cart_items = CartItem.objects.filter(user=user)
                    ex_var_list = []
                    id=[]
                    for cart_item in cart_items:
                        existing_variation = cart_item.variation.all()
                        ex_var_list.append(list(existing_variation))
                        id.append(cart_item.id)
                        
                        
                    # product_variation = [1,2,3,4,5,6]
                    # ex_var_list =  [6,3,2]
                    
                    for pr in product_variation:
                        if pr in ex_var_list:
                            index = ex_var_list.index(pr)
                            item_id = id[index]
                            cart_item = CartItem.objects.get(id=item_id)   
                            cart_item.quantity += 1
                            cart_item.user = user
                            cart_item.save() 
                        else:
                            cart_items = CartItem.objects.filter(cart=cart)
                            for cart_item in cart_items:
                                cart_item.user = user
                                cart_item.save()

            except:
                print('entering inside except block')
                pass
            
            auth.login(request,user)
            
            messages.success(request,'Welcome back, hope you are doing great. Enjoy shopping... ')
            
            # it will grab the previous url from where we had came
            url = request.META.get('HTTP_REFERER')
            
            try:
                query = requests.utils.urlparse(url).query
                print("query:",query)
                print('++++++++++++++++++++++++++++')
                params = dict(
                    x.split('=') for x in query.split('&')
                )
                print("params",params)
                
                if 'next' in params:
                    nextPage = params['next']
                    return redirect(nextPage)            
             
            except:
                return redirect('dashboard')
                        
        else:
            messages.error(request,'Please Enter Valid Data')
        
    return render(request,'accounts/login.html')

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request,'Logged out successfully')
    return redirect('home')

@login_required(login_url='login')
def dashboard(request):
    return render(request,'accounts/dashboard.html')



def activate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
        user = None
        
    
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active = True
        user.save()
        messages.success(request,'Congratulations! Your account have been activated.')
        return redirect('login')
    
    else:
        messages.error(request,'Invalid activation link')
        return redirect('register')
    
    
def forgotPassword(request):
    
    if request.method == 'POST':
        email = request.POST.get('email')
        print(email)
        
        # if account with this email exists in database
        if User.objects.filter(email=email).exists() :
            user = User.objects.get(email__exact=email)
            
            # +++++++++ Email +++++++++++
            current_site = get_current_site(request)
            mail_subject = 'Reset Your Password'
            message = render_to_string('accounts/reset_password_email.html',{
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()
            
            messages.success(request,'Password reset email has been send to your email address.')
            return redirect('login')
            
        else:
            messages.error(request,"Account does not exist")
            return redirect('forgotPassword')
            
    
    return render(request,'accounts/forgotPassword.html')

# validate functions is used to validate the link in which user will click
def resetpassword_validate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
        user = None
        
    
    if user is not None and default_token_generator.check_token(user,token):
        
        # ✅ Store UID in session
        request.session['uid'] = uid
        messages.success(request,'Please reset your password')
        return redirect('resetPassword')
    
    else:
        messages.error(request,'This link has been expired.')
        return redirect('forgotPassword')
    
    
def resetPassword(request):
    
    if request.method == 'POST':
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        # uid will bw present inside session
        uid = request.session.get('uid')
        if not uid:
            messages.error(request, "Session expired or invalid reset link.")
            return redirect('forgotPassword')
        
        else:
            if password == password2:
                
                user = User.objects.get(pk=uid)
                user.set_password(password)
                user.save()
                messages.success(request,'Password reset successfully.')
                return redirect('login')
            
            else:
                messages.error(request,'Passwords do not match')
                redirect('resetPassword')
    return render(request,'accounts/resetPassword.html')