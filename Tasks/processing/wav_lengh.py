# from scipy.io import wavfile
# Fs, x = wavfile.read("ntr_39.wav")


# import os
# # os.chdir(foo) # Get into the dir with sound
# statbuf = os.stat('ntr_27.wav')
# mbytes = statbuf.st_size / 1024
# duration = mbytes / 200


import pandas as pd
import os
import librosa
import random
import ipdb

AUDIO_FILES_DIRECTORY = 'audio_files'

class AudioProcessor(object):
	
	def __init__(self, pre_processed_audio_data, processed_audio_df):
		self.pre_processed_audio_data = pre_processed_audio_data
		self.processed_audio_df = processed_audio_df

	def process_audio(self, subject_audio_data):
		#new column for length of audio file
		df = pd.read_excel(subject_audio_data + '\\' + self.pre_processed_audio_data)
		col_audio_length = [] #new column with the audio duartion (Sec)
		col_digit = []
		
		sentence_num_column = df['TAPlistNumber']
		
		subject_audio_recordings_dir = subject_audio_data + '\\' + AUDIO_FILES_DIRECTORY
		dir = os.listdir(subject_audio_recordings_dir)
		
		for sen_num in sentence_num_column:
			for file in dir:
				if file[0]=='r':
					#find sentecne num in audio name
					ie=file.rfind("e")
					audio_num= file[ie+1:ie+file[ie:].find('_')]
					if int(sen_num) == int(audio_num):
						current_recording_file = subject_audio_recordings_dir + '\\' + file
						length = librosa.get_duration(filename=current_recording_file)
						col_audio_length.append(length)
			rand_digit = random.randint(1, 8)
			col_digit.append(rand_digit)
		
		
		df['length'] = pd.Series(col_audio_length)
		df['timing_digit'] = df['length'] -0.5
		df['rand_digit'] = col_digit
		
		
		df.to_excel(subject_audio_data + '\\' + self.processed_audio_df)
	def phase_allocation(self,subject_audio_data): #new column with phase name
		df = pd.read_excel(subject_audio_data + '\\' + self.pre_processed_audio_data)
		###copy here the algorithm??

def main():
	pass
if __name__ == '__main__':
	main()