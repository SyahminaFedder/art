from django.shortcuts import render, redirect, get_object_or_404
from django.db import IntegrityError
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from website.models import Student, Course, Staff, Event, Attendace

def authenticate_student(uid, passw):
    try:
        # Authenticate based on the student's ID and password
        student = Student.objects.get(sid=uid, spass=passw)
        return student
    except Student.DoesNotExist:
        return None

# Login view for both students and staff
def login(request):
    if request.method == 'POST':
        user_id = request.POST.get('uid')  
        password = request.POST.get('passw')  
        role = request.POST.get('role') 

        # Check if both ID and password are provided
        if not user_id or not password:
            return render(request, 'login.html', {'error_message': 'Please enter both ID and password'})

        if role == 'student':
            # Custom authentication for students based on ID and password
            student = authenticate_student(user_id, password)
            if student:
                request.session['student_id'] = student.sid 
                return redirect('studmain')  
            else:
                return render(request, 'login.html', {'error_message': 'Invalid student ID or password'})

        elif role == 'staff':
            # Custom authentication for staff based on `tid` and `tpass`
            try:
                # Assuming Staff has fields `tid` (ID) and `tpass` (password)
                staff = Staff.objects.get(tid=user_id, tpass=password)
                # Store staff ID in session
                request.session['staff_id'] = staff.tid
                return redirect('staffmain')  # Redirect to staff dashboard
            except Staff.DoesNotExist:
                return render(request, 'login.html', {'error_message': 'Invalid staff ID or password'})

    return render(request, 'login.html')


    # Always return the login page for GET requests or failed POSTs
    return render(request, 'login.html')

# Registration view for both students and staff
from django.contrib.auth.models import User

def register(request):
    error_message = ""  
    success_message = ""  

    if request.method == 'POST':
        uid = request.POST['id']  # Staff ID or Student ID
        upassw = request.POST['passw']
        uname = request.POST['name']
        uphoneno = request.POST['phoneno']
        urole = request.POST['role']

        try:
            if urole == 'student':
                ucode = request.POST['programme']
                ugender = request.POST['gender']
                course_instance = Course.objects.get(code=ucode)
                student = Student(sid=uid, sname=uname, spass=upassw, gender=ugender, sphno=uphoneno, code=course_instance)
                student.save()

            elif urole == 'staff':
                uposition = request.POST['position']
                # Create a new Django User for staff, map `tid` to `username`
                user = User.objects.create_user(username=uid, password=upassw, first_name=uname)
                staff = Staff(tid=uid, tname=uname, tpass=upassw, tphno=uphoneno, role=uposition)
                staff.save()

            success_message = "Data saved successfully!"
            return redirect('login')  
        except Exception as e:
            error_message = "Data not saved: " + str(e)

    return render(request, "register.html", {
        'error_message': error_message if error_message else None,
        'success_message': success_message if success_message else None
    })

# Staff main page
def staffmain(request):
    e = Event.objects.all().select_related('tid')
    for event in e:
        print(f"Event: {event.ename}, Staff ID: {event.tid.tid}")
    context = {'ev': e}
    return render(request, 'staffmain.html', context)

# Event creation by staff
def event(request):
    if request.method == 'POST':
        evid = request.POST['evid']
        evname = request.POST['evname']
        evs = request.POST['evs']
        eve = request.POST['eve']
        evv = request.POST['evv']
        staffid = request.POST['staffid']

        staff_instance = Staff.objects.get(tid=staffid)

        if Event.objects.filter(eid=evid).exists():
            return render(request, 'event.html', {
                'error_message': 'Event with this ID already exists.',
                'form_submitted': False,
            })

        Event.objects.create(eid=evid, ename=evname, sdate=evs, edate=eve, venue=evv, tid=staff_instance)
        return redirect('staffmain')

    return render(request, 'event.html', {'form_submitted': False})

# Update an existing event
def update_ev(request, eid):
    ev = Event.objects.get(eid=eid)
    context = {'data': ev}
    return render(request, "update_ev.html", context)

# Save updated event details
def save_update_ev(request, eid):
    evname = request.POST['evname']
    evs = request.POST['evs']
    eve = request.POST['eve']
    evv = request.POST['evv']
    staffid = request.POST['staffid']

    data = Event.objects.get(eid=eid)
    staff_instance = Staff.objects.get(tid=staffid)

    data.ename = evname
    data.sdate = evs
    data.edate = eve
    data.venue = evv
    data.tid = staff_instance
    data.save()

    return HttpResponseRedirect(reverse("staffmain"))

# Delete an event
def delete_ev(request, eid):
    data = Event.objects.get(eid=eid)
    data.delete()
    return HttpResponseRedirect(reverse('staffmain'))

# Student main page with event search functionality
def studmain(request):
    # Ensure the student is logged in before performing any operations
    student_id = request.session.get('student_id')
    if not student_id:
        return redirect('login')

    if request.method == 'GET':
        eid = request.GET.get('eid')
        joined_event_ids = Attendace.objects.filter(sid=student_id).values_list('eid', flat=True)

        if eid:
            search_results = Event.objects.filter(eid=eid.upper()).exclude(eid__in=joined_event_ids)
        else:
            search_results = None
        events = Event.objects.exclude(eid__in=joined_event_ids).values()

        context = {
            'ev': events,
            'search_results': search_results,
        }
        return render(request, 'studmain.html', context)

def details_ev(request, eid):
    # Ensure the student is logged in before performing any operations
    student_id = request.session.get('student_id')
    if not student_id:
        return redirect('login')

    # Fetch the event or return a 404 if not found
    ev = get_object_or_404(Event, eid=eid.upper())  # Assuming eid is case-insensitive

    # Check if the student has already joined the event
    is_joined = Attendace.objects.filter(sid=student_id, eid=ev.eid).exists()

    # If not joined, create an attendance record
    if not is_joined:
        Attendace.objects.create(sid_id=student_id, eid=ev)

    # Return the user to their event page after processing attendance
    return redirect('my_events')

# View all events a student has registered for
def my_events(request):
    student_id = request.session.get('student_id')
    joined_events = Event.objects.filter(attendace__sid=student_id)

    context = {'joined_events': joined_events}
    return render(request, 'details_ev.html', context)

from django.contrib.auth import logout as auth_logout

def logout(request):
    auth_logout(request)  # Log the user out by clearing the session
    return redirect('login')  # Redirect to the login page

def view_participants(request):
    # Fetch all events and their associated participants (students)
    events = Event.objects.all()

    # Attach participant data for each event
    for event in events:
        event.participants = Student.objects.filter(attendace__eid=event.eid)

    # Render the template with event and participant data
    return render(request, 'view_participants.html', {'events': events})

