import tle2czml
from datetime import datetime

# You can specify the time range you would like to visualise
start_time = datetime(2020, 6, 3, 11, 5)
end_time = datetime(2020, 6, 4, 11, 5)
tle2czml.create_czml("tle.txt", start_time=start_time, end_time=end_time)