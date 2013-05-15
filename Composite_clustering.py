import sys
import json
import requests0 as requests
import simplejson
import difflib
import re
import collections
import math
import numpy
import operator
import random


idf_dictionary=collections.defaultdict(float)
docClass=collections.defaultdict(dict)
document_list=collections.defaultdict(dict)
title_list = collections.defaultdict(dict)
cluster = [[]]
mini_cluster = []

def document_parsing(r):

    d = collections.defaultdict(float)
    set_list1 = set(r);
           
    for word in set_list1:
        if idf_dictionary.has_key(word):
           idf_dictionary[word]+=1;
        else:
           idf_dictionary[word]=1;
   
    # We will create a term frequency dictionary here

    for wrd in r:
        if  wrd not in d:
            d[wrd]=1
        else:
            d[wrd]+=1

    # Now we will convert it to log form

    for ky in d:
        value = d[ky]
        d[ky]=1+float(math.log(value,2))

      
    return d

def bing_search_clustering(fileName):
 
    d = collections.defaultdict(float)
    list=[]
    
    count =0
    docId = 0

    for i in range(30):
 	docClass[i]="texas longhorns"
    
    for i in range(30,60):
 	docClass[i]="texas aggies"
    
    for i in range(60,90):
 	docClass[i]="dallas cowboys"
    
    for i in range(90,120):
 	docClass[i]="dallas mavericks"
    
    for i in range(120,150):
 	docClass[i]="duke blue devils"

    count = 0
    lines = [line.strip() for line in open(fileName)]
      
    for line in lines:
        news=json.loads(line)
        text=news['Title']+' '+news['Description']
        wordlist=word_preprocessing(text)       
        document_list[docId] = document_parsing(wordlist)
        title_list[docId] = news['Title']
        docId+=1
        count+=1

    
        
    
    for key in idf_dictionary:
        val = len(document_list)/float(idf_dictionary[key])
        idf_dictionary[key]=math.log(val,2)


    for i in range(0,len(document_list)):
        for key in document_list[i]:
            if key in idf_dictionary:
               idf_value = idf_dictionary[key]    # We are getting the idf value for that term
            else:
               idf_value = 0
            
            document_list[i][key] = float(document_list[i][key]) * float(idf_value)
            

    # We will normalize the dicument list now

    value_g=0
    sum_element=0

    for i in range(0,len(document_list)):
        for key in document_list[i]:
            value_g = (document_list[i][key] * document_list[i][key])
            sum_element+=value_g
        sum_element=math.sqrt(sum_element)
        for every_key in document_list[i]:
            document_list[i][every_key] = float( document_list[i][every_key] ) / float(sum_element)



    flag_control=1

    while(flag_control):

       choice = raw_input('\nInput your choice: 1- Input Own Cluster Number(k value) 2 : Use Default k value\n')
       ch = int(choice)

       if ( ch == 1):

          inpt = raw_input('\nInput the number of clusters\n')
          input_range = int(inpt)
          flag_control=0

       elif ( ch == 2 ):
            input_range = 5
            flag_control=0
       else:
            print 'Input Correct Choice i.e. 1 or 2'



    
      
    cluster_id=[]
    cluster_id_new=[]
    id_list=[]
    cluster=[]
    
    value_list=[]

    # Forming the initial clusters

    for jj in range(0,len(document_list)):
        value_list.append(jj)

    initial_centroid = find_mean(value_list)
    dist_vect=[]
    dict_id_dist={}
    
    for l in range(0,len(document_list)):
        distance_value = 0.0
        distance_value = float( distance(initial_centroid,document_list[l]) )
        dist_vect.append(distance_value)
        dict_id_dist[l]=distance_value
        
    #sort the dict_vect

    dist_vect.sort()

    ll=0  
    min_clust=[]

    element_per_cluster = int ( len(document_list) / input_range)

    print 'element_per_cluster',
    print  element_per_cluster
  
    for m in range(0,len(dist_vect)):
        for key in dict_id_dist:
            if dict_id_dist[key] == dist_vect[m]:
               min_clust.append(key)
               ll+=1
               if (ll > element_per_cluster or m == (len(dist_vect)-1)):
                  ll = 0
                  cluster_id.append(min_clust) 
                  min_clust=[]

    print len(cluster_id)    
 
    for n in range(0,input_range):
        cluster_id_new.append([])

    #cluster_id=[[15],[45],[75],[105],[135]]
    #cluster_id_new=[[],[],[],[],[]]

    # K-Means Algorithm
  
    mean = []
    comp1=[]
    comp2=[]
    
        
    iteration_max = 15

    convergence_count = 0
    flag = 1

   
    while(flag):

         # Finding the Centroid 
         mean=[]
         
                        
         for i in range(0,len(cluster_id)):
             
             if len(cluster_id[i]) !=0:
                mean.append(find_mean(cluster_id[i]))      
                                
                             
         for values in range(0,len(document_list)):
        	ind=give_min_distance(document_list[values],mean)
             
                cluster_id_new[ind].append(values)

                

         flg = 1

         for rng in range(0,len(cluster_id)):
             comp1=cluster_id[rng]
             comp2=cluster_id_new[rng]
             if comp1 != comp2:
                flg = 0
         
         if(flg == 0):
           
           #Reform the Cluster
           
           cluster_id=[]
 
           for h in range(0,len(cluster_id_new)):
               id_list=[]
               id_list=cluster_id_new[h]
               
               cluster_id.append(id_list)

           cluster_id_new=[]         
           
           for h in range(0,len(cluster_id)):
               cluster_id_new.append([])
           

         
         if(flg == 1):
              flag = 0
  
         convergence_count+=1

         if(convergence_count > iteration_max):
           flag = 0;

    for l in range(0,len(cluster_id)):
        print 'Cluster ',
        print  l
        for val in range(0,len(cluster_id[l])):
            print docClass[cluster_id[l][val]],
            print ': ',
            print title_list[cluster_id[l][val]]

        

    
    print '\nThe Algorithm Converges in ',
    print convergence_count,
    print ' iterations'      

    # Calculate RSS

    rss=0
    dist = 0

    for lst_clus in range(0,len(cluster_id)):
        centroid_vect=find_mean(cluster_id[lst_clus])
        for every_element in range(0,len(cluster_id[lst_clus])):
            dist=distance(centroid_vect,document_list[cluster_id[lst_clus][every_element]])
            dist = dist * dist
            rss+=dist
 

    print '\nThe RSS value  for k value ',
    print input_range,
    print ' is ',
    print rss


    # Calculate Purity
    clust_1=0
    clust_2=0
    clust_3=0
    clust_4=0
    clust_5=0

    total_sum =0

    for each_cluster in range(0,len(cluster_id)):
        for id in range(0,len(cluster_id[each_cluster])):
            if(0<= cluster_id[each_cluster][id] <30):
              clust_1+=1
            elif(30<= cluster_id[each_cluster][id] <60):
              clust_2+=1
            elif(60<= cluster_id[each_cluster][id] < 90):
              clust_3+=1
            elif(90<= cluster_id[each_cluster][id] < 120):
              clust_4+=1
            elif(120<= cluster_id[each_cluster][id] < 150):
              clust_5+=1

        total_sum+=max(clust_1,clust_2,clust_3,clust_4,clust_5)
	clust_1=0
        clust_2=0
        clust_3=0
        clust_4=0
        clust_5=0

    purity = float(total_sum) / len(document_list)

    print '\nThe purity for k value ',
    print input_range,
    print ' is ',
    print purity
    

    # Calculate the Rand Index
    
    tp=0
    clust_1=0
    clust_2=0
    clust_3=0
    clust_4=0
    clust_5=0
 

    for each_cluster in range(0,len(cluster_id)):
        clust_1=0
        clust_2=0
        clust_3=0
        clust_4=0
        clust_5=0
        for idl in range(0,len(cluster_id[each_cluster])):
            if(0<= cluster_id[each_cluster][idl] <30):
              clust_1+=1
            elif(30<= cluster_id[each_cluster][idl] <60):
              clust_2+=1
            elif(60<= cluster_id[each_cluster][idl] < 90):
              clust_3+=1
            elif(90<= cluster_id[each_cluster][idl] < 120):
              clust_4+=1
            elif(120<= cluster_id[each_cluster][idl] < 150):
              clust_5+=1
        tp+= combination(clust_1) + combination(clust_2) + combination(clust_3) + combination(clust_4)+ combination(clust_5)

    #print tp    

    tn = 0

    clust_1=0
    clust_2=0
    clust_3=0
    clust_4=0
    clust_5=0

    clust=[]
       

    for each_cluster in range(0,len(cluster_id)):
        
        clust_1=0
        clust_2=0
        clust_3=0
        clust_4=0
        clust_5=0

        for id in range(0,len(cluster_id[each_cluster])):
            if(0<= cluster_id[each_cluster][id] <30):
              clust_1+=1
            elif(30<= cluster_id[each_cluster][id] <60):
              clust_2+=1
            elif(60<= cluster_id[each_cluster][id] < 90):
              clust_3+=1
            elif(90<= cluster_id[each_cluster][id] < 120):
              clust_4+=1
            elif(120<= cluster_id[each_cluster][id] < 150):
              clust_5+=1
        lst_val=[]
        lst_val=[clust_1,clust_2,clust_3,clust_4,clust_5]
        clust.append(lst_val) 

    for val in range(0,len(clust)):
        for j in range(0,len(clust[val])):
            for k in range(val+1,len(clust)):
                iter_clust = clust[k]
                for l in range(0,len(iter_clust)):
                      if( l != j):
                        tn+= clust[val][j] * iter_clust[l]
                  
    numerator = tn + tp

    denominator = combination(len(document_list))

    
    rand_index = float(numerator) / denominator

    print '\nThe RI[Rand_Index] for k value ',
    print input_range,
    print ' is ',
    print rand_index
    print '\n'


    return 

def combination(val):

    ret_val = 0

    if val == 0 :
       ret_val = 0
    elif val == 1:
       ret_val = 0
    elif val == 2:
       ret_val = 1
    else:
        ret_val = float( val * (val -1 ) ) / 2


    return ret_val


def distance(vect,compare):
    sum=0 
    for key in compare:
            if key in vect:
               sum+=float( (compare[key] - vect[key]) * (compare[key] - vect[key]) )
            else:
               sum+=float( compare[key] * compare[key] )

    dist = math.sqrt(sum)
     
    return dist



def find_mean(lst):
   
     
    mn = collections.defaultdict(float)
    vect = collections.defaultdict(float)
    

    for i in range(0,len(lst)):
        
        vect = document_list[lst[i]]
        for each_key in vect:
            if each_key not in mn:
                   mn[each_key] = vect[each_key]
            else:
                    #mn[key]+=iter_lst[i][key]
                    mn[each_key]+=vect[each_key]

    for val in (mn):
        mn[val] = float( mn[val]/float(len(lst)) )


    return mn


def word_preprocessing(word):
 return re.findall(r"[\w]+", word.lower())


def give_min_distance(compare,mn_list):
    
    sum=0   
    dist = 0 
    lst = []

    

    for val in mn_list:
        sum = 0
        for key in compare:
            if key in val:
               sum+=float( (compare[key] - val[key]) * (compare[key] - val[key]) ) 
            else:
               sum+=float( compare[key] * compare[key] )

        dist = math.sqrt(sum)
        lst.append(dist)

    
    minimum_value = min(lst)
    index = lst.index(minimum_value)    
   
    return index

def main():
    
    bing_search_clustering(sys.argv[1]);
       
if __name__ == '__main__':
  main()
