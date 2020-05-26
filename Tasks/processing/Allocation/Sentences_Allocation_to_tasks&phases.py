import pandas as pd
import os
import random

SUBJECT_DATA = r'audio_data_80sentences.xlsx'
ALLOCATION_PLAN = r'Sentences_Allocation_Omer.xlsx'

def allocation(subject_data,allocation_plan):
    '''the function gets a matrix for sentecnes per task and phase, and 80 subject data,
     and allocate the sentences for each session'''
    #read files
    subject_data = pd.read_excel(subject_data)
    allocation_plan = pd.read_excel(allocation_plan)

#@#@# To talk with Tomer if he thinks it's nesecery!
    # #allocate even index to digit and odd to dicthotic
    # for i in subject_data['FileNumber']:
    #     if (i%2) == 0: #even
    #         subject_data.at[i-1,'Tasks']= 'Digit'
    #     else:
    #         subject_data.at[i-1,'Tasks'] = 'Dichotic'

    #read allocation plan
    Digit_before = allocation_plan.iloc[0, 2]
    Digit_after = allocation_plan.iloc[0, 3]
    Digit_before_after = allocation_plan.iloc[0, 4]

    Dichotic_before = allocation_plan.iloc[1, 2]
    Dichotic_after = allocation_plan.iloc[1, 3]
    Dichotic_before_after = allocation_plan.iloc[1, 4]

    #split data to neg/neu
    data_neg = subject_data[subject_data['SentenceType'] == 'neg']
    data_ntr = subject_data[subject_data['SentenceType'] == 'ntr']

    # #split data to dichotic/digit:
    # data_neg_dichotic = data_neg[data_neg['Tasks']=='Dichotic']
    # data_neg_digit = data_neg[data_neg['Tasks']=='Digit']
    #
    # data_ntr_dichotic = data_ntr[data_neg['Tasks']=='Dichotic']
    # data_ntr_digit = data_ntr[data_neg['Tasks']=='Digit']

    dic_phases_number = {}
    n_list= [Digit_before, Digit_after, Digit_before_after, Dichotic_before, Dichotic_after, Dichotic_before_after]
    n_str_list = ['Digit_before', 'Digit_after', 'Digit_before_after', 'Dichotic_before', 'Dichotic_after', 'Dichotic_before_after']
    for i in range(len(n_list)):
        dic_phases_number[n_str_list[i]]= n_list[i]

    print(dic_phases_number)
    for c,data in enumerate([data_neg, data_ntr]):
        index_list = list(range(len(data)))
        for k in dic_phases_number.keys():
            sample_index_list = random.sample(index_list,dic_phases_number[k])
            print(sample_index_list)
            for i in sample_index_list:
                index_list.remove(i)
                if c==1:
                    subject_data.at[i,'Phases'] = k
                else:
                    subject_data.at[i+40,'Phases'] = k

    print(subject_data['Phases'])
    subject_data.to_excel('audio_data_TasksPhases.xlsx')

allocation(SUBJECT_DATA,ALLOCATION_PLAN)


