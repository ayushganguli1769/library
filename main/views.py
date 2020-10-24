from django.shortcuts import render,redirect
from django.http import HttpResponse,Http404
from django.contrib.auth.models import auth,User
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, permission_classes
from .models import Customer, Book, OrderList
from functools import cmp_to_key
from django.views.decorators.csrf import csrf_exempt
import json
from django.db.models import Q
import pytz
from datetime import datetime
def dateCompare(x,y):
    if x.is_returned is False and y.is_returned is True:
        return -1
    elif x.is_returned is True and y.is_returned is False:
        return 1
    else:
        if x.return_date < y.return_date:
            return -1
        else:
            return 1
def home(request):
    return render(request,'home_page.html')
def test(request):
    return render(request,'home_page.html')
    return render(request, 'admin_profile.html')
def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username = username, password = password)
        if user != None :
            auth.login(request,user)
            curr_user_id = str(request.user.id)
            if request.user.is_staff or request.user.type_user.is_admin:
                url = '/adminProfile/' + curr_user_id+'/'
                return redirect(url)
            elif request.user.type_user.is_librarian:
                url = '/librarianProfile/' + curr_user_id+'/'
                return redirect(url)
            else:
                return HttpResponse("Not a valid User")
        else:
            return render(request, 'login.html', {'message':"This is a demo version. To maintain security users can only be added by admin. Please use the IDs username:admin password:1234 or username:librarian2 password:1234",'error_message': "Invalid Credentials"})
    return render(request,'login.html', {'message':"This is a demo version. To maintain security users can only be added by admin. Please use the IDs username:admin password:1234 or username:librarian2 password:1234"})
@login_required
def addLibrarian(request):
    if request.user.is_staff or request.user.type_user.is_admin:
        if 'addUser' in request.POST :
            print('exec block')
            (is_admin,is_librarian) = (False,False)
            username = request.POST['username']
            if User.objects.filter(username= username).exists():
                return render(request,'addLibrarian.html',{'message':"User with curr username already exists"})
            designation = request.POST['designation']
            email = request.POST['email']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            password = request.POST['password']
            password1 = request.POST['password1']
            if 'is_admin' in request.POST :
                is_admin = True
            if 'is_librarian' in request.POST :
                is_librarian = True
            print(is_admin,is_librarian)
            my_user = User.objects.create_user(username = username,password = password,first_name = first_name,last_name = last_name,is_staff = is_admin)
            my_user.save()
            my_user.type_user.is_admin = is_admin
            my_user.type_user.is_librarian = is_librarian
            my_user.type_user.designation = designation
            my_user.save()
        return render(request,'addLibrarian.html')
    else:
        raise Http404("Unathorized")
@login_required
def viewLibrarian(request):
    if request.user.is_staff or request.user.type_user.is_admin:
        all_user = User.objects.all()
        return render(request,'viewLibrarian.html',{'all_user':all_user})
    else:
        raise Http404("Unathorized")
@login_required
def deleteUser(request,user_id):
    if request.user.is_staff or request.user.type_user.is_admin:
        user_to_delete = User.objects.get(id = user_id)
        user_to_delete.delete()
        return HttpResponse("ok")
    else:
        raise Http404("Unathorized")
@login_required
def userSearch(request):
    if request.user.is_staff or request.user.type_user.is_admin:
        all_user = []
        print('exec')
        (is_admin,is_librarian) = (False,False)
        text_val = request.POST['text_val']
        if text_val.isdigit():
            try:
                all_user_temp = [User.objects.get(id = int(text_val))]
            except User.DoesNotExist:
                return render(request,'viewLibrarian.html',{'all_user':all_user})
        else:
            all_user_temp = User.objects.filter(username__contains = text_val)
        print(all_user_temp)
        if 'is_admin' in request.POST:
            is_admin = True
        if 'is_librarian' in request.POST:
            is_librarian = True
        for curr_user in all_user_temp:
            if (curr_user.is_staff or curr_user.type_user.is_admin) and is_admin:
                all_user.append(curr_user)
            elif (curr_user.type_user and curr_user.type_user.is_librarian) and is_librarian:
                all_user.append(curr_user)
        return render(request,'viewLibrarian.html',{'all_user':all_user})
    else:
        raise Http404("Unathorized")
@login_required
def addStudent(request):
    if request.user.type_user.is_librarian:
        message= None
        if 'addStudent' in request.POST:
            name = request.POST['student_name']
            phone_no = int(request.POST['phone_no'])
            new_customer = Customer(name= name,phone_no=phone_no)
            new_customer.save()
            message = "Student Sucessfully Added"
        return render(request,'addStudent.html',{'message':message})
    else:
        raise Http404("Unathorized")
@login_required
def viewStudent(request):
    if request.user.type_user.is_librarian:
        all_student = Customer.objects.all()
        message = None
        if  request.POST:
            text_val = request.POST['text_val']
            if text_val.isdigit():
                try:
                    all_student = [all_student.get(phone_no = int(text_val))]
                except:
                    return render(request,'viewStudent.html',{'message':"Student with given phone number does not exist",'all_student':[]})
            else:
                all_student= all_student.filter(name__contains = text_val)
        
        return render(request,'viewStudent.html',{'message':message,'all_student':all_student})
@login_required
def student_profile(request,student_id):
    if request.user.type_user.is_librarian:
        profile_user = Customer.objects.get(id = student_id)
        student_order_list = OrderList.objects.filter(customer_related= profile_user)
        print(student_order_list,'before sort')
        student_order_list = sorted(student_order_list , key = cmp_to_key(dateCompare))
        print(student_order_list,'after sort')
        if 'update' in request.POST:
            name = request.POST['student_name']
            phone_no = int(request.POST['student_phone_no'])
            image = None
            if 'student_image' in request.FILES:
                image = request.FILES['student_image']
            profile_user.name = name
            profile_user.phone_no = phone_no
            profile_user.image = image
            profile_user.save()
        return render(request,'profile.html',{'profile_user':profile_user,'student_order_list':student_order_list})
    else:
        raise Http404("Unathorized User")
@login_required
def bookSection(request):
    if request.user.type_user.is_librarian:
        if 'addBook' in request.POST:
            name = request.POST['name']
            author = request.POST['author']
            new_book = Book(name= name, author= author)
            new_book.save()
        all_books = Book.objects.all()
        return render(request,'book_section.html',{'all_books':all_books})
    else:
        raise Http404("Unathorized User")
@login_required
@csrf_exempt
def bookSuggest(request,name):
    if request.user.type_user.is_librarian:  
        q1 = Q( name__contains = name)
        q2 = Q(author__contains = name)
        all_books_query = Book.objects.filter( q1 | q2)
        data = {'all_book':[]}
        curr = 0
        for book in all_books_query:
            data['all_book'].append({'name':book.name,'author':book.author,'id':book.id})
            curr += 1
            if curr > 10:
                break
        return HttpResponse(json.dumps(data))
    else:
        return HttpResponse("Unathorized")
@login_required
@csrf_exempt
def issueBook(request,user_id,book_id,year,month,day,hour,minute):
    if request.user.type_user.is_librarian: 
        try:
            req_book = Book.objects.get(id= int(book_id))
            customer_object = Customer.objects.get(id = user_id)
            return_date = datetime(year,month,day,hour,minute, tzinfo = pytz.timezone("Asia/Calcutta"))
            new_order = OrderList(customer_related = customer_object,book_related = req_book,return_date = return_date)
            new_order.save()
            data = {'message':'ok','book_name':req_book.name,'book_author':req_book.author,'issue_date':str(new_order.issue_date),'return_date':str(return_date),'order_id':new_order.id}
            return HttpResponse(json.dumps(data))
        except:
            return HttpResponse(json.dumps({'message':"Invalid"}))
    else:
        return HttpResponse("Unathorized")
@login_required
@csrf_exempt
def returnBook(request,order_id):
    returned_order =OrderList.objects.get(id = order_id)
    returned_order.is_returned = True
    returned_order.save()
    return HttpResponse("ok")
def librarianProfile(request,user_id):
    curr_user = User.objects.get(id= user_id)
    return render(request, 'librarian_profile.html',{'curr_user':curr_user})
def adminProfile(request,user_id):
    curr_user = User.objects.get(id= user_id)
    return render(request, 'admin_profile.html',{'curr_user':curr_user})