##to write code that organize the audio_data file from the server and convert it into xsls. - CHECK :)
#to write a code that organize the files - put all the audio files in a directory called 'audio files'
###!!##to write a code that copy the top 20 neutral and negative into INPUT of the BodyMap and rename them into numbers??
#try to rename and keep the order and also the quesion ID as an adition.
#to rename the file - '19' --->'subject 19'

import pandas as pd
import os
path = r"Subjects"
def edit_audio_data(subject_num):
    path = "Subjects/"+str(subject_num)+'/'
    dir = os.listdir(path)
    audio_file_name = [s for s in dir if "audio_data" in s][0] #look for audio_data_19...
    df = pd.read_csv(path+audio_file_name)
    df['SentenceType'].replace({'Negative':'neg'}, regex=True,inplace = True)
    df['SentenceType'].replace({'Neutral':'ntr'}, regex=True,inplace = True)
    filepath_out = path+'audio_data.xlsx'
    df.to_excel(filepath_out)
edit_audio_data("19")
