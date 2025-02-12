"""

URL configuration for litrevu project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))

"""

from django.contrib import admin
from django.urls import path
from authentication.views import CustomLoginView, SignupPageView
from django.contrib.auth.views import LogoutView
from blog.views import (
    home,
    ticket_upload,
    edit_ticket,
    delete_ticket,
    review_upload,
    edit_review,
    delete_review,
    create_ticket_review,
    subscriptions,
    follow_user,
    unfollow_user,
    user_posts,
)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", CustomLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),
    path(
        "signup/",
        SignupPageView.as_view(template_name="authentication/signup.html"),
        name="signup",
    ),
    path("home/", home, name="home"),
    path("create_ticket/", ticket_upload, name="create_ticket"),
    path("ticket/<int:ticket_id>/edit/", edit_ticket, name="edit_ticket"),
    path("ticket/<int:ticket_id>/delete/", delete_ticket, name="delete_ticket"),
    path("ticket/<int:ticket_id>/create_review/", review_upload, name="create_review"),
    path("review/<int:review_id>/edit/", edit_review, name="edit_review"),
    path("review/<int:review_id>/delete/", delete_review, name="delete_review"),
    path("ticket-review/create", create_ticket_review, name="create_ticket_review"),
    path("subscriptions/", subscriptions, name="subscriptions"),
    path("follow/", follow_user, name="follow_user"),
    path("unfollow/<int:user_id>/", unfollow_user, name="unfollow_user"),
    path("posts", user_posts, name="user_posts"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
