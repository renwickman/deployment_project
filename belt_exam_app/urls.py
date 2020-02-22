from django.urls import path
from . import views

urlpatterns = [
   path('', views.index),
   path('users', views.createUser),
   path('login', views.login),
   path('welcome', views.welcome),
   path('quoteAdd', views.addQuote),
   path('quoteDelete/<int:id>', views.deleteQuote),
   path('like/<int:id>', views.likeQuote),
   path('unlike/<int:id>', views.unlikeQuote),
   path('user/<int:id>', views.displayUser),
   path('myaccount/edit/<int:id>', views.editUser),
   path('myaccount/submit/<int:id>', views.submitUser),
   path('logout', views.logout)
]

# path('editUser', views.editUser),
   # path('submitUser', views.submitUser),


# urlpatterns = [
#     path('', views.index),
#     path('users', views.createUser),
#     path('login', views.login),
#     path('homepage', views.homepage),
#     path('cats', views.createCat),
#     path('vote/<int:id>', views.voteCat),
#     path('unvote/<int:id>', views.unvoteCat),
#     path('delete/<int:id>', views.deleteCat),
#     path('profile', views.userProfile),
#     path('cats/<int:id>', views.catProfile),
#     path('logout', views.logout)
# ]