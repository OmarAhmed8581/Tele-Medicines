from datetime import datetime

array=['2020-11-28','2014-7-14','2018-9-25']
array.sort(key=lambda date:datetime.strptime(date,"%Y-%m-%d"))
print(array)
