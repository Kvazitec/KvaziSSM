from datetime import timedelta, datetime
import time
now_date = "00:00:00/01/01/2000"
start_date = datetime.strptime(now_date, "%H:%M:%S/%d/%m/%Y")
current_date = start_date
lasttime = time.time()
while True:
    if time.time() - lasttime > 1:
        current_date += timedelta(seconds=3600)
        now_date = current_date.strftime("%H:%M:%S/%d/%m/%Y")
        print(now_date)