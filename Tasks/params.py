#!/usr/bin/env python
# -*- coding: utf-8 -*-

##TODO - to add desctiption 

#Console

AUDIOPATH = r'Subjects'
IMAGEPATH = r'Instructions_Pictures'
IMAGEPATH_DICHOTIC_PRACTICE_ONE = r'Instructions_Pictures\Dichotic\DichoticInst1'
IMAGEPATH_DICHOTIC_PRACTICE_TWO = r'Instructions_Pictures\Dichotic\DichoticInst2'
IMAGEPATH_DICHOTIC = r'Instructions_Pictures\Dichotic\DichoticInst3'

IMAGEPATH_DCT_PRACTICE_1 = r'Instructions_Pictures\Digitnew\DigitInstTomerOmer\digit1'
IMAGEPATH_DCT_PRACTICE_2 = r'Instructions_Pictures\Digitnew\DigitInstTomerOmer\digit2'
IMAGEPATH_DCT_PRACTICE_3 = r'Instructions_Pictures\Digitnew\DigitInstTomerOmer\digit3'
IMAGEPATH_DICHOTIC_BREAK = r'Instructions_Pictures\Dichotic\DichoticInst4'
	
PRE_PROCESSED_AUDIO_DF = 'audio_data.xlsx'
PROCESSED_AUDIO_DF = 'audio_data_digit.xlsx' # file name containing audio data after processing ready for dct-stp task
AFACT_PHASE = "afact_phase"
DICHOTIC_PHASE_STR = 'dichotic_phase'


# controls ammount of truals of the different phases
N_BASELINE_TRIALS = 10
N_POST_TRIALS = 10
N_AFACT_TRIALS = 20
N_DICHOTIC_TRIALS = 20
N_PRACTICE_TRIALS = 8


#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*
#Task audio data manager 

PROCESSED_AUDIO_DF = 'audio_data_digit.xlsx' # file name containing audio data after processing ready for dct-stp task
AUDIO_FILES_DIRECTORY = 'audio_files_wav'

# sentences excel column names
LENGTH_COL = 'length'
SENTENCE_TEXT = 'sentContent'
SENTENCE_VALENCE = 'SentenceType'
SENTENCE_NUM = 'TAPlistNumber'
SENTENCE = 'sentence'

ONE_SECOND = 1000
MILISECONDS_BEFORE_END = 500

##TODO - check whith tomer why is it parallel to params from digit? maybe we should delete it? 
# task properties 
NEGATIVE_SENTENCE = 'neg' 			# According to audio df excel file
NEUTRAL_SENTENCE = 'ntr'			# According to audio df excel file

AFACT_PHASE = "afact_phase"			# in console we must use these contants
DICHOTIC_PHASE = "dichotic_phase"

# Instruction pointers
BEGINING_OF_TAKS  = 0
AFTER_PRACTICE_1  = 6
AFTER_PRACTICE_2  = 11

# THE FOLLOWINGS SPECIFIES "DEFAULS" - IT MEANS THAT IT WAS NOT SPEIFIED FROM CONSOLE
DEFAULT_N_PRACTICE_TRIALS = 8
DEFAULT_CATCH_TRIALS_RATIO = 1.0/8.0
DEFAULT_N_START_NEUTRAL_TRIALS = 4
DEFAULT_N_BLOCK_PER_PHASE = 1

#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*

#DCT
DEFAULS_N_BLOCK_PER_PHASE = 1
# sentences directories and files names
SENTENCE_NAME_COL = 'sentence_name'
SUBJECT = 'subject'
GROUP = 'group'
GENDER = 'gender'

FIXATION_TIME = 100 																			########### CHANGE WHENR OPERATING TO 1000 ###########
PRACTICE_FEEDBACK_DURATAION = 300
ONE_SECOND = 1000
MILISECONDS_BEFORE_END = 500
MIN_DIGIT = 1
MAX_DIGIT = 8
BLOCK_CHANGE_WAIT_TIME = 3000
CATCH_TRIAL_RESPONSE_DELAY = 500
DCT_STIMULI = u'XXX'
CATCH_SENTENCEE_QUESTION = u":האם המשפט האחרון ששמעת היה"
DCT_STIMULI_FONT = "david 50 bold"
RIGHT ='r'
LEFT = 'l'
RIGHT_RESPONSE_KEY = "<Shift_R>" #even
LEFT_RESPONSE_KEY = "<Shift_L>" #odd

#DCT gui properties 
BACKGROUND = "black"
FOREGROUND = "white"
CORRECT = "green"
WRONG = "red"
FRAME_1 = "first"
LABEL_1 = "label_1"
CHANGE_BLOCK_FRAME = 'change_block_frame'
BUTTON_LABEL = 'button_label'

#DCT task properties
EVEN= 'even'
ODD = 'odd'
CORRECT_SENTENCE = 1
NOT_CORRECT_SENTENCE = 0
RESPONSE_LABELS = {RIGHT : EVEN, LEFT: ODD} 	# should be changed at some point???
RESPONSE_LABELS_ON_CATCH_TRIALS = {RIGHT : CORRECT_SENTENCE, LEFT: NOT_CORRECT_SENTENCE} 	# should be changed at some point???
MIN_DIGIT = 1
MAX_DIGIT = 8
BLOCK_CHANGE_WAIT_TIME = 3000

#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*

#Dichotic
MAIN_FRAME = 'm_frame'
BACKGROUND_COLOR = 'black'
FIXATION_LABEL = 'fixation_label'
FOREGROUND_COLOR = 'white'

NEGATIVE_SENTENCE = 'neg'			# According to audio df excel file
NEUTRAL_SENTENCE = 'ntr'			# According to audio df excel file
AFACT_PHASE = "afact_phase"
FIXATION_STIMULI = '+'

DICHOTIC_RIGHT_KEY = "<Right>"
DICHOTIC_LEFT_KEY = "<Left>"

FIXATION_FONT = 'david 64 bold'
BLOCK_BREAK_TIME = 10000
CHUNK_NEU_START_DELAY	= 0
CHUNK_NEG_START_DELAY	= 0 #no delay
CHUNK_INITIAL_SILENCE  	= 0 # TODO - chekc if it is also in Iftach's
CHUNCK_BLOCK_CHANGE_WAIT_TIME = 1000
BLOCK_CHANGE_WAIT_TIME_ADDITION = 1000
BETWEEN_SENTENCES_DELAY = 300

PRE_PROCESSED_AUDIO_DF = 'audio_data.xlsx'
PROCESSED_AUDIO_DF = 'audio_data_digit.xlsx' # file name containing audio data after processing ready for dct-stp task

#DichoticDataManager 

DEFAULT_NUMBER_OF_BLOCKS = 3
DEFAULT_NUMBER_OF_CHUNCKS = 2 # SHOULD BE 4
DEFAULT_NUMBER_OF_UNIQUE_SENTENCES = 6 # SHOULD BE 10
DEFAULT_NUMBER_OF_N_BACK = 2
N_TRIALS_PRACTICE_ONE = 7
N_TRIALS_PRACTICE_TWO = 6

#Data 
#builds on the response key to be right/left arrows. (keysym - TK)
DICHOTIC_LEFT_KEYSYM = 'Left'
DICHOTIC_RIGHT_KEYSYM = 'Right'

