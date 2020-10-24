"""library URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, include
from .import views
app_name= 'main'
urlpatterns = [
    path('test/', views.test,name='test'), 
    path('login/',views.login,name='login'),  
    path('addLibrarian/',views.addLibrarian,name='addLibrarian'), 
    path('viewLibrarian/',views.viewLibrarian,name='viewLibrarian'),
    path('deleteUser/<int:user_id>/', views.deleteUser,name='deleteUser'),
    path('user_search/',views.userSearch,name='userSearch'),
    path('addStudent/',views.addStudent,name='addStudent'),
    path('viewStudent/',views.viewStudent,name= "viewStudent"),
    path('student_profile/<int:student_id>/', views.student_profile,name='student_profile'),
    path('book_section/',views.bookSection,name='book_section'),
    path('bookSuggest/<str:name>/',views.bookSuggest,name= 'bookSuggest'),
    path('issueBook/<int:user_id>/<int:book_id>/<int:year>/<int:month>/<int:day>/<int:hour>/<int:minute>/',views.issueBook,name='issueBook'),
    path('returnBook/<int:order_id>/',views.returnBook,name='returnBook'),
    path('adminProfile/<int:user_id>/',views.adminProfile,name='adminProfile'),
    path('librarianProfile/<int:user_id>/',views.librarianProfile,name='librarianProfile'),
]
