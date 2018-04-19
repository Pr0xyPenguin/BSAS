import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from scipy.signal import argrelextrema
from scipy.spatial import distance
import random

#
#
#COMMENTS
#TO
#BE
#ADDED
#
#

def bsas(threshold):
    list_of_clusters = []
    list_of_clusters = list_of_clusters + [Users[0][1:]]
    clusteredusers = []
    clusteredusers = clusteredusers + [[Users[0][0]]]
    for i in range(1, len(Users)):
        min_temp_dist = 10000
        for j in range( len(list_of_clusters)):
            dst = distance.euclidean(Users[i][1:],list_of_clusters[j])
            if dst < min_temp_dist:
                min_temp_dist = dst
                key = j
        if min_temp_dist>threshold and len(list_of_clusters)<maxcls:
            list_of_clusters = list_of_clusters + [[Users[i][1:]]]
            clusteredusers = clusteredusers + [[Users[i][0]]]
        else:
            clusteredusers[key] = clusteredusers[key] + [Users[i][0]]
            n=(len(clusteredusers[key]))
            list_of_clusters[key] = (n/(n+1)*np.array(list_of_clusters[key])) + (np.array(Users[i][1:])/(n+1))





#--------------------------------------------------------------#

f = open('u.item', encoding='ISO-8859-14')
lines=f.readlines()
Categories = []
for line in lines:
    temp = line[len(line)-38:-1].split('|')
    Categories = Categories + [temp]

#--------------------------------------------------------------#

f = open('u.data', 'r')
lines=f.readlines()
Users = []
cur_u = 0

for line in lines:
    temp = line.split(',')
    if int(temp[2]) >= 3:
        add = list(map(int,[temp[0]] + Categories[int(temp[1])-1]))
    else:
        continue
    if int(temp[0]) != cur_u:
        Users = Users + [add]
        if cur_u > 0:
            Sum = sum(Users[cur_u-1][1:])
            Users[cur_u-1][1:] = np.divide(Users[cur_u-1][1:],Sum)
        cur_u +=1;
    else:
        Users[cur_u-1][1:] =(np.array(Users[cur_u-1][1:]) + np.array(add[1:])).tolist()
Users[len(Users)-1][1:] = np.divide(Users[len(Users)-1][1:],sum(Users[len(Users)-1][1:]))

#--------------------------------------------------------------#

mini = 10
maxi = 0
for i in range(len(Users)):
    for j in range (len(Users)):
        if i == j:
            continue
        apos = distance.euclidean(Users[i][1:],Users[j][1:])
        if apos > maxi:
            maxi = apos
        if apos < mini:
            mini = apos
print(mini)
print(maxi)
tmin = mini + 0.25*(maxi-mini)
tmax = mini + 0.75*(maxi-mini)
print(tmin)
print(tmax)
pollatheta = np.arange(tmin,tmax,0.01)
print(pollatheta)
#--------------------------------------------------------------#

maxcls=10;
list_of_clusters = []
list_of_clusters = list_of_clusters + [Users[0][1:]]
key = 0
dst = 0
clusteredusers = []
clusteredusers = clusteredusers + [[Users[0][0]]]
clstr = []

print('======================================')
#--------------------------------------------------------------#

for l in pollatheta:
    threshold = l
    list_of_clusters = []
    list_of_clusters = list_of_clusters + [Users[0][1:]]
    for i in range(1, len(Users)):
        min_temp_dist = 10000
        for j in range( len(list_of_clusters)):
            dst = distance.euclidean(Users[i][1:],list_of_clusters[j])
            if dst < min_temp_dist:
                min_temp_dist = dst
                key = j
        if min_temp_dist>threshold and len(list_of_clusters)<maxcls:
            list_of_clusters = list_of_clusters + [[Users[i][1:]]]
            clusteredusers = clusteredusers + [[Users[i][0]]]
        else:
            clusteredusers[key] = clusteredusers[key] + [Users[i][0]]
            list_of_clusters[key] = ((np.array(Users[i][1:])+np.array(list_of_clusters[key]))/2)
    clstr = clstr + [len(list_of_clusters)]

print(len(clstr))
print(len(pollatheta))

print(np.bincount(clstr).argmax())
length = 0
for i in range(len(clstr)):
    if clstr[i] != np.bincount(clstr).argmax():
        length = i-1
        break
threshold_final = 0.0
for i in range(length+1):
    threshold_final = threshold_final + pollatheta[i]
threshold_final = np.divide(threshold_final , length+1)
print(threshold_final)

plt.plot(pollatheta,clstr)
plt.show()
bsas(threshold_final)
