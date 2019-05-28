import csv
#User input to pick which day & month to find differences for
UserMonth = 8
UserDay = 24
UserYear = 2018

#photodiode difference for each unit for 24 hour period
difference1 = [0]*86400
difference2 = [0]*86400
#difference3 = [0]*86400

#test these values for accuracy
MAX1 = 1869
MAX2 = 1844
MAX3 = 1881

#smoothing it out
datapoints1 = 0
datapoints2 = 0
total_1 = 0
total_2 = 0

#*****FIRST MAGNETOMETER UNIT*****
f1 = open("CleanAug15.txt", "r")

eof = False

LEFT = [0]*86401
RIGHT = [0]*86401
N = 0

while not eof:
    line = ""
    for data in f1.readline():
        line = line + data
    first = line.split("/")
    second = first[2].split(" ")
    
    monthint = int(first[0])
    dayint = int(first[1])
    yearint = int(second[0])

    time = second[1].split(":")
    
    hourint = int(time[0])
    minuteint = int(time[1])
    seconds = time[2].split("|")
    secondint = int(seconds[0])

    leftint = int(second[5])
    right = second[9].split("|")
    rightint = int(right[0])

    if dayint > UserDay and monthint == UserMonth:
        eof = True
    if monthint == UserMonth and dayint == UserDay and yearint == UserYear:
        N = secondint + (60*minuteint) + (3600*hourint)
        #opposite from other two units
        RIGHT[N]=rightint
        LEFT[N]=leftint
        #newcode
        if difference1[N] != 0:
            datapoints1 = datapoints1 -1
        if RIGHT[N] < 100 and LEFT[N] < 100:
            difference1[N] = ""
        elif abs(RIGHT[N] - LEFT[N]) < 6:
            difference1[N] = 0
        elif RIGHT[N] > LEFT[N]:
            difference1[N] = (MAX1 - RIGHT[N]) + (MAX1 - LEFT[N])
        else:
            difference1[N] = -1*((MAX1 - RIGHT[N]) + (MAX1 - LEFT[N]))
        datapoints1 = datapoints1 + 1
print('Done with one')

#*****SECOND MAGNETOMETER UNIT*****
f2 = open("Aug15_2.txt", "r")

eof = False

LEFT = [0]*86401
RIGHT = [0]*86401
N = 0

while not eof:
    line = ""
    for data in f2.readline():
        line = line + data
    first = line.split("/")
    second = first[2].split(" ")
    
    monthint = int(first[0])
    dayint = int(first[1])
    yearint = int(second[0])

    time = second[1].split(":")
    
    hourint = int(time[0])
    minuteint = int(time[1])
    secondint = int(time[2])


    reading = first[2].split("|")
    leftint = int(reading[1])
    rightint = int(reading[2])

    if dayint > UserDay and monthint == UserMonth:
        eof = True
    if monthint == UserMonth and dayint == UserDay and yearint == UserYear:
        N = secondint + (60*minuteint) + (3600*hourint)
        #opposite
        RIGHT[N]=leftint
        LEFT[N]=rightint
        #newcode
        if difference2[N] != 0:
            datapoints2 = datapoints2 -1
        if RIGHT[N] < 100 and LEFT[N] < 100:
            difference2[N] = ""
        elif abs(RIGHT[N] - LEFT[N]) < 6:
            difference2[N] = 0
        elif RIGHT[N] > LEFT[N]:
            difference2[N] = (MAX2 - RIGHT[N]) + (MAX2 - LEFT[N])
        else:
            difference2[N] = -1*((MAX2 - RIGHT[N]) + (MAX2 - LEFT[N]))
        datapoints2 = datapoints2 + 1

for n in difference1:
    if n == "":
        total_1 = total_1
    else:
        total_1 = total_1 + n
for n in difference2:
    if n == "":
        total_1 = total_1
    else:
        total_2 = total_2 + n
dailyavg1 = total_1/datapoints1
dailyavg2 = total_2/datapoints2

print(dailyavg1)
print(dailyavg2)

average1 = [0.0]*144
average2 = [0.0]*144
count1 = 0
count2 = 0

temp = 0.0
m = 1
while m < 86401:
    if difference1[m-1] == "":
        count1 = count1
    else:
        temp = temp + difference1[m-1]
        count1 = count1 + 1
    if m%600 == 0:
        average1[int(m/600)-1] = float(temp/count1)
        temp = 0
        count1 = 0
    m = m + 1
#average1[int(m/600)-1] = temp/count1

temp = 0.0
m = 1
while m < 86401:
    if difference2[m-1] == "":
        count2 = count2
    else:
        temp = temp + difference2[m-1]
        count2 = count2 + 1
    if m%600 == 0:
        average2[int(m/600)-1] = float(temp/count2)
        temp = 0
        count2 = 0
    m = m + 1
#average2[int(m/600)-1] = temp/count2
        
diffstr = [""]*144 #every two seconds
for d in range(144):
        diffstr[d] = [str(average1[d]), str(average2[d])]

DATA = open("smooth_24.csv", "w")
with DATA:
    writer = csv.writer(DATA)
    writer.writerows(diffstr)
print("complete")
