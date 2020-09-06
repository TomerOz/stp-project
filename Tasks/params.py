#!/usr/bin/env python
# -*- coding: utf-8 -*-

##TODO - to add desctiption 


ALLOCATION_TOMER = r'.\\Sentences_Allocation_Tomer.xlsx'
ALLOCATION_OMER = r'.\\Sentences_Allocation_Omer.xlsx'

ALLOCATION = ALLOCATION_TOMER
#ALLOCATION = ALLOCATION_OMER

#Console

AUDIOPATH = r'.\\Subjects'
IMAGEPATH = r'.\\Instructions_Pictures'
WORDS_PATH = r'.\\Tasks\\processing\\AfactWordsAlternative'
IMAGEPATH_DICHOTIC_PRACTICE_ONE = r'.\\Instructions_Pictures\\Dichotic\\DichoticInst1'
IMAGEPATH_DICHOTIC_PRACTICE_TWO = r'.\\Instructions_Pictures\\Dichotic\\DichoticInst2'
IMAGEPATH_DICHOTIC = r'.\\Instructions_Pictures\\Dichotic\\DichoticInst3'
# IMAGEPATH_DICHOTIC_END = r"C:\Users\psylab6027\Documents\GitHub\stp-project\Instructions_Pictures\Dichotic\EndOfTask"
# IMAGEPATH_DIGIT_END =  r"C:\Users\psylab6027\Documents\GitHub\stp-project\Instructions_Pictures\Digitnew\DigitInstTomerOmer"

IMAGEPATH_DICHOTIC_END = r'.\\Instructions_Pictures\\Dichotic\\EndOfTask'
IMAGEPATH_DIGIT_END =  r'.\\Instructions_Pictures\\Digitnew\\DigitInstTomerOmer'

IMAGEPATH_END_OF_EXPERIMENT = r'Instructions_Pictures\EndOfExperiment'

IMAGEPATH_DCT_PRACTICE_1 = r'.\\Instructions_Pictures\\Digitnew\\DigitInstTomerOmer\\digit1'
IMAGEPATH_DCT_PRACTICE_2 = r'.\\Instructions_Pictures\\Digitnew\\DigitInstTomerOmer\\digit2'
IMAGEPATH_DCT_PRACTICE_3 = r'.\\Instructions_Pictures\\Digitnew\\DigitInstTomerOmer\\digit3'
IMAGEPATH_DICHOTIC_BREAK = r'.\\Instructions_Pictures\\Dichotic\\DichoticInst4'

IMAGEPATH_AFACT_INSTRUCTIONS = r'.\\Instructions_Pictures\\AFACT & MAB Instructions\\AFACT_main_instructions'
IMAGEPATH_AFACT_INSTRUCTIONS_AFTER_PRACTICE = r'.\\Instructions_Pictures\\AFACT & MAB Instructions\\AFACT_after_practice_instructions'
IMAGEPATH_MAB_INSTRUCTIONS = r'.\\Instructions_Pictures\\AFACT & MAB Instructions\\MAB_main_instructions'
IMAGEPATH_MAB_INSTRUCTIONS_AFTER_PRACTIC = r'.\\Instructions_Pictures\\AFACT & MAB Instructions\\MAB_after_practice_instructions'

##temporary - for allocation -
PRE_PROCESSED_AUDIO_DF = 'audio_data_80sentences.xlsx'

# PRE_PROCESSED_AUDIO_DF = 'audio_data.xlsx'
PROCESSED_AUDIO_DF = 'audio_data_digit.xlsx' # file name containing audio data after processing ready for dct-stp task
AFACT_PHASE = "afact_phase"
DICHOTIC_PHASE_STR = 'dichotic_phase'


# controls ammount of truals of the different phases
# should be deleted :
#<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
N_BASELINE_TRIALS = 10 # in digit baseline
N_POST_TRIALS = 10 # in digit post intervention
N_AFACT_TRIALS = 20
N_DICHOTIC_TRIALS = 20 
N_PRACTICE_TRIALS = 8 # in digit and afact
# <><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>

#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*
#Task audio data manager 

PROCESSED_AUDIO_DF = 'processed_audio_df.xlsx' # file name containing audio data after processing ready for dct-stp task
AUDIO_FILES_DIRECTORY = 'audio_files'

# sentences excel column names
LENGTH_COL = 'length'
SENTENCE_TEXT = 'SentContent'
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
MAB_PHASE = "MAB_phase"

DIGIT_PRE = "DIGIT_PRE"
DIGIT_POST = "DIGIT_POST" 

DICHOTIC_PRE = "DICHOTIC_PRE"
DICHOTIC_POST = "DICHOTIC_POST"


# Instruction pointers
BEGINING_OF_TAKS  = 0
AFTER_PRACTICE_1  = 6
AFTER_PRACTICE_2  = 11

# THE FOLLOWINGS SPECIFIES "DEFAULTS" - IT MEANS THAT IT WAS NOT SPEIFIED FROM CONSOLE
DEFAULT_N_BLOCK_PER_PHASE = 1
DEFAULT_CATCH_TRIALS_RATIO = 1.0/8.0
DEFAULT_N_PRACTICE_TRIALS = 8
DEFAULT_N_START_NEUTRAL_TRIALS = 4

#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*

#DCT
DEFAULS_N_BLOCK_PER_PHASE = 1 #for AFACT. 
# sentences directories and files names
SENTENCE_NAME_COL = 'sentence_name'
SUBJECT = 'subject'
GROUP = 'group'
GENDER = 'gender'
SESSION = 'session'

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
DCT_STIMULI_FONT = "Courier 50 bold"
RIGHT ='r'
LEFT = 'l'
RIGHT_RESPONSE_KEY = "<Shift_R>" #even
LEFT_RESPONSE_KEY = "<Shift_L>" #odd

CATCH_RIGHT_RESPONSE_KEY = "<Alt_R>" # identical
CATCH_LEFT_RESPONSE_KEY = "<Alt_L>" # not identical

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
# AFACT:
GREATER_X = "more_then_4"
SMALLER_X = "less_then_4"
ALIVE = "ALIVE"
STILL = "STILL"
RESPONSE_LABELS_AFACT_ALTERNATIVE_1 = {RIGHT : GREATER_X, LEFT: SMALLER_X} 
RESPONSE_LABELS_AFACT_ALTERNATIVE_2 = {RIGHT : ALIVE, LEFT: STILL}
#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*
# MAB
MAB_RESONSE_KEY = "<space>"
MAB_PRACTICE_FEEDBACK_DURATAION = 1000

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

#DichoticDataManager 
DEFAULT_NUMBER_OF_BLOCKS = 3 # In Tomer's should be 2 --- difined via console in n_blocks argument
DEFAULT_NUMBER_OF_CHUNCKS = 4 # SHOULD BE 4
DEFAULT_NUMBER_OF_UNIQUE_SENTENCES = 10 # SHOULD BE 10 - trials per chunk
DEFAULT_NUMBER_OF_N_BACK = 2
N_TRIALS_PRACTICE_ONE = 7
N_TRIALS_PRACTICE_TWO = 6

#Data 
#builds on the response key to be right/left arrows. (keysym - TK)
DICHOTIC_LEFT_KEYSYM = 'Left'
DICHOTIC_RIGHT_KEYSYM = 'Right'

