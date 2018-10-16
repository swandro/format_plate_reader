##Stephen Wandro 12/26/16
###Format the raw OD file so it can be easily graphed
###Biotek plate reader (usually ambient)

import sys
from itertools import islice

#Final lists
time = [] #list of times
temperature = []  #list of temperatures
OD = []  #List of lists. Outer list is each well. Inner lists, ODs.

def process_plate(plate:[str]):
    #Takes 9 lines as a plate and appends the result lists
    time.append(plate[0].split()[0])
    temperature.append(plate[0].split()[1])
    OD_list = plate[0].split()[2:]
    for line in plate[1:]:
        OD_list.extend(line.split())
    OD.append(OD_list)

#Go through the file and process the text into lists
with open(sys.argv[1],'r', encoding = 'iso-8859-1') as openfile:
    i = 0 #Glocal line count
    while True:
        line = openfile.readline().strip()
        if line[0:4] == "Time":
            break
    while True:
        plate = list(islice(openfile, 9))
        if not plate or plate[0][0]=="~":
            break
        process_plate(plate)

#Format the time
Hours = []
Minutes = []
for moment in time:
    moment_split = moment.split(':')
    h, m = 0, 0
    m += int(moment_split[-1])/60 + int(moment_split[-2])
    h += int(moment_split[-1])/3600 + int(moment_split[-2])/60
    try:
        m += int(moment_split[-3])*60
        h += int(moment_split[-3])
    except IndexError:
        pass
    Hours.append(h)
    Minutes.append(m)
        
    

#Print the header
print(sys.argv[1])
wells = ''
for letter in "ABCDEFGH":
    for number in range(1,13):
        wells += letter + str(number) + '\t'
print("Reading\tHours\tMinutes\tTemperature\t" + wells[:-1])

#Print the data
for i in range(len(time)):
    print(str(i+1) + '\t' + str(round(Hours[i],2)) + '\t' + str(Minutes[i]) + '\t' +
          str(temperature[i]) + '\t' + '\t'.join(OD[i]))

  
    




