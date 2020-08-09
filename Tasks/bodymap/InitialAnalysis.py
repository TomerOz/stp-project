import pandas as pd
import matplotlib.pyplot as pyplot
from scipy.stats import chisquare

path_before = r'C:\Users\psylab6027\Documents\GitHub\BodyMap\BodyMap\output\cluster\before_yoga_afterNegativeSTP.csv'
path_after = r'C:\Users\psylab6027\Documents\GitHub\BodyMap\BodyMap\output\cluster\after_yoga_afterNegativeSTP.csv'


columns = ['x','y','intensity','tone']
before_file = pd.read_csv(path_before, usecols=columns)
after_file = pd.read_csv(path_after,usecols=columns)

def read_file(path_csv, columns=['x','y','intensity','tone']):
    file = pd.read_csv(path_csv, usecols=columns)
    return file

def freq_analysis(file, block):
    freq_sensations = file['tone'].count()  #total number / freq of sensations
    tone_list = ['grey','blue','red']
    dic_freq= {}      #to count the freq of red, blue, grey + creat a pie plot
    dic_freq['all']=float(freq_sensations)
    for tone in tone_list:
        dic_freq[tone] = float((file['tone']==tone).sum())
    dic_relFreq = {}
    for tone in dic_freq.keys():
        if tone!='all':
            relFreq = dic_freq[tone]/dic_freq['all']
            dic_relFreq[tone] = relFreq
    # print(dic_freq,dic_relFreq)
    # labels = dic_relFreq.keys()
    labels = ['Neutral :-|','Pleasant :)','Unpleasant :(']
    colors = ['grey','blue','red']
    x = dic_relFreq.values()
    pyplot.pie(x=x,labels=labels,colors={'grey':"grey",'blue':"blue",'red':"red"},
               autopct='%1.1f%%', shadow=True, startangle=90)
    pyplot.title(block)
    # pyplot.show()
    pyplot.savefig(block)
    pyplot.close()
    print(list(dic_freq.values()))
    return list(dic_freq.values())[1:]
    #to calc intensity mean

    #intensity mean for red, blue, grey seperately

def intensity_analysis(file):
    mean_intensity = file['intensity'].mean()
    mean_intenities_tone = file.groupby('tone')['intensity'].mean()
    # pleasant_mean_intensity = mean_intenities_tone['blue']
    # unpleasant_mean_intensity = mean_intenities_tone['red']
    # neutral_mean_intensity = mean_intenities_tone['grey']
    # print(mean_intensity, mean_intenities_tone)
    return mean_intensity, mean_intenities_tone

file_before = read_file(path_before, columns)
freq_before = freq_analysis(file_before,block = 'before')
intensity_before, intensity_tone_before = intensity_analysis(file_before)

file_after = read_file(path_after, columns)
freq_after = freq_analysis(file_after,block = 'after')
intensity_after, intensity_tone_after = intensity_analysis(file_after)


contrast_intensity_all = intensity_after-intensity_before
contrast_intensity_tone = intensity_tone_after - intensity_tone_before
print(contrast_intensity_all, contrast_intensity_tone)

print(chisquare([freq_after],[freq_before]))