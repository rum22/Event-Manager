from django.shortcuts import render, redirect, get_object_or_404
from .forms import OrganizationRegisterForm,OrganizationUpdateForm,Profile_orgUpdateForm, Profile_viewerUpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from event.models import Post
from django.contrib.auth.models import User

def register_org(request):
	if request.method == 'POST':
		form=OrganizationRegisterForm(request.POST)
		#checks validity at backend
		if(form.is_valid()):
			form.save()
			username=form.cleaned_data.get('username')
			messages.success(request, f'Your Account has been created! You will now be able to login.')
			return redirect('login_org')
	else:
		form=OrganizationRegisterForm()
	return render(request,'organizations/register_org.html', {'form':form})

#decorator adds functionality to an existing function.here it checks if a person is logged in or not.
@login_required
def profile_org(request):
	if request.method == 'POST':
		u_form = OrganizationUpdateForm(request.POST, instance=request.user)
		if request.user.profile_org.is_org:
			p_form = Profile_orgUpdateForm(request.POST, request.FILES, instance=request.user.profile_org)
		else:
			p_form = Profile_viewerUpdateForm(request.POST, instance=request.user.profile_org)#because we are upoading an image
		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()
			messages.success(request, f'Your Account has been Updated!')
			return redirect('profile_org')
	else:
		u_form = OrganizationUpdateForm(instance=request.user)
		if request.user.profile_org.is_org:
			p_form = Profile_orgUpdateForm(instance=request.user.profile_org)
		else:
			p_form = Profile_viewerUpdateForm(instance=request.user.profile_org)
	context={
		'u_form': u_form,
		'p_form': p_form
	}
	return render(request,'organizations/profile_org.html', context)

class Bookmarks_user(LoginRequiredMixin,ListView):
	model = Post
	template_name = 'organizations/bookmarks_view.html'
	context_object_name = 'posts'
	paginate_by = 4

	def get_queryset(self):
		user = get_object_or_404(User, username=self.kwargs.get('username'))
		p = Post.objects.none()
		for i in user.profile_org.bookmarks.all():
			p |= Post.objects.filter(pk=i.pk)
		return p.order_by('-date_posted')
