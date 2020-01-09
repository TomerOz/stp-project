import random

NumNegUniqe=20
NumNeuUniqe=20
NumBlock = 4
NumTrials = 10 #per block
NumOneBack = 4 #per block 

block_dic={}
#block_dic={b1:{neg=[1,3,8,8,9,4,2,7,7,....],neu=[1,4,4...],b2:{neg=....}...}

def build_block_dic(NumNegUniqe,NumNeuUniqe,NumBlock,NumTrials,NumOneBack):
    for i in range(NumBlock):
        block_dic['block'+str(i+1)]={}
    for num_block in block_dic.keys():
        neg_number_lst = random.sample(range(0,NumTrials,2), NumTrials)
        neu_number_lst = random.sample(range(0,NumTrials,2), NumTrials)
        OneBackNeg_lst = random.sample(range(1,NumTrials), NumOneBack) 
        #index 1 to 10 in neg_number_lst (for not begining with repetition in the first sentence), 
        #bad EXAMPLE! [2,5,3,9]
        OneBackNeu_lst = random.sample(range(1,NumTrials), NumOneBack)
        #to talk with Iftach about the repetition!
 
        print('neg_number_lst',neg_number_lst, 'OneBackNeg_lst', OneBackNeg_lst)
    
        for oneback_index in OneBackNeg_lst:
            neg_number_lst.insert(oneback_index,neg_number_lst[oneback_index])
        block_dic[num_block] = neg_number_lst
        # print('neg_number_lst',neg_number_lst)
        
        
        for oneback_index in OneBackNeu_lst:
            neu_number_lst.insert(oneback_index,neu_number_lst[oneback_index])
        block_dic[num_block] = neu_number_lst
    # for num_oneback in OneBackNeu_lst:
        # for num in neu_number_lst:
            # if num == num_oneback:
               # i =neu_number_lst.index(num)
               # neu_number_lst.insert(i,num_oneback) 
        # block_dic[num_block] = neu_number_lst
#$#$#Ctl+Q
build_block_dic(NumNegUniqe,NumNeuUniqe,NumBlock,NumTrials,NumOneBack)
print(block_dic)
            

        
    