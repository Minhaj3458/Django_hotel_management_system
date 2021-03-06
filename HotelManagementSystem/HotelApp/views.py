from django.shortcuts import render,redirect
import mysql.connector
from .import models
from .forms import Online_Booking_form,offline_Booking_form,Add_Employee_form,Add_Room_form,Add_salary_form
from django.http import HttpResponse
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserModel
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string




# Create your views here.
def Authenticate_reg(request):
    if request.method == 'POST':
        MyData = User()
        MyData.first_name = request.POST.get('first_name')
        MyData.last_name = request.POST.get('last_name')
        MyData.username = request.POST.get('username')
        MyData.email = request.POST.get('email')
        MyData.is_superuser = request.POST.get('is_superuser')
        MyData.is_staff = request.POST.get('is_staff')
        MyData.password = request.POST.get('password')
        MyData.Con_password = request.POST.get('Con_password')
        if  MyData.password == MyData.Con_password:
             MyData.save()
        return redirect('Authenticate_login')

    return render(request,'admin/Authenticate_reg.html')
def Authenticate_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
        return redirect('Adminpage')

    return render(request, 'admin/Authenticate_login.html')

def Authenticate_Forgetpas(request):
    data = User()
    if request.method == 'POST':
        data = UserModel(request.POST, request.FILES, instance=data)
        if data.is_valid():
            data.save()
            return redirect('Authenticate_login')
        else:
            return HttpResponse("Failed")


    return render(request, 'admin/Authenticate_Forgetpas.html')
def Home(request):
    Home_About = models.About_us.objects.all().order_by('-Id')[:1]
    Context={
        'About': Home_About
    }
    return render(request,'Home.html',Context)
def all(request):
    return render(request,'allinclude.html')
def OnlineBooking(request):
    if request.method == 'POST':
        upload_image = request.FILES.get('Img')
        fname = upload_image.name
        with open('E:/Project2/HotelManagementSystem/static/Allfiles/Media/' + fname, 'wb+') as location:
            for ch in upload_image.chunks():
                location.write(ch)
        MyData = models.Online_Booking()
        MyData.Id = request.POST.get('Id')
        MyData.Check_in = request.POST.get('Check_in')
        MyData.Check_out = request.POST.get('Check_out')
        MyData.ADULT = request.POST.get('ADULT')
        MyData.CHILDREN = request.POST.get('CHILDREN')
        MyData.Name = request.POST.get('Name')
        MyData.Surname = request.POST.get('Surname')
        MyData.Email = request.POST.get('Email')
        MyData.Phone_Number = request.POST.get('Phone_Number')
        MyData.Nid_No = request.POST.get('Nid_No')
        MyData.City = request.POST.get('City')
        MyData.Country = request.POST.get('Country')
        MyData.Img = upload_image
        MyData.Address = request.POST.get('Address')
        MyData.Date = request.POST.get('Date')
        MyData.Time = request.POST.get('Time')
        MyData.save()
    return render(request,'online_booking_page.html')
def Employee_login(request):
    conn = mysql.connector.connect(host='localhost', user='root', password='', database='Hotel_Management_System')
    if request.method == 'POST':
        Employee_Id = request.POST.get('Employee_Id')
        User_email = request.POST.get('Email')
        User_password = request.POST.get('Password')
        cur = conn.cursor()
        quer1 = "select Email,Password,Employee_Id from Employee_regis where Email=%s"
        val = (User_email,)
        cur.execute(quer1, val)
        data = cur.fetchall()
        print(data, User_email)
        if User_email == data[0][0] and User_password == data[0][1] and Employee_Id == data[0][2]:
            data = models.Add_Employee.objects.get(Employee_Id=Employee_Id)
            return render(request, 'admin/EmployeeShow.html', {'data': data})
            messages.add_message(request, messages.SUCCESS, 'Login Successfully')
        else:
            messages.add_message(request, messages.ERROR, 'Employee Id & Email & Password not Macthing')
    return render(request,'Employee_login_page.html')
def Employee_Reg(request):
    if request.method == 'POST':
        Data = models.Employee_reg()
        Data.Id = request.POST.get('Id')
        Data.Fname = request.POST.get('Fname')
        Data.Lname = request.POST.get('Lname')
        Data.Email = request.POST.get('Email')
        Data.Phone_Number = request.POST.get('Phone_Number')
        Data.Employee_Id = request.POST.get('Employee_Id')
        Data.Address = request.POST.get('Address')
        Data.Password = request.POST.get('Password')
        Data.Con_password = request.POST.get('Con_password')
        Data.Date = request.POST.get('Date')
        Data.Time = request.POST.get('Time')
        Mydata = models.Add_Employee.objects.get(Employee_Id=Data.Employee_Id)
        if Data.Password == Data.Con_password and Mydata:
            user = Data.save()
            current_site = get_current_site(request)
            mail_subject ='An Account Created'
            messege = render_to_string('emailsend.html',{
                'user': user,
                'domain': current_site.domain
            })
            send_mail = request.POST.get('Email')
            email = EmailMessage(mail_subject, messege, to=[send_mail])
            email.send()
            return redirect('Employee_login')
        elif Data.Password != Data.Con_password:
            messages.add_message(request, messages.SUCCESS, 'Login Successfully')

        else:
            return HttpResponse('Fail')
    return render(request,'Employee_Register_Page.html')
def Employee_Fotpass(request):
    return render(request,'Employee_forgetpass_page.html')
def all_admin(request):
    return render(request,'admin/AdminAllinclude.html')

def Admin(request):
    data = models.Online_Booking.objects.all().order_by('-Id')
    return render(request,'admin/Admin.html',{'data':data})

def Addemployee(request):
    if request.method == 'POST':
        upload_image = request.FILES.get('Upload_Image')
        fname = upload_image.name
        with open('E:/Project2/HotelManagementSystem/static/Allfiles/Media/' + fname, 'wb+') as location:
            for ch in upload_image.chunks():
                location.write(ch)
        if request.method == 'POST':
            Data = models.Add_Employee()
            Data.Employee_Id = request.POST.get('Employee_Id')
            Data.First_Name = request.POST.get('First_Name')
            Data.Last_Name = request.POST.get('Last_Name')
            Data.Email = request.POST.get('Email')
            Data.Mobile_Number = request.POST.get('Mobile_Number')
            Data.Joining_Date = request.POST.get('Joining_Date')
            Data.Dateof_Birth = request.POST.get('Dateof_Birth')
            Data.Departments = request.POST.get('Departments')
            Data.Gender = request.POST.get('Gender')
            Data.Blood_Group = request.POST.get('Blood_Group')
            Data.Education = request.POST.get('Education')
            Data.Personal_Identity = request.POST.get('Personal_Identity')
            Data.Guardian = request.POST.get('Guardian')
            Data.Guardian_Number = request.POST.get('Guardian_Number')
            Data.Upload_Image = upload_image
            Data.Address = request.POST.get('Address')
            Data.Date = request.POST.get('Date')
            Data.Time = request.POST.get('Time')
            Data.save()
            return redirect('Addemployee')
        else:
            return HttpResponse("Failed")

    data = models.Add_Employee.objects.all().order_by('-Employee_Id')
    return render(request,'admin/addemployee.html',{'data':data})
def Editemployee(request,id):
    data = models.Add_Employee.objects.get(Employee_Id=id)
    if request.method == 'POST':
        data = Add_Employee_form(request.POST, request.FILES, instance=data)
        if data.is_valid():
            upload_image = request.FILES.get('Upload_Image')
            fname = upload_image.name
            with open('E:/Project2/HotelManagementSystem/static/Allfiles/Media/' + fname, 'wb+') as location:
                for ch in upload_image.chunks():
                    location.write(ch)
            data.save()
            return redirect('Allemployee')
        else:
            return HttpResponse("Failed")

    select = data.Departments
    if select == 'Departments':
        select = 1
    elif select == 'Housekeeping':
        select = 2
    elif select == 'Manager':
        select = 3
    elif select == 'Chef':
        select = 4
    elif select == 'Food and Beverage':
        select = 5
    elif select == 'Kitchen':
        select = 6
    elif select == 'Security':
        select = 7
    else:
        select = 8

    select = data.Gender
    if select == 'Gender':
        select = 1
    elif select == 'MALE':
        select = 2
    else:
        select = 3

    return render(request,'admin/Editemployee.html',{'data': data,"select": select})
def Allemployee(request):
    if request.method == 'POST':
        Serch = request.POST.get('search')
        print(Serch)
        data = models.Add_Employee.objects.filter(Employee_Id=Serch) or models.Add_Employee.objects.filter(First_Name=Serch)
        return render(request, 'admin/allemployee.html', {"data": data})
    data = models.Add_Employee.objects.all().order_by('-Employee_Id')
    return render(request,'admin/allemployee.html',{'data': data})
def online_Booking_info(request):
    if request.method == 'POST':
        Serch = request.POST.get('search')
        print(Serch)
        show = models.Online_Booking.objects.filter(Country =Serch) or models.Online_Booking.objects.filter(Name=Serch)
        return render(request,'admin/Online_Booking.html',{"data":show})

    data = models.Online_Booking.objects.all().order_by('-Id')
    return render(request,'admin/Online_Booking.html',{'data':data})
def Edit_online_Booking(request,id):
    data = models.Online_Booking.objects.get(Id=id)
    if request.method == 'POST':
        data = Online_Booking_form(request.POST, request.FILES, instance=data)
        if data.is_valid():
            upload_image = request.FILES.get('Img')
            fname = upload_image.name
            with open('E:/Project2/HotelManagementSystem/static/Allfiles/Media/' + fname, 'wb+') as location:
                for ch in upload_image.chunks():
                    location.write(ch)
            data.save()
            return redirect('online_Booking_info')
        else:
            return HttpResponse("Failed")

    select = data.ADULT
    if select == 'ADULT':
        select = 1
    elif select == '1 ADULT':
        select = 2
    elif select == '2 ADULT':
        select = 3
    elif select == '3 ADULT':
        select = 4
    else:
        select = 5

    select = data.CHILDREN
    if select == 'CHILDREN':
        select = 1
    elif select == '1 CHILDREN':
        select = 2
    elif select == '2 CHILDREN':
        select = 3
    elif select == '3 CHILDREN':
        select = 4
    else:
        select = 5
    return render(request,'admin/EditonlineBooking.html',{'data': data,"select":select})
def AddCustomer(request):
    if request.method == 'POST':
        upload_image = request.FILES.get('Upload_Image')
        fname = upload_image.name
        with open('E:/Project2/HotelManagementSystem/static/Allfiles/Media/' + fname, 'wb+') as location:
            for ch in upload_image.chunks():
                location.write(ch)
        if request.method == 'POST':
            Data = models.Offline_Booking()
            Data.Customer_Id = request.POST.get('Customer_Id')
            Data.Check_in = request.POST.get('Check_in')
            Data.Check_out = request.POST.get('Check_out')
            Data.First_Name = request.POST.get('First_Name')
            Data.Last_Name = request.POST.get('Last_Name')
            Data.Email = request.POST.get('Email')
            Data.Mobile_Number = request.POST.get('Mobile_Number')
            Data.ADULT = request.POST.get('ADULT')
            Data.CHILDREN = request.POST.get('CHILDREN')
            Data.Total_Person = request.POST.get('Total_Person')
            Data.Select_Room = request.POST.get('Select_Room')
            Data.Room_Number = request.POST.get('Room_Number')
            Data.Gender = request.POST.get('Gender')
            Data.Personal_Identity = request.POST.get('Personal_Identity')
            Data.Upload_Image = upload_image
            Data.Country = request.POST.get('Country')
            Data.Address = request.POST.get('Address')
            Data.Date = request.POST.get('Date')
            Data.Time = request.POST.get('Time')
            Data.save()
            return redirect('AddCustomer')
        else:
            return HttpResponse("Failed")

    data = models.Offline_Booking.objects.all().order_by('-Customer_Id')
    return render(request,'admin/AddCustomer.html',{'data': data})
def AllCustomer(request):
    if request.method == 'POST':
        Serch = request.POST.get('search')
        print(Serch)
        data = models.Offline_Booking.objects.filter(First_Name=Serch) or models.Offline_Booking.objects.filter( Email=Serch)
        return render(request, 'admin/AllCustomer.html', {"data": data})
    data = models.Offline_Booking.objects.all().order_by('-Customer_Id')
    return render(request,'admin/AllCustomer.html',{'data': data})
def EditCustomer(request,id):
    data = models.Offline_Booking.objects.get(Customer_Id=id)
    if request.method == 'POST':
        data = offline_Booking_form(request.POST, request.FILES, instance=data)
        if data.is_valid():
            upload_image = request.FILES.get('Upload_Image')
            fname = upload_image.name
            with open('E:/Project2/HotelManagementSystem/static/Allfiles/Media/' + fname, 'wb+') as location:
                for ch in upload_image.chunks():
                    location.write(ch)
            data.save()
            return redirect('AllCustomer')
        else:
            return HttpResponse("Failed")

    select = data.ADULT
    if select == 'ADULT':
        select = 1
    elif select == '1 ADULT':
        select = 2
    elif select == '2 ADULT':
        select = 3
    elif select == '3 ADULT':
        select = 4
    else:
        select = 5

    select = data.CHILDREN
    if select == 'CHILDREN':
        select = 1
    elif select == '1 CHILDREN':
        select = 2
    elif select == '2 CHILDREN':
        select = 3
    elif select == '3 CHILDREN':
        select = 4
    else:
        select = 5

    select = data.Select_Room
    if select == 'Select Room':
        select = 1
    elif select == 'Delux':
        select = 2
    elif select == 'Super Delux':
        select = 3
    elif select == 'Single':
        select = 4
    else:
        select = 5

    select = data.Room_Number
    if select == 'Room Number':
        select = 1
    elif select == 'Room101':
        select = 2
    elif select == 'Room102':
        select = 3
    elif select == 'Room103':
        select = 4
    else:
        select = 5

    select = data.Gender
    if select == 'Gender':
        select = 1
    elif select == 'MALE':
        select = 2
    else:
        select = 3

    return render(request,'admin/EditCustomer.html',{'data': data,"select": select})
def Delete(request,id):
    data = models.Online_Booking.objects.get(Id=id)
    data.delete()
    return redirect('online_Booking_info')

def Search(request):
    if request.method == 'POST':
        Serch = request.POST.get('serch')
        print(Serch)
        data = models.Offline_Booking.objects.filter(First_Name=Serch) or models.Offline_Booking.objects.filter(Email=Serch)
        return render(request, 'admin/AddCustomer.html', {"data": data})

def AddCustpage_Delete(request,id):
    data = models.Offline_Booking.objects.get(Customer_Id=id)
    data.delete()
    return redirect('AddCustomer')
def AllCustpage_Delete(request,id):
    data = models.Offline_Booking.objects.get(Customer_Id=id)
    data.delete()
    return redirect('AllCustomer')

def AddEmplopage_Delete(request,id):
    data = models.Add_Employee.objects.get(Employee_Id=id)
    data.delete()
    return redirect('Addemployee')

def Add_Employee_Search(request):
    if request.method == 'POST':
        Serch = request.POST.get('serch')
        print(Serch)
        data = models.Add_Employee.objects.filter(Employee_Id=Serch) or models.Add_Employee.objects.filter(First_Name=Serch)
        return render(request,'admin/addemployee.html', {"data": data})

def AllEmployee_Delete(request,id):
    data = models.Add_Employee.objects.get(Employee_Id=id)
    data.delete()
    return redirect('Allemployee')


def Add_room(request):
    if request.method == 'POST':
        upload_image = request.FILES.get('Room_Image')
        fname = upload_image.name
        with open('E:/Project2/HotelManagementSystem/static/Allfiles/Media/' + fname, 'wb+') as location:
            for ch in upload_image.chunks():
                location.write(ch)
        if request.method == 'POST':
            Data = models.Add_Room()
            Data.Room_Number = request.POST.get('Room_Number')
            Data.Room_Type = request.POST.get('Room_Type')
            Data.Room_Floor = request.POST.get('Room_Floor')
            Data.Room_Facility = request.POST.get('Room_Facility')
            Data.Room_Price = request.POST.get('Room_Price')
            Data.Room_Image = upload_image
            Data.Date = request.POST.get('Date')
            Data.Time = request.POST.get('Time')
            Data.save()
            return redirect('Add_room')
        else:
            return HttpResponse("Failed")

    data = models.Add_Room.objects.all().order_by('-Room_Number')
    return render(request, 'admin/AddRoom.html',{'data': data})

def Add_Room_Search(request):
    if request.method == 'POST':
        Serch = request.POST.get('serch')
        print(Serch)
        data = models.Add_Room.objects.filter(Room_Number=Serch) or models.Add_Rooms.objects.filter(Room_Type=Serch)
        return render(request, 'admin/AddRoom.html',{"data": data})

def AddRooms_Delete(request,id):
    data = models.Add_Room.objects.get(Id=id)
    data.delete()
    return redirect('Add_room')

def EditRooms(request,id):
    data = models.Add_Room.objects.get(Id=id)
    if request.method == 'POST':
        data = Add_Room_form(request.POST, request.FILES, instance=data)
        if data.is_valid():
            upload_image = request.FILES.get('Room_Image')
            fname = upload_image.name
            with open('E:/Project2/HotelManagementSystem/static/Allfiles/Media/' + fname, 'wb+') as location:
                for ch in upload_image.chunks():
                    location.write(ch)
            data.save()
            return redirect('All_Room')
        else:
            return HttpResponse("Failed")


    select = data.Room_Type
    if select == 'Select Room':
        select = 1
    elif select == 'Delux':
        select = 2
    elif select == 'Super Delux':
        select = 3
    elif select == 'Single':
        select = 4
    else:
        select = 5

    select = data.Room_Number
    if select == 'Room Number':
        select = 1
    elif select == 'Room101':
        select = 2
    elif select == 'Room102':
        select = 3
    elif select == 'Room103':
        select = 4
    else:
        select = 5

    select = data.Room_Floor
    if select == 'Room Floor':
        select = 1
    elif select == 'Floor_G':
        select = 2
    elif select == 'Floor_First':
        select = 3
    elif select == 'Floor_Second':
        select = 4
    else:
        select = 5

    return render(request,'admin/EditRooms.html',{'data': data,"select": select})

def All_Room(request):
    if request.method == 'POST':
        Serch = request.POST.get('search')
        print(Serch)
        data = models.Add_Room.objects.filter(Room_Number=Serch) or models.Add_Room.objects.filter(Room_Type=Serch)
        return render(request, 'admin/AllRooms.html',{"data": data})

    data = models.Add_Room.objects.all().order_by('-Id')
    return render(request, 'admin/AllRooms.html',{'data': data})

def AllRooms_Delete(request,id):
    data = models.Add_Room.objects.get(Id=id)
    data.delete()
    return redirect('All_Room')

def AddEmployeeSalary(request):
    if request.method == 'POST':
        if request.method == 'POST':
            Data = models.Add_Salarys()
            Data.Employee_Id = request.POST.get('Employee_Id')
            Data.Employee_Name = request.POST.get('Employee_Name')
            Data.Email = request.POST.get('Email ')
            Data.Mobile_Number = request.POST.get('Mobile_Number')
            Data.Departments = request.POST.get('Departments')
            Data.Salary = request.POST.get('Salary')
            Data.Date = request.POST.get('Date')
            Data.Time = request.POST.get('Time')
            Data.save()
            return redirect('AddEmployeeSalary')
        else:
            return HttpResponse("Failed")

    return render(request, 'admin/AddEmployeeSalary.html')

def EmployeeShow(request):

    return render(request, 'admin/EmployeeShow.html')

def EmailSend(request):

    return render(request, 'emailsend.html')