import pandas as pd
import os
import librosa
import random

class AudioProcessor(object):
    
    def __init__(self, pre_processed_audio_data, processed_audio_df):   
        self.pre_processed_audio_data = pre_processed_audio_data
		self.processed_audio_df = processed_audio_df
        self._process_audio()
        	
	def _process_audio(self):
	
		#new column for length of audio file
		df = pd.read_excel(self.pre_processed_audio_data)
		col_audio_length = [] #new column with the audio duartion (Sec)
		col_digit = []
		
		sentence_num_column = df['TAPlistNumber']
		
		cwd = os.getcwd()
		dir = os.listdir(cwd)
		
		for sen_num in sentence_num_column:
			for file in dir:
				if file[0]=='r':
					#find sentecne num in audio name
					ie=file.rfind("e")
					audio_num= file[ie+1:ie+file[ie:].find('_')]
					if int(sen_num) == int(audio_num):
						length = librosa.get_duration(filename=file)
						col_audio_length.append(length)
			rand_digit = random.randint(1, 8)
			col_digit.append(rand_digit)
		
		df['length'] = col_audio_length
		df['timing_digit'] = df['length'] -0.5
		df['rand_digit'] = col_digit
		
		
		df.to_excel(self.processed_audio_df)

