#1 datetime Module
import datetime

x = datetime.datetime.now()

print(x)


#2 Creating Date Objects
x = datetime.datetime(2020, 5, 17)
print(x)


#3 Date Formatting
x = datetime.datetime(2018, 6, 1)
print(x.strftime("%B"))


#4 Calculate the time difference in hours, minutes and seconds
from datetime import datetime

start = datetime.strptime("4:25:40", "%H:%M:%S")
end = datetime.strptime("11:40:10", "%H:%M:%S")

difference = end - start

seconds = difference.total_seconds()
print('difference in seconds is:', seconds)

minutes = seconds / 60
print('difference in minutes is:', minutes)

hours = seconds / (60 * 60)
print('difference in hours is:', hours)


#5 Calculate the time interval between two given times
from datetime import datetime

start = "2:13:57"
end = "11:46:38"

time1 = datetime.strptime("6:20:50", "%H:%M:%S")
print('Start time is :', time1.time())

time2 = datetime.strptime("11:56:18", "%H:%M:%S")
print('End time is :', time2.time())

delta = time2 - time1

print("Time difference in seconds is", delta.total_seconds(), "seconds")


#6 Using the divmod( ) function
import datetime
  
time1 = datetime.datetime(2018, 10, 12, 20, 15, 40)
time2 = datetime.datetime(2015, 2, 10, 15, 41, 30)

difference = time1 - time2 
print('Difference is : ', difference)
  
minutes = divmod(difference.total_seconds(), 60) 
print('Difference in minutes: ', minutes[0],
      'minutes', minutes[1], 'seconds')
  
minutes = divmod(difference.seconds, 60) 
print('Total difference in minutes: ', minutes[0], 'minutes',minutes[1], 'seconds')


#7 Working with Timezones
import datetime

x = datetime.datetime.now()

print(x.strftime("%c"))
print(x.year)