# Get data from UT Tyler
import json
import time
import datetime
import requests
from pyquery import PyQuery
import re
import sys

#########################################################
# Authentication
#########################################################

def myuttyler_authenticate(username, password):
  ''' 
  Authenticate username and password. Returns a cookie object if authentication
  is successful, Boolean False otherwise. 
  >>> user = "myuser"
  >>> pw = "mypass!"
  >>> cookies = myuttyler_authenticate(user, pw)
  >>> if(cookies):
  >>>   print("Logged in!")
  >>> else:
  >>>   print("Bad login!")
  '''

  data = {"userid": username, "pwd": password}
  loginURL = "https://sis-portal-prod.uttyler.edu/psp/TAPPRD/EMPLOYEE/EMPL/?&cmd=login&languageCd=ENG"

  # Don't allow redirects: We need to get the cookies from the initial response.
  r = requests.post(loginURL, data=data, allow_redirects=False)

  # If we're instructed to redirect to this specific address, login was good.
  if r.headers['location'] == "https://sis-portal-prod.uttyler.edu/psp/TAPPRD/EMPLOYEE/EMPL/h/?tab=DEFAULT":
    return r.cookies
  else:
    return False

def blackboard_authenticate(username, password):
  ''' 
  Authenticate username and password. Returns a cookie object if authentication
  is successful, Boolean False otherwise. 
  '''

  data = {"user_id": username, "password": password} 

  # Hardcoded stuff observed through Dev tools
  data["login"] = "Login"
  data["action"] = "login"

  loginURL = "https://blackboard.uttyler.edu/webapps/login/"

  # Don't allow redirects: We need to get the cookies from the initial response.
  r = requests.post(loginURL, data=data, allow_redirects=False)

  # Upon observation, we can use the content-type to differentiate between a 
  # successful and bad login.
  if r.headers['content-type'] == "text/html":
    return r.cookies
  else:
    return False

#########################################################
# MyUTTyler
#########################################################
def student_center(cookies):
  '''
  Pass in valid cookies after authentication and recieve a PyQuery object for
  parsing
  '''

  # Extremely long URL, courtesy of Oracle.
  summaryURL = "https://sis-cs-prod.uttyler.edu/psc/TCSPRD/EMPLOYEE/HRMS/c/SA_LEARNER_SERVICES.SSS_STUDENT_CENTER.GBL?PORTALPARAM_PTCNAV=UTT_STUDENT_CENTER&amp;EOPP.SCNode=EMPL&amp;EOPP.SCPortal=EMPLOYEE&amp;EOPP.SCName=UTT_SYSTEM_ACCESS&amp;EOPP.SCLabel=System%20Access&amp;EOPP.SCPTfname=UTT_SYSTEM_ACCESS&amp;FolderPath=PORTAL_ROOT_OBJECT.UTT_SYSTEM_ACCESS.UTT_STUDENT_CENTER&amp;IsFolder=false&amp;PortalActualURL=https%3a%2f%2fsis-cs-prod.uttyler.edu%2fpsc%2fTCSPRD%2fEMPLOYEE%2fHRMS%2fc%2fSA_LEARNER_SERVICES.SSS_STUDENT_CENTER.GBL&amp;PortalContentURL=https%3a%2f%2fsis-cs-prod.uttyler.edu%2fpsc%2fTCSPRD%2fEMPLOYEE%2fHRMS%2fc%2fSA_LEARNER_SERVICES.SSS_STUDENT_CENTER.GBL&amp;PortalContentProvider=HRMS&amp;PortalCRefLabel=Student%20Center&amp;PortalRegistryName=EMPLOYEE&amp;PortalServletURI=https%3a%2f%2fsis-portal-prod.uttyler.edu%2fpsp%2fTAPPRD%2f&amp;PortalURI=https%3a%2f%2fsis-portal-prod.uttyler.edu%2fpsc%2fTAPPRD%2f&amp;PortalHostNode=EMPL&amp;NoCrumbs=yes&amp;PortalKeyStruct=yes"

  r = requests.get(url=summaryURL, cookies=cookies)
  jQuery = PyQuery(r.content)
  return jQuery

def get_myutt_info(myutt_cookies):
  studentCenter = student_center(myutt_cookies)
  summary = account_summary(studentCenter)
  todo = todo_list(studentCenter)
  schedule = get_schedule(studentCenter)
  info = {}
  info["summary"] = summary
  info["todo"] = todo
  info["schedule"] = schedule
  return info

def account_summary(jQuery):
  '''
  Returns a simple financial account summary that returns a dictionary with the
  following keys:
    "due": How much due overall
    "dueNow": How much due now
    "dueFuture": How much due in the future

  Pass in the jQuery object for the student center
  >>> studentCenter = student_center(cookies)
  >>> summary = account_summary(studentCenter)
  >>> print(summary)
  '''

  # Get amount owed. Example: You owe 1,718.00.
  due = jQuery("#SSF_SS_DERIVED_SSF_MESSAGE_TEXT").text()

  if not due:
    return False

  due = due[:-1].replace("You owe ", "")
  dueNow = jQuery("#SSF_SS_DERIVED_SSF_AMOUNT_TOTAL2").text()
  dueFuture = jQuery("#SSF_SS_DERIVED_SSF_AMOUNT_TOTAL3").text()

  returnDict = {
      "due": due,
      "dueNow": dueNow,
      "dueFuture": dueFuture
  }
  return returnDict

def todo_list(jQuery):
  '''
  Return a list of todo items. 
  Pass in the jQuery object for the student center
  >>> studentCenter = student_center(cookies)
  >>> todo = todo_list(studentCenter)
  >>> print(todo)
  '''

  todos = jQuery("div[id^='win0divSRVCIND_TODO_VW_DESCR']")
  return [jQuery(x).text() for x in todos]

def get_schedule(jQuery):
  '''
  Return a schedule list.
  Pass in the jQuery object for the student center
  >>> studentCenter = student_center(cookies)
  >>> schedule = schedule(studentCenter)
  >>> print(schedule)
  '''
  dateList = ["Mo", "Tu", "We", "Th", "Fr", "TBA"]
  neatDates = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "TBA"]

  courseName = [jQuery(x).text().encode('ascii', 'ignore') for x in jQuery("div[id^='win0divCLASS_NAME']")]
  courseInfo = [jQuery(x).text().encode('ascii', 'ignore') for x in jQuery("span[id^='DERIVED_SSS_SCL_SSR_MTG_SCHED_LONG']")]

  # With all the data together, we can start parsing.
  courses = []
  for date in neatDates:
    courses.append((date, []))

  for courseData in zip(courseName, courseInfo):
    namestr = courseData[0]
    subject = namestr[0:4]
    courseNum = int(namestr[5:9])
    data = courseData[1].split(' ')
    classTime = "".join(data[1:4])
    rawDates = data[0].encode('ascii', 'ignore')
    location = " ".join(data[4:])
    dates = [rawDates[x:x+2] for x in xrange(0,len(rawDates),2)]

    # Room to be announced
    if rawDates == "Room:":
      dates = ["TBA"]

    for date in dates:
      course = {
        "subject" : subject,
        "courseNum": courseNum,
      }

      if date == "TBA":
        course["date"] = "TBA"
        course["time"] = "TBA"
        course["startTime"] = time_struct("12:00AM")
      else:
        course["time"] = classTime
        course["startTime"] = time_struct(data[3])
        course["location"] = location
      courses[dateList.index(date)][1].append(course)

  for i,x in enumerate(courses):
    x[1].sort(course_order)
  return courses

def time_struct(timeStr):
  '''
  Return a time structure. "hour", "minutes", "ampm". Pass in a time string
  like "8:45PM"
  '''
  hour = int(timeStr.split(':')[0])
  minutes = int(timeStr[-4:-2])
  pm = int(timeStr[-2:].upper() == "PM")
  if (hour == 12):
    if not pm:
      hour = 0
  else:
    hour += (12 * pm)

  return {"hour":hour, "min":minutes, "str":timeStr}

def course_order(c1, c2):
  return compare_time_structs(c1["startTime"], c2["startTime"])

def compare_time_structs(ts1, ts2):
  atts = ["hour", "min"]
  for attr in atts:
    if ts1[attr] > ts2[attr]:
      return 1
    elif ts1[attr] < ts2[attr]:
      return -1
  return 0


#########################################################
# Blackboard Announcements
#########################################################
def get_announcements(blackboard_cookies):
  '''
  Pass in valid blackboard_cookies after authentication and recieve a list of
  dictionaries representing blackboard announcements.
  '''

  url = "https://blackboard.uttyler.edu/webapps/blackboard/execute/announcement?method=search&context=mybb&viewChoice=3"

  r = requests.get(url=url, cookies=blackboard_cookies)
  announcementHTML = r.content
  return parse_announcement_html(announcementHTML)

def parse_announcement_html(announcementHTML):
  jQuery = PyQuery(announcementHTML)

  announcements = []
  announcementLIs = jQuery("ul#announcementList").children("li")
  now = datetime.datetime.utcnow()

  for li in announcementLIs:
    date = jQuery(li).find(".details p").eq(0)
    jQuery(date).children("span").remove()
    date = date.text()
    # 'Friday, September 14, 2012'
    dateObj = time.strptime(date.lower(), "%A, %B %d, %Y")
    timestamp = int(time.mktime(dateObj))
    dtObj = datetime.datetime.fromtimestamp(timestamp)

    title = jQuery(li).children("h3").text()
    details = jQuery(li).find(".vtbegenerated").text()

    # details aren't necessarily provided
    if details:
        details = details.encode("ascii", "xmlcharrefreplace").replace("&#160;", " ")

    course = jQuery(li).find("span.courseId").text()
    
    # Some announcements are general and don't have a course.
    if course:
        course = course.split('-')[-2:]
        course = " ".join(course)
    

    if now - dtObj <= datetime.timedelta(weeks=2):
      announcements.append({
        "title":title,
        "details":details,
        "timestamp":timestamp,
        "date":date,
        "course":course
      })
  return sorted(announcements, key=lambda k: k['timestamp'], reverse=True)

 

#########################################################
# Blackboard Grades
#########################################################
def get_grades(blackboard_cookies):
    gradelist = []
    courses = get_course_urls(blackboard_cookies)
    for name,url in courses:
        # Retrieve SOFTWARE DEVELOPMENT from "2013-SPRING-COSC-4336.001 (SOFTWARE DEVELOPMENT)"
        grades = get_grades_from_url(url, blackboard_cookies)
        if grades:
            gradelist.append((name, grades))
    # Sort courses by the timestamp of the most recent grade for that course
    return sorted(gradelist, key=lambda k: k[1][0]['timestamp'], reverse=True)

def get_course_urls(blackboard_cookies):
  courseListURL = "https://blackboard.uttyler.edu/webapps/portal/execute/tabs/tabAction"
  gradeURLPattern = "https://blackboard.uttyler.edu/webapps/bb-mygrades-bb_bb60/myGrades?course_id=%s&stream_name=mygrades&is_stream=false"
  data = {'action': 'refreshAjaxModule', 'tabId': '_2_1', 'modId': '_4_1',
          'tab_tab_group_id': '_3_1'}
  haveData = False
  retries = 3
  retryCount = 0
  while not haveData and retryCount < retries:
      try:
          r = requests.post(url=courseListURL, cookies=blackboard_cookies, data=data)

          # Strip cdata and xml 
          content = r.content[44:-14]
          jQuery = PyQuery(content)
          links = jQuery(".courseListing > li > a")

          courses = []

          # Course ID in the anchor href, name in anchor text
          for a in links:
              name = jQuery(a).text().split(":")[1].strip()
              href = jQuery(a).attr("href")
              courseID = re.search(r'id%3D([^%]+)%', href).groups()[0]
              gradesURL = gradeURLPattern % courseID
              courses.append((name, gradesURL))
          haveData = True
      except IndexError:
          retryCount += 1
          time.sleep(3)

  if retryCount == retries:
      return []
  else:
      return courses

  
def get_grades_from_url(courseURL, cookies):
    gradeRequest = requests.get(url=courseURL, cookies=cookies)
    return parse_grades_html(gradeRequest.content)

def parse_grades_html(gradeHTML):
    jQuery = PyQuery(gradeHTML)
    items = jQuery(".has-stats > div.grade-item")

    # Only items with timestamps are actual grades
    items = [jQuery(x) for x in items if jQuery(x).find("span.timestamp").text()]
    grades = []

    for item in items:
        title = item.children(".name").text()
        grade = item.find(".gradeCellGrade").remove("span.grade-label").text()

        date = item.find("span.timestamp").text()
        dateObj = time.strptime(date.lower(), "%b %d, %Y %I:%M %p")
        timestamp = int(time.mktime(dateObj))

        grades.append({
            "title":title,
            "grade":grade,
            "date":date,
            "timestamp":timestamp
        })
    return sorted(grades, key=lambda k: k['timestamp'], reverse=True)

