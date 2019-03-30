from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Contact
from django.core.mail import send_mail

# Create your views here.
def contact(request):
    if request.method == 'POST':
        listing_id = request.POST['listing_id']
        listing = request.POST['listing']    
        name = request.POST['name']        
        realtor_email = request.POST['realtor_email']        
        user_id = request.POST['user_id']        
        phone = request.POST['phone']
        email = request.POST['email']
        message = request.POST['message']

        if request.user.is_authenticated:
            user_id = request.user.id
            has_contacted = Contact.objects.all().filter(listing_id=listing_id,user_id=user_id)
            if has_contacted:
                messages.error(request,'You have already made an inquiry for this listing')
                return redirect('/listings/'+listing_id )
        contact = Contact(listing=listing, listing_id=listing_id, name=name, email=email, phone=phone, message=message, user_id=user_id)

        contact.save()
        send_mail(
            'Propery Listing Inquiry','There has been an inquiry for ' + listing + '. Sign into the admin panel for more info.','wsmoyer@ualr.edu',[realtor_email,'wsmoyer@ualr.edu'],fail_silently=False
        )
        messages.success(request, 'Your request has been submitted, a realtor will contact you soon.')
        return redirect('/listings/'+listing_id )