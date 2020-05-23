from django.shortcuts import render, get_object_or_404
from .models import Post
from django.views.generic import ListView, DetailView, CreateView,UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User

#posts=[
#	{
#		'organization': 'dhrumil',
#		'title': 'Event 1',
#		'content': 'First Event content',
#		'date_posted': 'August 1, 2020',
#		'date_of_event': 'August 10,2020',
#		'venue': 'Nalanda',
#		'tags': {'educational' : 0,'fun' : 1,'sports' : 1,'party' : 1,'other' : 0},
#	},
#	{
#		'organization': 'test',
#		'title': 'Event 2',
#		'content': 'Second Event content',
#		'date_posted': 'August 3, 2020',
#		'date_of_event': 'August 12,2020',
#		'venue': 'Nehru Hall',
#		'tags': {'educational' : 1,'fun' : 0,'sports' : 0,'party' : 1,'other' : 0},
#	}
#]

"""function based view
def home(request):
	context={
		'posts': Post.objects.all()
	}
	return render(request, 'event/home.html', context)
"""

#class based views has a lot of inbuilt good stuff
class PostListView(ListView):
	model = Post
	#searches for the give template
	template_name = 'event/home.html'
	context_object_name = 'posts'
	ordering = ['-date_posted']
	#adds the pages link. all logic about it is on homepage
	paginate_by = 4

class OrganizationPostListView(ListView):
	#model on which we query
	model = Post
	#searches for the give template
	template_name = 'event/organization_posts.html'
	context_object_name = 'posts'
	#adds the pages link. all logic about it is on homepage
	paginate_by = 4

	#overriding the query that this list view will make
	def get_queryset(self):
		user = get_object_or_404(User, username=self.kwargs.get('username'))
		return Post.objects.filter(organization=user).order_by('-date_posted')


class Add_Bookmark(DetailView):
	model = Post
	template_name = 'event/after_bookmark.html'
	def get_queryset(self):
		user = get_object_or_404(User, username=self.kwargs.get('username'))
		pst = get_object_or_404(Post, pk=self.kwargs.get('pk'))
		user.profile_org.bookmarks.add((Post.objects.filter(pk=pst.pk)).first())
		return super().get_queryset()

class Remove_Bookmark(DetailView):
	model = Post
	template_name = 'event/after_bookmark.html'
	def get_queryset(self):
		user = get_object_or_404(User, username=self.kwargs.get('username'))
		pst = get_object_or_404(Post, pk=self.kwargs.get('pk'))
		user.profile_org.bookmarks.remove((Post.objects.filter(pk=pst.pk)).first())
		return super().get_queryset()

class FilteredView(ListView):
	model = Post
	template_name = 'event/filtered_posts.html'
	context_object_name = 'posts'
	paginate_by = 4
	#trying to use postcreateview and orgpostlistview like stuff
	def get_queryset(self):
		tag=self.kwargs.get('tag')
		post = Post.objects.none()
		for p in Post.objects.all():
			for t in p.tags:
				if t==tag:
					post |= Post.objects.filter(pk=p.pk)
		#post |= Post.objects.last()
		return post.order_by('-date_posted')


class PostDetailView(DetailView):
	model = Post

#this mixin allows you to create post only if you are logged in
class PostCreateView(LoginRequiredMixin, CreateView):
	model = Post
	Post.date_of_event.input_formats=['%Y-%m-%d']
	fields = ['title','content','venue','date_of_event','tags']
	def form_valid(self, form):
		form.instance.organization = self.request.user
		return super().form_valid(form)

#userpassestestmixin used so that no one else can update out post.def_func used for that
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Post
	# enter event details as YYYY-MM-DD hh:minmin:secsec
	Post.date_of_event.input_formats=['%Y-%m-%d']
	fields = ['title','content','venue','date_of_event','tags']
	def form_valid(self, form):
		form.instance.organization = self.request.user
		return super().form_valid(form)

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.organization:
			return True
		return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Post
	success_url = '/'

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.organization:
			return True
		return False

def about(request):
	return render(request, 'event/about.html',{'title':'About'})

def filtered(request):
	return render(request, 'event/filtered.html')

class Announcement(ListView):
	model = Post
	template_name = 'event/announcement.html'
	context_object_name = 'posts'
	paginate_by = 4

	def get_queryset(self):
		user = get_object_or_404(User, username=self.kwargs.get('username'))
		return Post.objects.filter(organization=user).order_by('-date_posted')