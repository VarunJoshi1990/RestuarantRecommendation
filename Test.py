# -*- coding: utf-8 -*-
"""
Created on Thu May 05 19:39:05 2016

@author: Varun Joshi
"""
 
import pandas as pd
import random
import time
from scipy.spatial.distance import cosine

#Getting score
def getCosScore(his, simi):
   return sum(his*simi)/sum(simi)
 
# Initialisation #
data = pd.read_csv('r.csv')
rest = open('restaurants.txt','r')
freq=[]
restList=[]

rest.readline()
for l in rest:
    l=l.split(";")
    print l
    x=float(l[2])
    y=float(l[3].strip())
    print l[1]
    print (x**2+y**2)
    restList.append([l[0],l[1],(x**2+y**2)])

for i in data.ix[0]:
    if i == 0:
        freq.append(0)
    else:
        freq.append(1)
    
# Finding neighborhood #
# For computation we dont need the reviewer column

data_update = data.drop('Reviewer', 1)
data_update =data_update.astype(float)


# Finding for 1000 iterations, each time with updated ratings

count=0
prev=[]
while count<1000:
    #item based similarity
    data_is = pd.DataFrame(index=data_update.columns,columns=data_update.columns)

# Filling in with cosine values
    for i in range(0,len(data_is.columns)) :
        for j in range(0,len(data_is.columns)):
            #Similarity between item i and item j i.e restaurant i and restaurant j
            data_is.ix[i,j] = 1-cosine(data_update.ix[:,i],data_update.ix[:,j])
    #print data_is
    data_neigh = pd.DataFrame(index=data_is.columns,columns=[range(1,16)])
 
    for i in range(0,len(data_is.columns)):
        data_neigh.ix[i,:15] = data_is.ix[0:,i].order(ascending=False)[:15].index
    #print data_neigh
# Finding neighborhood done #
 
# Get the ratings for the missing values for "you" 

    data_sim = pd.DataFrame(index=data.index,columns=data.columns)
    data_sim.ix[:,:1] = data.ix[:,:1]
    #print data_sim
#If there is rating already present then keep the same else find the value based on similarity
    for i in range(0,len(data_sim.index)):
        for j in range(1,len(data_sim.columns)):
            rev = data_sim.index[i]
            rating = data_sim.columns[j]
 
            if data_update.ix[i][j-1] > 0:
                data_sim.ix[i][j] = data_update.ix[i][j-1]
            else:
                top_sim_rest = data_neigh.ix[rating][1:15]
                top_sim_vals = data_is.ix[rating].order(ascending=False)[1:15]
                user_rev = data_update.ix[rev,top_sim_rest]
                data_sim.ix[i][j] = getCosScore(user_rev,top_sim_vals)
    #print data_sim
# Get the top recommendations in order
    data_rec = pd.DataFrame(index=data_sim.index, columns=['Reviewer','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15'])
    data_rec.ix[0:,0] = data_sim.ix[:,0]
    
    ratings=[]
# Get the top recommendations for the user
#If the distance is less than 0.5 - add 1 point to the score prev calc
# 0.5 to 1 - 0.75 point
# 1 to 2 - 0.5 point
# 2 to 4 - 0.25 point
# >4    - 0 point
    for j in range(1,len(data_sim.columns)):
        if restList[j-1][2]<4:
            data_sim.set_value(i,chr(ord('A')+j-1),data_sim.ix[0][j]+0.25)
        if restList[j-1][2]<2:
            data_sim.set_value(i,chr(ord('A')+j-1),data_sim.ix[0][j]+0.25)
        if restList[j-1][2]<1:
            data_sim.set_value(i,chr(ord('A')+j-1),data_sim.ix[0][j]+0.25)
        if restList[j-1][2]<0.5:
            data_sim.set_value(i,chr(ord('A')+j-1),data_sim.ix[0][j]+0.25)
        
        ratings.append(data_sim.ix[0][j]*10)   #Multiply by 10 for visualisation purpose
    print data_sim.ix[0]
    data_rec.ix[0,1:] = data_sim.ix[0,:].order(ascending=False).ix[1:16,].index.transpose()
        
    
    print count
    print data_rec.ix[:0,:16] #printing the recommendation in descending order
    
    r=random.randint(1,5)
    #If the same restaurant is recommended continuously more than 2 then 2nd best recommendation is considered
    #This is same as real life where you won't visit the same restaurant more than 2 times in a row
    if len(prev)==0:
        prev.append(data_rec.ix[0][1])
        prev.append(1)
    else:
        if prev[0]==data_rec.ix[0][1]:
            if prev[1]==2:
                prev[0]=data_rec.ix[0][2]
                #print data_recommend.ix[0][2]
                prev[1]=1
            else:
                prev[1]=2
        else:
            prev[0]=data_rec.ix[0][1]
            prev[1]=1

    new_rating=float(data_update[prev[0]][0]*freq[ord(prev[0])-ord('A')]+r)/float(freq[ord(prev[0])-ord('A')]+1)
    freq[ord(prev[0])-ord('A')]+=1

    data_update.set_value(0,prev[0],new_rating)
    
    count+=1
    h="""<head><!-- Load c3.css -->
    <link href=".\c3-0.4.11\c3.css" rel="stylesheet" type="text/css">

    <!-- Load d3.js and c3.js -->
    <script src="https://d3js.org/d3.v3.min.js" charset="utf-8"></script>
    <script src=".\c3-0.4.11\c3.min.js"></script>
    </head>
    <body>
    <p> The current iteration is: """+str(count)+"""</p><p>The current recommendation is: """+str(prev[0])+"""</p>
    <div id="chart" height=600px></div>
    <script>

    var chart = c3.generate({
    data: {
        columns: [
            ['freq',
            """
            
    f=str(freq[:-1])[1:-1]
    h1="""], 
        ['rating (x10)',
        """    
    rat=str(ratings)[1:-1]
            
    h2="""],
            ['dist (x10)', 17.674,38.9,62.7,13.2,3.8,21.8,24.4,12,25.1,.7,8.4,33.4,16.23,56.1,15.7],
        ],
        type: 'bar',
        types: {
            'dist (x10)': 'line',
            'rating (x10)': 'line',
        }
    }
});

</script>
</body>
  """
    out=open("index1.html","w")
    out.write(h+f+h1+rat+h2)
    out.close()
    time.sleep(2)
