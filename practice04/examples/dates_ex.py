#1 Write a Python program to subtract five days from current date.
from datetime import date, timedelta
current_date = date.today()
new_date = current_date - timedelta(days=5)
print("Current date:", current_date)
print("Subtract five days from current date:", new_date)

#2 Write a Python program to print yesterday, today, tomorrow.
from datetime import date, timedelta
today = date.today()
yesterday = today - timedelta(days=1)
tomorrow = today + timedelta(days=1)
print("Yesterday:", yesterday)
print("Today:", today)
print("Tomorrow:", tomorrow)

#3 Write a Python program to drop microseconds from datetime.
from datetime import datetime
now = datetime.now()
without_microseconds = now.replace(microsecond=0)
print("Original datetime:", now)
print("Without microseconds:", without_microseconds)

#4 Write a Python program to calculate two date difference in seconds.
from datetime import datetime
date1_str = input("Enter first date (YYYY-MM-DD HH:MM:SS): ")
date2_str = input("Enter second date (YYYY-MM-DD HH:MM:SS): ")
date1 = datetime.strptime(date1_str, "%Y-%m-%d %H:%M:%S")
date2 = datetime.strptime(date2_str, "%Y-%m-%d %H:%M:%S")
difference = date2 - date1
seconds = abs(difference.total_seconds())
print("Difference in seconds:", int(seconds))