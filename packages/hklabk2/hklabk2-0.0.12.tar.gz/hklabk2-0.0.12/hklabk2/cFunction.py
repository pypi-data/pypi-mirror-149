#!/usr/bin/env python
# coding: utf-8

# In[10]:


#! /usr/bin/env python
# coding: utf-8 

# In[1]:

# description: 반올림 계산 함수
# input: invalue 반올림 대상 값
# output: 소수점 3자리 (반올림) 
def roundFunction(invalue): 
    step1 = invalue * 1000
    step2 = int(step1) 
    outvalue = step2/1000
    return outvalue

# description: 문자열로 이루어진 리스트의 합을 구하는 함수 
# input: inputList 문자열 리스트 
# output: 문자열내 총합 
def sumFunc(inputList): 
    #길이를 변수에 저장 
    listLength = len(inputList) 
    
    #리스트의 각 값을 정수로 변환 
    for i in range(0 , listLength): 
        inputList[i] = int(inputList[i])
        
    #정수로 변환된 리스트 합을 구함
    result = sum(inputList)
    return result 
# description: 기준 연주차에서 과거 주차를 계산하는 함수 
# input: yearweek(기준주차) , preweek(기준 주차 대비 빼야할 주차 정보) 
# output : 기준 연주차 대비 preWeek 이전 연주차 정보 ( 예: 201712 , 12 -> 201652)
def preWeek(yearWeek ,preWeek):
    from isoweek import Week 
    yeardigit = 4 #만년 이후에는 자리수가 바뀔수 있으니까.. 
    inputYear = int(str(yearWeek)[:yeardigit]) #년도만 잘라서 저장 
    inputWeek = int(str(yearWeek)[yeardigit:]) #주차만 잘라서 저장 
    resultWeek = inputWeek - preWeek           #현 주차 - 뒤로 갈 주차 계산 결과 
    
    while(resultWeek <=0):   # 주차가 0 이하라면 
        inputYear = inputYear-1  # 년도가 하나 줄어듭니다. 
        calcWeek = Week.last_week_of_year(inputYear).week  # 줄어든 년도의 총 주차수 
        resultWeek = calcWeek + resultWeek 
        #총 주차수에 resultWeek을 더해줍니다. (0 또는 음수 일테니까)
        #더했는데 0 또는 음수라면 양수가 될 때까지 반복합니다. 
    if(resultWeek <10): 
        resultWeek = "0" + str(resultWeek) #1자리수면 앞에 0을 붙여줌 
    result = str(inputYear) + str(resultWeek) #년도와 주차를 문자열로 더해서 출력 
    return result



# In[7]:


sumFunc(["11","22"])


# In[8]:


roundFunction(12.22222)


# In[11]:


preWeek("201702" , 100)


# In[ ]:




