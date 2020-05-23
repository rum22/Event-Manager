from django.urls import path
from . import views
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView,PostDeleteView,OrganizationPostListView, FilteredView, Announcement, Add_Bookmark, Remove_Bookmark
from .set_reminder import Set_Reminder

urlpatterns = [
    path('',PostListView.as_view(),name='event-home'),
    path('organization/<str:username>',OrganizationPostListView.as_view(),name='organization-posts'),
    path('about/',views.about,name='event-about'),
    path('post/<int:pk>',PostDetailView.as_view(),name='post-detail'),
    path('post/new/',PostCreateView.as_view(),name='post-create'),
    path('post/<int:pk>/update',PostUpdateView.as_view(),name='post-update'),
    path('post/<int:pk>/delete',PostDeleteView.as_view(),name='post-delete'),
    path('filtered/',views.filtered,name='filter'),
    path('filtered/<str:tag>',FilteredView.as_view(),name='filtered'),
    path('announcement/<str:username>',Announcement.as_view(),name='announcement'),
    path('post/add_bookmark/<str:username>/<int:pk>/',Add_Bookmark.as_view(),name='add_to_bookmark'),
    path('post/remove_bookmark/<str:username>/<int:pk>/',Remove_Bookmark.as_view(),name='remove_from_bookmark'),
    path('calender/<int:pk>',Set_Reminder.as_view(),name='set-reminder')
]