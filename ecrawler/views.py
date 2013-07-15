# Create your views here.
from django.shortcuts import render
import imaplib, email, os
from django.conf import settings
from books.models import Draft
from django.core.files.base import ContentFile



def photos(request):
	#files = [ f for f in os.listdir(settings.MEDIA_ROOT) if os.path.isfile(os.path.join(settings.MEDIA_ROOT,f)) ]
	
	img_list = Draft.objects.all()

	return render(request, 'photos.html', {"img_list": img_list})

def crawl(request):

	imap = imaplib.IMAP4_SSL(settings.MAIL_SERVER)
	imap.login(settings.BOTMAIL_USER, settings.BOTMAIL_PASSWORD)
	imap.select("INBOX") 

	imap.select()
	typ, data = imap.uid('SEARCH', 'UNSEEN')
	msgs = data[0].split()
	
	#print "Found {0} msgs".format(len(msgs))

	for uid in msgs:
	    typ, s = imap.uid('FETCH', uid, '(RFC822)')
	    mail = email.message_from_string(s[0][1])

	    #print "From: {0}, Subject: {1}, Date: {2}\n".format(mail["From"], mail["Subject"], mail["Date"])

	    if mail.is_multipart():
	        #print 'multipart'
	        for part in mail.walk():
	            ctype = part.get_content_type()
	            if ctype in ['image/jpeg', 'image/png', 'image/gif']:
	                #print "Email attachment file: %s"%part.get_filename()
	                new_draft = Draft()
	                new_draft.name = part.get_filename()

	                ext = part.get_filename().split('.')[-1]

	                new_draft.save()
	                
	                new_draft.photo.save("%s%d.%s"%("image",new_draft.id,ext),ContentFile(part.get_payload(decode=True)))

	return photos(request)


