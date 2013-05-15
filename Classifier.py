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


term_dict_business=collections.defaultdict(dict)
term_dict_politics=collections.defaultdict(dict)
term_dict_entertainment=collections.defaultdict(dict)


document_list=collections.defaultdict()

probability_entertainment=0.0
probability_business = 0.0
probability_politics = 0.0

total_terms_entertainment_class=0
total_terms_business_class=0
total_terms_politics_class=0

class_business=[]
class_entertainment=[]
class_politics=[]

tp_business=0
tp_politics=0
tp_entertainment=0

fp_business=0
fp_politics=0
fp_entertainment=0


fn_business=0
fn_politics=0
fn_entertainment=0



def naive_bays_classification(fileName1,fileName2,fileName3,fileName4,fileName5,fileName6):
 
        
    count =0
    docId =0
    
    global total_terms_entertainment_class
    global total_terms_business_class
    global total_terms_politics_class

    global probability_entertainment
    global probability_business
    global probability_politics

    
    entertainment_class_length=0
    business_class_length=0
    politics_class_length=0

    global_document_count=0

    lines = [line.strip() for line in open(fileName1)]
      
    for line in lines:
        news=json.loads(line)
        text=news['Title']+' '+news['Description']
        wordlist=word_preprocessing(text)
        
        total_terms_entertainment_class += len(wordlist)   

        for each_term in wordlist:
            if each_term not in term_dict_entertainment:
               term_dict_entertainment[each_term]=1
            else:
               term_dict_entertainment[each_term]+=1
             
        entertainment_class_length+=1
        global_document_count+=1
        wordlist=[]
    
    lines = [line.strip() for line in open(fileName2)]

    for line in lines:
        news=json.loads(line)
        text=news['Title']+' '+news['Description']
        wordlist=word_preprocessing(text)

        total_terms_business_class+=len(wordlist)

        for each_term in wordlist:
            if each_term not in term_dict_business:
               term_dict_business[each_term]=1
            else:
               term_dict_business[each_term]+=1

        business_class_length+=1
        global_document_count+=1
        wordlist=[]

    lines = [line.strip() for line in open(fileName3)]

    for line in lines:
        news=json.loads(line)
        text=news['Title']+' '+news['Description']
        wordlist=word_preprocessing(text)

        total_terms_politics_class += len(wordlist)

        for each_term in wordlist:
            if each_term not in term_dict_politics:
               term_dict_politics[each_term]=1
            else:
               term_dict_politics[each_term]+=1

        politics_class_length+=1
        global_document_count+=1
        wordlist=[]

    
    probability_entertainment = float( entertainment_class_length) / global_document_count 
    probability_business = float( business_class_length) / global_document_count    
    probability_politics = float( politics_class_length) / global_document_count 
    
       

    lines = [line.strip() for line in open(fileName4)]

    for line in lines:
        news=json.loads(line)
        text=news['Title']+' '+news['Description']
        title=news['Title']
        wordlist=word_preprocessing(text)
         
        calculate_class(wordlist,title,0)
            

    lines = [line.strip() for line in open(fileName5)]

    for line in lines:
        news=json.loads(line)
        text=news['Title']+' '+news['Description']
        title=news['Title']
        wordlist=word_preprocessing(text)

        calculate_class(wordlist,title,1)
  
    lines = [line.strip() for line in open(fileName6)]

    for line in lines:
        news=json.loads(line)
        text=news['Title']+' '+news['Description']
        title=news['Title']
        wordlist=word_preprocessing(text)

        calculate_class(wordlist,title,2)

    print 'Entertainment'
    for ll in range(0,len(class_entertainment)):
        print class_entertainment[ll][0],
        print ' ',
        print class_entertainment[ll][1]


    print '\nBusiness'
    for ll in range(0,len(class_business)):
        print class_business[ll][0],
        print ' ',
        print class_business[ll][1]

    print '\nPolitics'
    for ll in range(0,len(class_politics)):
        print class_politics[ll][0],
        print ' ',
        print class_politics[ll][1]


    
    tp_aggr = tp_business + tp_politics + tp_entertainment
    fp_aggr = fp_business + fp_politics + fp_entertainment
    fn_aggr = fn_business + fn_politics + fn_entertainment

    p_aggr = float(tp_aggr) / ( tp_aggr + fp_aggr)
    r_aggr = float(tp_aggr) / ( tp_aggr + fn_aggr)

    f_aggr = float( 2 * float(p_aggr * r_aggr)) / (p_aggr + r_aggr)

        
    print '\nEntertainment Class'
    print 'True Positive',
    print tp_entertainment,
    print 'False Positive',
    print fp_entertainment,
    print 'False Negative',
    print fn_entertainment,
    print 'True Negative',
    print ( len(class_entertainment) + len(class_business) + len(class_politics) - tp_entertainment - fp_entertainment - fn_entertainment )

    print '\nBusiness Class'
    print 'True Positive',  
    print tp_business,
    print 'False Positive',
    print fp_business,
    print 'False Negative',
    print fn_business,
    print 'True Negatine',
    print ( len(class_entertainment) + len(class_business) + len(class_politics) - tp_business - fp_business - fn_business )

    print '\nPolitics Class'
    print 'True Positive',
    print tp_politics,
    print 'False Positive',
    print fp_politics,
    print 'False Negative',
    print fn_politics,
    print 'True Negative',
    print ( len(class_entertainment) + len(class_business) + len(class_politics) - tp_politics - fp_politics - fn_politics )



    print '\nThe F1 value is',
    print f_aggr
    print '\n'   
    

    return 


def calculate_class(word_list,ttl,exp_class):
    
    global probability_entertainment
    global probability_business
    global probability_politics

    global tp_business
    global tp_politics
    global tp_entertainment

    global fp_business
    global fp_politics
    global fp_entertainment


    global fn_business
    global fn_politics
    global fn_entertainment

    
    sum_entertainment=0
    sum_business=0
    sum_politics=0
   
    for each_term in word_list:
        
        if each_term in term_dict_entertainment:
           numerator = term_dict_entertainment[each_term]+1
        else:
           numerator = 1
        denominator = total_terms_entertainment_class + len(term_dict_entertainment)
        frac = float(numerator) / denominator
        log_form = float(math.log(frac,2))
        sum_entertainment+=log_form

        if each_term in term_dict_business:
            numerator = term_dict_business[each_term]+1
        else:
            numerator = 1
        denominator = total_terms_business_class + len(term_dict_business)
        frac = float(numerator) / denominator
        log_form = float(math.log(frac,2))
        sum_business+=log_form

        if each_term in term_dict_politics:
            numerator = term_dict_politics[each_term]+1
        else:
            numerator = 1
        denominator = total_terms_politics_class + len(term_dict_politics)
        frac = float(numerator) / denominator
        log_form = float(math.log(frac,2))
        sum_politics+=log_form

       

    val_ent = float(math.log(float(probability_entertainment),2)) + sum_entertainment
    val_bus = float(math.log(float(probability_business),2)) + sum_business
    val_pol = float(math.log(float(probability_politics),2)) + sum_politics


    max_prob = max(val_ent,val_bus,val_pol)
   
    txt=''
    
    if(exp_class == 0):
      txt = 'Entertainment'
    elif(exp_class == 1):
      txt = 'Business'
    elif(exp_class == 2):
      txt = 'Politics'

    tpl=()

    if(max_prob == val_ent):
      tpl = (txt,ttl)
      #class_entertainment.append(ttl)
      class_entertainment.append(tpl)
      if (exp_class == 0):
         tp_entertainment+=1
      if (exp_class == 1):
         fn_business+=1
      if (exp_class == 2):
         fn_politics+=1
      if (exp_class == 1 or exp_class == 2):
         fp_entertainment+=1
       
    elif(max_prob == val_bus):
      tpl = ( txt,ttl)
      #class_business.append(ttl)
      class_business.append(tpl)
      if (exp_class == 1):
         tp_business+=1
      if (exp_class == 0):
         fn_entertainment+=1
      if (exp_class == 2):
         fn_politics+=1
      if (exp_class == 0 or exp_class == 2):
         fp_business+=1
      

    elif(max_prob == val_pol):
      tpl = ( txt,ttl)
      #class_politics.append(ttl)
      class_politics.append(tpl)
      if (exp_class == 2):
         tp_politics+=1
      if (exp_class == 0):
         fn_entertainment+=1
      if (exp_class == 1):
         fn_business+=1
      if (exp_class == 0 or exp_class == 1):
         fp_politics+=1

    return


def word_preprocessing(word):
 return re.findall(r"[\w]+", word.lower())


def main():
    
    naive_bays_classification(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5],sys.argv[6]);
       
if __name__ == '__main__':
  main()
