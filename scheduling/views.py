from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from .models import User, classRooms, Course, Time, coursesoffered
from django.contrib.auth.decorators import login_required

# Create your views here.


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("addDetails"))
        else:
            return render(request, "scheduling/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        messages.success(request,"Username = 'halden' , Password = '123456' ")
        return render(request, "scheduling/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "scheduling/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "scheduling/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "scheduling/register.html")

def index(request):

    if request.user :
       return HttpResponseRedirect(reverse('addDetails'))
    else :
        return render(request, "scheduling/login.html")


@login_required(login_url="login")
def addDetails(request):

    if request.user :
        context = {
            'courses' : Course.objects.filter(user_name = request.user),
            'times': Time.objects.filter(user_name = request.user)   
        }

        return render(request, "scheduling/index.html", context)
    else:
        return render(request, "scheduling/index.html")



# Add Courses Offered 
@login_required(login_url="login")
def coursesOffered(request):
    
    if request.method == "POST":
        try : 
            selectCourse = request.POST["selectCourse"]
        except:
            selectCourse = 0
        try:
            studentEnrollment = request.POST["studentEnrollment"]
        except:
            studentEnrollment = 0
        try:
            selectTime1 = request.POST["selectTime1"]
        except:
            selectTime1 = ''
        try:
            selectTime2 = request.POST["selectTime2"]
        except:
            selectTime2 = ''
        try:
            selectTime3 = request.POST["selectTime3"]
        except:
            selectTime3 = ''
        try:
            selectTime4 = request.POST["selectTime4"]
        except:
            selectTime4 = ''
        try:
            selectTime5 = request.POST["selectTime5"]
        except:
            selectTime5 = ''

        timeList = [selectTime1, selectTime2, selectTime3, selectTime4, selectTime5]

        while '' in timeList:
            timeList.remove('')

        res = []
        for i in timeList:
            if i not in res:
                res.append(i)

        course = Course.objects.get(pk=selectCourse)
        courseOff = coursesoffered(user_name = request.user, coursePre = course, studentEnrollment = studentEnrollment )
        courseOff.save()

        for i in res:
            time = Time.objects.get(pk=i)
            courseOff.times.add( time )
            courseOff.save()

        messages.success(request,"Course Added Successfully.")
        return HttpResponseRedirect(reverse('addDetails'))
    else:
        context = {
            'coursesoff' : coursesoffered.objects.filter(user_name=request.user)
        }
        return render(request, "scheduling/coursesOffered.html", context)

@login_required(login_url="login")
def removeCoursesOffered(request, itemid):

    if request.method == "POST":
        courseToRemove = coursesoffered.objects.get(pk=itemid)
        courseToRemove.delete()

        messages.error(request,"Course removed Successfully.")
        return HttpResponseRedirect(reverse('coursesOffered'))
    else:
        context = {
            'coursesoff' : coursesoffered.objects.filter(user_name=request.user)
        }
        
        return render(request, "scheduling/coursesOffered.html", context)


# Add class Room
@login_required(login_url="login")
def addClassRoom(request):

    if request.method == "POST":
        
        classname = request.POST["classname"]
        capacity = request.POST["capacity"]
        classRoom = classRooms(user_name = request.user, class_name = classname, class_capacity = capacity  )
        classRoom.save()
        messages.success(request,"Class Room Added Successfully.")
        return HttpResponseRedirect(reverse('addDetails'))
    else:
        context = {
            'classRooms' : classRooms.objects.filter(user_name=request.user)
        }
        return render(request, "scheduling/viewclass.html", context)


@login_required(login_url="login")

def removeClasses(request, itemid):

    if request.method == "POST":
        classroomRemove = classRooms.objects.get(pk=itemid)
        classroomRemove.delete()

        messages.error(request,"Class Room removed Successfully.")
        return HttpResponseRedirect(reverse('addClassroom'))
    else:
        context = {
            'classRooms' : classRooms.objects.filter(user_name=request.user)
        }
        return render(request, "scheduling/viewclass.html", context)

# Add courses

@login_required(login_url="login")
def addCourses(request):

    if request.method == "POST":
        
        coursename = request.POST["coursename"]
        checkgraduate = request.POST["graduate"]

        if checkgraduate == "postgraduate":
            coursename = coursename + "(PG)"

        addcourse = Course(user_name = request.user, course_name = coursename, checkgraduate = checkgraduate)
        addcourse.save()
        messages.success(request,"Course Added Successfully.")
        return HttpResponseRedirect(reverse('addDetails'))
    else:
        context = {
            'courses' : Course.objects.filter(user_name = request.user)
        }
        return render(request, "scheduling/viewCourse.html", context)

@login_required(login_url="login")
def removeCourses(request, itemid):

    if request.method == "POST":
        
        course = Course.objects.get(pk=itemid)
        course.delete()
        messages.error(request,"Course removed Successfully.")
        return HttpResponseRedirect(reverse('addCoures'))
    else:
        context = {
            'courses' : Course.objects.filter(user_name = request.user)
        }
        return render(request, "scheduling/viewCourse.html", context)    

# Add Time Slots
@login_required(login_url="login")
def addTimeSlots(request):

    if request.method == "POST":
        timename = request.POST["timename"]
        addtime = Time(user_name = request.user, time= timename)
        addtime.save()
        messages.success(request,"Time Added Successfully.")
        return HttpResponseRedirect(reverse('addDetails'))
    else:
        context = {
            'times': Time.objects.filter(user_name = request.user)
        }
        return render(request, "scheduling/viewTimeSlots.html", context)

@login_required(login_url="login")
def removeTime(request, itemid):
    if request.method == "POST":
        print(itemid)
        times = Time.objects.get(pk=itemid)
        times.delete()
        messages.error(request,"Time slot removed Successfully.")
        return HttpResponseRedirect(reverse('timeSlots'))
    else:
        context = {
            'times': Time.objects.filter(user_name = request.user)
        }
        return render(request, "scheduling/viewTimeSlots.html", context)

# schedule

@login_required(login_url="login")
def schedule(request):
    
    coursesoff = coursesoffered.objects.filter(user_name=request.user)
    classrooms = classRooms.objects.filter(user_name=request.user)
    allTimes = Time.objects.filter(user_name=request.user)

    # courses offered
    coursesoffList = []
    for course in coursesoff:
        coursesDict = {}
        enrollAndTime = []
        graduate = []
        enroll = []
        graduate.append(course.coursePre.checkgraduate)
        enroll.append(course.studentEnrollment)
        enrollAndTime.append(graduate)
        enrollAndTime.append(enroll)
        times = []
        for i in course.times.all():
            times.append(i.time)
        enrollAndTime.append(times)
        coursesDict[course.coursePre.course_name] = enrollAndTime
        coursesoffList.append(coursesDict)
    # print("Course Offered -> ",coursesoffList)

    # class rooms Dict
    classroomsDict = {}
    for classroom in classrooms:
        classroomsDict[classroom.class_name] = classroom.class_capacity 
    # print("Class Rooms -> ",classroomsDict)


    # declaring schedule 
    schedule = []
    for i in range(len(classrooms)+1):
        time = []
        for j in range(len(allTimes)+1):
            time.append(-1)
        schedule.append(time)

    # Time Index
    timeIdx = {}

    # Class rooms Index 
    classroomsIdx = {}


    # Giveing Time to schedule list
    for i, time in zip(range(1, len(allTimes)+1), allTimes):
        schedule[0][i] = time.time
        timeIdx[time.time] = i

    # Giveing class rooms to schedule list
    for i, classroom in zip(range(1, len(classrooms)+1), classrooms):
        schedule[i][0] = classroom.class_name
        classroomsIdx[classroom.class_name] = i

    # To schdule post-graduate schedule if there is no time given then schedule at random time
    errorCheck = {}

    errorMessageList = []

    for i, time in zip(range(1, len(allTimes)+1), allTimes):
        schedule[0][i] = time.time
        errorCheck[time.time] = i

    # print(errorCheck)

    for course in coursesoffList:
        for i in course:
            if course[i][0][0] == 'postgraduate':

                requireClassCap = course[i][1][0]
                timeList = course[i][2]

                timeListStr = ', '.join(timeList)
                

                classRoom = ""
                minDiff = 500
                # print(course)
                if timeList :

                    
                    # check classroom and give time
                    for classroom in classroomsIdx:                    

                        diff = classroomsDict[classroom] - requireClassCap

                        if diff >= 0 and diff < minDiff:
                            minDiff = diff
                            classRoom = classroom

                        timecheckList = []

                        for ss in range(1, len(schedule[classroomsIdx[classroom]])):

                            if schedule[classroomsIdx[classroom]][ss] == -1 :
                                timecheckList.append(schedule[0][ss])
                        
                        for timecheck in timecheckList :
                            for time in timeList :
                                if timecheck == time:
                                    timePosition = True
                        
                        if diff >= 0 and diff < minDiff and timePosition == True:
                            minDiff = diff
                            classRoom = classroom 



                    if classRoom != "" :
                        count = 0
                        for time in course[i][2]:

                            schTime = timeIdx[time]
                            if errorCheck[time] != -1 :
                                if schedule[classroomsIdx[classRoom]][schTime] == -1 :
                                    schedule[classroomsIdx[classRoom]][schTime] = i
                                    errorCheck[time] = -1
                                    break
                                        

                                else:
                                    errorMessage = "No two Post-Graduate Course can be sechedule at same time "+i+" "+timeListStr
                                    errorMessageList.append(errorMessage)
                                    # print("No 2 Post-Graduate Course can be sechedule at same time -> ",i)
                            count += 1

                        if count == len(timeList):

                            errorMessage = "No two Post-Graduate Course can be sechedule at same time "+i+" "+timeListStr
                            errorMessageList.append(errorMessage)
                    
                    else:
                        errorMessage = "No Time slot is availabe "+i+" "+timeListStr
                        errorMessageList.append(errorMessage)
            
                else:
                    
                    for classroom in classroomsIdx:                    

                        diff = classroomsDict[classroom] - requireClassCap

                        if diff >= 0 and diff < minDiff:
                            minDiff = diff
                            classRoom = classroom

                        timecheckList = []

                        for ss in range(1, len(schedule[classroomsIdx[classroom]])):

                            if schedule[classroomsIdx[classroom]][ss] == -1 :
                                timecheckList.append(schedule[0][ss])

                        
                        if diff >= 0 and diff < minDiff :
                            minDiff = diff
                            classRoom = classroom 

                    classIdx = classroomsIdx[classRoom]

                    classoom_noTime = schedule[classIdx]
                    time_noTime = schedule[0]


                    if classRoom != "" :

                        for time in time_noTime[1:]:

                            schTime = timeIdx[time]
                            if errorCheck[time] != -1 :
                                if schedule[classroomsIdx[classRoom]][schTime] == -1 :
                                    schedule[classroomsIdx[classRoom]][schTime] = i
                                    errorCheck[time] = -1
                                    break
                                else:
                                    errorMessage = "No two Post-Graduate Course can be sechedule at same time "+i+" "+timeListStr
                                    errorMessageList.append(errorMessage)
                            else:
                                errorMessage = "No two Post-Graduate Course can be sechedule at same time "+i+" "+timeListStr
                                errorMessageList.append(errorMessage)
                    else:
                        errorMessage = "No Time slot is availabe "+i+" "+timeListStr
                        errorMessageList.append(errorMessage)
                    
    # To schedule under graduate

    for course in coursesoffList:
        for i in course:
            if course[i][0][0] == 'undergraduate':

                requireClassCap = course[i][1][0]
                timeList = course[i][2]

                classRoom = ""
                minDiff = 500
                # check classroom and give time
                if timeList:


                    for classroom in classroomsIdx:                    
                        
                        timePosition = False
                        currentClassRoomCap = classroomsDict[classroom]
                        diff = classroomsDict[classroom] - requireClassCap
                        timecheckList = []

                        for ss in range(1, len(schedule[classroomsIdx[classroom]])):


                            if schedule[classroomsIdx[classroom]][ss] == -1 :
                                timecheckList.append(schedule[0][ss])

                        for timecheck in timecheckList :
                            for time in timeList :
                                if timecheck == time :
                                    timePosition = True
        

                        if diff >= 0 and diff < minDiff and timePosition == True:
                            minDiff = diff
                            classRoom = classroom 

                    if classRoom != "" :
                        for time in timeList:
                            
                            schTime = timeIdx[time]
                            if schedule[classroomsIdx[classRoom]][schTime] == -1 :
                                schedule[classroomsIdx[classRoom]][schTime] = i
                                break
                    else:
                        errorMessage = "No Time slot is availabe "+i
                        errorMessageList.append(errorMessage)

                else:
                    
                    for classroom in classroomsIdx:                    

                        diff = classroomsDict[classroom] - requireClassCap

                        if diff >= 0 and diff < minDiff:
                            minDiff = diff
                            classRoom = classroom

                        timecheckList = []

                        for ss in range(1, len(schedule[classroomsIdx[classroom]])):

                            if schedule[classroomsIdx[classroom]][ss] == -1 :
                                timecheckList.append(schedule[0][ss])
                        
                        if diff >= 0 and diff < minDiff :
                            minDiff = diff
                            classRoom = classroom 



                    classIdx = classroomsIdx[classRoom]

                    classoom_noTime = schedule[classIdx]
                    time_noTime = schedule[0]



                    if classRoom != "" :
                        count = 0

                        for time in time_noTime[1:]:

                            schTime = timeIdx[time]


                            if schedule[classroomsIdx[classRoom]][schTime] == -1 :
                                schedule[classroomsIdx[classRoom]][schTime] = i
                                errorCheck[time] = -1
                                break
                            count += 1

                        if count == len(time_noTime[1:]):
                            errorMessage = "No Time slot is availabe "+i+" "+timeListStr
                            errorMessageList.append(errorMessage)
                            
                    else:
                        errorMessage = "No Time slot is availabe "+i+" "+timeListStr
                        errorMessageList.append(errorMessage)


    classRList = []
    for classR in classrooms:
        newClass = []
        newClass.append(classR.class_name)
        newClass.append(classR.class_capacity)
        classRList.append(newClass)

    scheduledCourses = []

    # for ss in schedule:
    for cc in range(1,len(schedule)):
        finalList = []
        for i in schedule[cc][1:]:
            if i == -1 :
                finalList.append("")
            else:
                finalList.append(i)
        scheduledCourses.append(finalList)

    for cR in range(len(scheduledCourses)):
        scheduledCourses[cR].insert(0, classRList[cR][0])
        scheduledCourses[cR].insert(1, classRList[cR][1])

    graduateCheck = {}
    for i in coursesoff:
        graduateCheck[i.coursePre.course_name] = i.coursePre.checkgraduate

    context = {
        'times' : allTimes,
        'classrooms' : classrooms,
        'class' : classRList,
        'scheduledCourses': scheduledCourses,
        'errorMessageList': errorMessageList,
        'graduateCheck': graduateCheck,
    }
    return render(request, "scheduling/schedule.html", context)
