# -*- coding: utf-8 -*-
"""
@author: hduong contribution 50% (built up original source code)
@author: wzhang contribution 50% (fixed and debugged any problems with the source code)
We changed list to set but it only shorten the time by 30% and we still can't get the final csv file
"""
import time
import json
import csv
import nltk
from nltk.corpus import words
from nltk.corpus import stopwords
from operator import itemgetter

def main():
    with open("yelp_academic_dataset_review_small.json")as in_json:
        object1=json.load(in_json);
        in_json.close()
    json_string=json.dumps(object1);
    object2=json.loads(json_string);
    list_review=[];
    list_stars=[];
    i=0;
    while i<len(object2):
        text=object2[i].get("text");
        list_review.append(text);
        i+=1;
    
    j=0;
    while j<len(object2):
        text=object2[j].get("stars");
        list_stars.append(text);
        j+=1;
    
    k=0;
    list_word_review=[];
    t0=time.time();
    while k<len(list_review):
        text=list_review[k];
        
        
        list_words=set(nltk.word_tokenize(text));
        
        lemmatizer = nltk.WordNetLemmatizer();
        
        list_words=[word.lower() for word in list_words];
        pos_translate = {"J" : "a", "V" : "v", "N" : "n", "R" : "r"}
        def pos2pos(tag):
         if tag in pos_translate: return pos_translate[tag] 
         else: return "n" 

        stop_words=stopwords.words("english");
        ENG_words=words.words("en");
        list_words=[lemmatizer.lemmatize(word,pos2pos(pos[0])) for word,pos in nltk.pos_tag(list_words) if word in ENG_words] 
        
        list_words=[word for word in list_words if (word not in stop_words) and (word.isalnum())] 
        
          
        
        list_word_review.append(list_words);
        k+=1;
    t1=time.time()-t0
    print('first:')
    print(t1)
    flat_list = [];
    
    t0=time.time();
    for sublist in list_word_review:
        
        
        for item in sublist:
            flat_list.append(item);
    
    words_reviews=set(flat_list);
    average_star=[];
    word_selected=[];
    
    for word in words_reviews:
        discard=0;
        sum_star=0;
        average=0;
        for x in range(len(list_word_review)):  
            if word in list_word_review[x]:
                discard+=1;
                sum_star+=list_stars[x];
        if discard>9:
            average=sum_star/discard;
            word_selected.append(word);
            average_star.append(average);
    t1=time.time()-t0;
    print('second:')
    print(t1)
    print(word_selected);
    print(average_star);
    bad_words=[];
    good_words=[];
    average_bad_word=[]
    average_good_word=[];
    l=0;
    while l<len(average_star):
        if average_star[l]<2.5:
            bad_words.append(word_selected[l]);
            average_bad_word.append(average_star[l]);
        if average_star[l]>4.0:
            good_words.append(word_selected[l]);
            average_good_word.append(average_star[l])
        l+=1;
    
        
    merged_list_Bad = [(bad_words[i], average_bad_word[i]) for i in range(0, len(bad_words))];
    merged_list_good = [(good_words[i], average_good_word[i]) for i in range(0, len(good_words))];
    merged_list_Bad=sorted(merged_list_Bad,key=itemgetter(1));
    merged_list_good=sorted(merged_list_good,key=itemgetter(1),reverse=True);
    
    final_result_bad=merged_list_Bad[0:501];
    final_result_good=merged_list_good[0:501];
    
    with open("sentimentlevel.csv", "w+") as csvfileOut:
        writer = csv.writer(csvfileOut, delimiter=',', quotechar='"');
        writer.writerow(["word", "sentiment level"]);
        i=0;
        while i<len(final_result_bad):
            writer.writerows([final_result_bad[i][0],str(final_result_bad[i][1])]);
            i+=1;
        j=0;
        while j<len(final_result_good):
            writer.writerows([final_result_good[j][0],str(final_result_good[j][1])]);
            j+=1;
        csvfileOut.close();

main()