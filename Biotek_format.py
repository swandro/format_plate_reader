#Stephen Wandro 12/26/16
###Format the raw OD file so it can be easily graphed
##Biotek plate reader in the anaerobic chamber
##Export only one OD at a time. Id you have more than 1 OD reading,
##export them as separate text files and run this script multiple times


import sys
from itertools import islice

#Final lists
time = [] #list of times
OD = []  #List of lists. Outer list is each well. Inner lists, ODs.

def process_plate(plate:[str]):
    #Takes 9 lines as a plate and appends the result lists
    time.append(plate[1].split()[-1][1:-1])
    OD_list = []
    for line in plate[3:11]:
        OD_list.extend(line.split('\t')[1:13])
    OD.append(OD_list)

#Go through the file and process the text into lists
with open(sys.argv[1],'r') as openfile:
    while True:
        plate = list(islice(openfile, 12))
        if not plate:
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
print("Hours\tMinutes\t" + wells[:-1])

#Print the data
for i in range(len(time)):
    print(str(round(Hours[i],2)) + '\t' + str(Minutes[i]) + '\t' + '\t'.join(OD[i]))

  
    




