# -*- coding: utf-8 -*-
import random
import string

import lxml
from lxml import etree
import urllib

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views.generic import ListView, FormView, CreateView, UpdateView, DeleteView, View
from django.core.urlresolvers import reverse_lazy

from .models import Link, Owner
from .forms import OwnerEditForm, LinkEditForm


class StartPageView(View):

    def create_hash(self, session_key):
        random.seed(session_key)
	chars = ''.join((string.lowercase, string.uppercase))
	gen_hash = ''.join(random.choice(chars) for _ in range(6))
	return gen_hash
    
    def get(self, request, *args, **kwargs):
        if hasattr(request, 'session') and not request.session.session_key:
            request.session.save()
            request.session.modified = True
	    session_id = request.session.session_key
	    gen_hash = self.create_hash(request.session.session_key)
	    Owner.objects.create(gen_hash=gen_hash, session_id=session_id)
	else:
	    try:
                owner = Owner.objects.get(session_id=request.session.session_key)
	        gen_hash = owner.gen_hash
	    except Owner.DoesNotExist:
		gen_hash = self.create_hash(request.session.session_key)
		session_id = request.session.session_key
		Owner.objects.create(gen_hash=gen_hash, session_id=session_id) 

	return HttpResponseRedirect(reverse_lazy('list', kwargs={'gen_hash':gen_hash}))


class YTLinksListAndCreateView(CreateView):
    template_name = 'list.html'
    model = Owner
    form_class = LinkEditForm

    def get_context_data(self, **kwargs):
	owner = Owner.objects.get(gen_hash=self.kwargs['gen_hash'])
	kwargs['object_list'] = Link.objects.filter(owner=owner)
	kwargs['owner'] = owner
	return kwargs

    def yt_parser(self, url): 
    	yt = etree.HTML(urllib.urlopen(url).read()) 
    	d = {}
    	for i in yt.iter():
            if 'videoId' in i.values(): 
                d['videoId'] = i.values()[1]
            elif 'title' in i.values():
                d['title'] = i.values()[1]
            elif 'og:image'in i.values():
                d['og:image'] = i.values()[1]
            elif 'videoId' in d.keys() and 'title' in d.keys() and 'og:image' in d.keys():
        	break
    	return d
    
    def pl_to_eng(text)
    	trans = dict((ord(a), b) for a, b in zip(u'ąćęłńóśżźĄĆĘŁŃÓŚŻŹ', u'acelnoszzACELNOSZZ'))
    	return text.translate(trans)
   
    def form_valid(self, form):
    	test_link = form.instance.link
	try:
	    form.instance.video_id = self.yt_parser(test_link)['videoId']
	    text = self.yt_parser(test_link)['title']
	    form.instance.gen_name = pl_t_eng(text)
	    form.instance.img = self.yt_parser(test_link)['og:image']
	except:
	    messages.error(self.request, 'This is not a YouTube link, please correct it')
	    return HttpResponseRedirect(reverse_lazy('list', kwargs={'gen_hash': self.kwargs['gen_hash']}))
	owner = Owner.objects.get(gen_hash=self.kwargs['gen_hash'])
	form.instance.owner = owner
        return super(YTLinksListAndCreateView, self).form_valid(form)


    def get_success_url(self):
	gen_hash = self.kwargs['gen_hash']
	return reverse_lazy('list', kwargs={'gen_hash': gen_hash})

class YTLinksDeleteView(DeleteView):
    template_name = 'delete.html'
    model = Link

    def get_object(self):
	obj = Link.objects.get(video_id=self.kwargs['video_id'])
	return obj

    def post(self, request, *args, **kwargs):
    	if request.POST.get('return'):
	    gen_hash = self.kwargs['gen_hash']
	    return HttpResponseRedirect(reverse_lazy('list', kwargs={'gen_hash':gen_hash}))
	return super(YTLinksDeleteView, self).post(request, *args, **kwargs)
    
    def get_success_url(self):
	gen_hash = self.kwargs['gen_hash']
	return reverse_lazy('list', kwargs={'gen_hash':gen_hash})


class EditUserView(UpdateView):
    template_name = 'edit.html'
    model = Owner
    form_class = OwnerEditForm

    def get_object(self):
	obj = Owner.objects.get(gen_hash=self.kwargs['gen_hash'])	
	return obj
	
    def get_success_url(self):
	gen_hash = self.object.gen_hash
	return reverse_lazy('list', kwargs={'gen_hash': gen_hash})
    
