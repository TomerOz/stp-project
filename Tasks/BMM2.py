from .DCT import DctTask, TaskData
from playsound import playsound
import os
import random
import librosa
import ipdb
import math
import time
import winsound


from .params import *

INSTRUCTIONS_AUDIO_PATH = r'Tasks\BMMRecordings'
INSTRUCTIONS_AUDIO_PATH_MALE = r'Tasks\BMMRecordings\Male'

if not BMM_DEBUG_MODE:
    INSTUCTIONS_AUDIO_1 = "BMM_1.wav"
    INSTUCTIONS_AUDIO_2 = "BMM_2.wav"
    INSTUCTIONS_AUDIO_3 = "BMM_3.wav"
    INSTUCTIONS_AUDIO_4 = "BMM_4.wav"
    INSTUCTIONS_AUDIO_5 = "BMM_5.wav"


else: # on Debug mode
    INSTUCTIONS_AUDIO_1 = r"old-BMM-Recordings\1.wav"
    INSTUCTIONS_AUDIO_2 = r"old-BMM-Recordings\2.wav"
    INSTUCTIONS_AUDIO_3 = r"old-BMM-Recordings\3.wav"
    INSTUCTIONS_AUDIO_4 = r"old-BMM-Recordings\4.wav"
    INSTUCTIONS_AUDIO_5 = r"old-BMM-Recordings\5.wav"


BETWEEN_INSTRUCTIONS_DELAY = 1000
MIN_PRACTICE_RESPONSES = 4 # should be ~4
# RANDOM_TIME_LAPSE_BETWEEN_BMM_TRIALS - is a list that sets the random interval between sentences.

class BMMTask(DctTask):
    def __init__(self, gui, exp, td, flow):
        super(BMMTask, self).__init__(gui, exp, td, flow, response_labels="original")

        self.sentences_start_times = []

        self.instructions_audio_path = INSTRUCTIONS_AUDIO_PATH

        self.instructions_paths = self._get_instructions_audio_files()
        self.n_instruction_audios = len(self.instructions_paths)
        self.instructions_input_delay_times = self._get_instructions_input_delay_times()



        self.instructions_audio_index = 0
        self.current_instruction_duration = self.get_duration_of_audio(self.instructions_audio_index)
        self.min_practice_responses = MIN_PRACTICE_RESPONSES
        self.last_practice_response_times = []
        self.is_practice_finished = False
        self.is_stp_practice_finished = False
        self.current_sentence_responses = []
        self.stimulus_live_text = "+"
        self.original_stimulus_live_text = "+"
        self.sentence_start_time = 0

        self.gender_instructions_paths = {"m": INSTRUCTIONS_AUDIO_PATH_MALE, "f": INSTRUCTIONS_AUDIO_PATH}

        self.is_continue_initiated = False

    def _get_instructions_input_delay_times(self):
        sec = 1000
        silence_lengths = [60*sec, 60*sec, 60*sec, 4*sec, 8*sec]
        delays = []
        for i in range(len(self.instructions_paths)):
            duration = self.get_duration_of_audio(i)
            delays.append(duration-silence_lengths[i])
        return delays

    def _get_instructions_audio_files(self):
        instructions_paths = []
        instructions_paths.append(os.path.join(self.instructions_audio_path, INSTUCTIONS_AUDIO_1))
        instructions_paths.append(os.path.join(self.instructions_audio_path, INSTUCTIONS_AUDIO_2))
        instructions_paths.append(os.path.join(self.instructions_audio_path, INSTUCTIONS_AUDIO_3))
        instructions_paths.append(os.path.join(self.instructions_audio_path, INSTUCTIONS_AUDIO_4))
        instructions_paths.append(os.path.join(self.instructions_audio_path, INSTUCTIONS_AUDIO_5))

        return instructions_paths

    def _change_gender_audio_path(self, gender_key):
        self.instructions_audio_path = self.gender_instructions_paths[gender_key]
        self.instructions_paths = self._get_instructions_audio_files()
        self.instructions_input_delay_times = self._get_instructions_input_delay_times()

    def change_text_on_screen(self, text):
        self.exp.LABELS_BY_FRAMES[FRAME_1][LABEL_1].config(text=text)

    def display_main_frame(self, text=None):
        if text == None:
            text = "+"
        self.change_text_on_screen(text)
        self.exp.display_frame(FRAME_1, [LABEL_1])


    def play_instructions_audio(self, instuction_index):
        #playsound(self.instructions_paths[instuction_index], block=False)
        winsound.PlaySound(self.instructions_paths[instuction_index], winsound.SND_ASYNC)
        self.td.start_time_record() # saves t0 - when instructions starts

    def _start_audio(self):
        winsound.PlaySound(self.td.current_sentence_path, winsound.SND_ASYNC | winsound.SND_ALIAS )

        self.td.start_time_record() # saves t0 - when sentence starts
        self.sentence_start_time = time.time()

        # Senetnces to follow each other automatically:
        random_noise = RANDOM_TIME_LAPSE_BETWEEN_BMM_TRIALS[random.randint(0,len(RANDOM_TIME_LAPSE_BETWEEN_BMM_TRIALS)-1)]
        interval_between_sentences = random_noise
        time_of_next_sentence = round(self.td.current_sentence.sentence_length + interval_between_sentences)


    def is_senetence_finished(self):
        if time.time() >= self.td.current_sentence.sentence_length/1000 + self.sentence_start_time:
            return True
        else:
            return False


    def _getresponse(self, eff=None):
        print("response")
        self.td.t1 = time.time() # recording rt                             ## END OF TIME RECORD
        self.td.record_time()
        self.td.record_trial()

        self.current_sentence_responses.append(self.td.t1)
        self.last_practice_response_times.append(self.td.t1)

        if len(self.current_sentence_responses) >= 2 and self.is_practice_finished and not self.is_continue_initiated:
            self.is_continue_initiated = True
            self.gui.after(3000, self._continue)

    def _continue(self):
        self.is_continue_initiated = False

        self.td.current_trial += 1 # raising trial by 1
        self.td.updata_current_sentence() # updatind sentence - loading everything nedded

        self.current_sentence_responses = [] # clearing for next sentence

        if self.td.current_trial_type_intance.is_change_block_trial:
            pass

        elif self.td.current_trial_type_intance.is_instructions:
            pass

        elif self.td.current_trial == 5 and not self.is_stp_practice_finished: # end of practice stps back to instructions
            self.is_practice_finished = False
            self._unbind_keyboard()
            self.gui.after(BETWEEN_INSTRUCTIONS_DELAY, self.next_audio_instructions)
        else:
            self._trial() # continues to next trial

    def _trial(self):
        '''This function is being called after response to last trial took place.
                First, it records last trial,
                Second, it start the next trial'''

        self.change_text_on_screen("+")
        self._bind_keyboard()
        # Checking if experiment ended:
        if self.td.current_trial < self.td.total_ammount_of_trials:
            ''' Task is still running'''
            self.gui.after(0, self._start_audio)
        else:
            ''' Task is over'''
            self._unbind_keyboard()
            self.td.sd.create_data_frame()
            # raise flag of completion

            # audio saying task is over:
            if self.td.menu.menu_data["gender"] == "m":
                winsound.PlaySound(r'Tasks\BMMRecordings\Male\End\BMM_END.wav', winsound.SND_ASYNC | winsound.SND_ALIAS )
            else:
                winsound.PlaySound(r'Tasks\BMMRecordings\End\BMM_END.wav', winsound.SND_ASYNC | winsound.SND_ALIAS )

            self.end_task()

    def _unbind_keyboard(self):
        self.gui.unbind(CATCH_RIGHT_RESPONSE_KEY)
        self.gui.unbind(CATCH_LEFT_RESPONSE_KEY)
        self.gui.unbind(RIGHT_RESPONSE_KEY)
        self.gui.unbind(LEFT_RESPONSE_KEY)
        self.gui.unbind(BMM_RESPONSE_KEY)
        ### TODO: Make sure to unbind here all other tasks keys!! #### <><><>

    def _bind_keyboard(self):
        self.gui.bind(BMM_RESPONSE_KEY, lambda eff: self._getresponse(eff))

    def get_duration_of_audio(self, instuction_index):
        duration = 1000*math.ceil(float(librosa.get_duration(filename=self.instructions_paths[instuction_index])))
        return duration

    def _get_input_delay_time(self):
        return self.instructions_input_delay_times[self.instructions_audio_index]

    def start_over_instructions_audio(self):
        self.exp.display_frame(FRAME_1, [LABEL_1])
        # to avoid re evoking the replay button
        self.exp.LABELS_BY_FRAMES["message_invalid_frame"]['message_invalid_label'].destroy()
        self.start_audio_instructions()

    def _on_invalidated_phase(self):
        invalid_frame = self.exp.create_frame("message_invalid_frame")
        message_invalid_label = self.exp.create_label("message_invalid_label", "message_invalid_frame")
        button_hear_practice_again = self.exp.create_button("message_invalid_frame", "message_invalid_label", u"שמע הוראות שוב", self.start_over_instructions_audio)
        self.exp.display_frame("message_invalid_frame", ["message_invalid_label"])

    def validation_post_practice_instructions(self):
        if self.instructions_audio_index == 0:
            self.last_practice_response_times = []
            return True
        elif self.instructions_audio_index == 1:
            if len(self.last_practice_response_times) >= self.min_practice_responses:
                self.last_practice_response_times = []
                return True
        elif self.instructions_audio_index == 2:
            if len(self.last_practice_response_times) >= self.min_practice_responses:
                self.last_practice_response_times = []
                return True
        elif self.instructions_audio_index == 3:
            if len(self.last_practice_response_times) >= 0: #self.min_practice_responses:
                self.last_practice_response_times = []
                return True

        return False

    def next_audio_instructions(self):
        self._unbind_keyboard()
        if self.validation_post_practice_instructions():
            self.instructions_audio_index += 1
            self.start_audio_instructions()
        elif self.instructions_audio_index == 4: # audio_phase ended
            self.is_practice_finished = True
            self.is_stp_practice_finished = True
            self.td.current_trial -= 1 #giving back the lost trial that was the stp practice end marker
            self._continue() # experiment starts
        else:
            self._on_invalidated_phase()
            # some message - repeat - inform experimenter

    def __skip_instructions(self, event):
        print("skip attempted", self.instructions_audio_index)

        winsound.PlaySound(None, winsound.SND_PURGE)
        self._unbind_keyboard()
        if self.instructions_audio_index != 4: # audio_phase ended
            self.last_practice_response_times = []
            self.gui.after_cancel(self.next_instruction_audio_id)
            self.instructions_audio_index += 1
            self.start_audio_instructions()
            # Maybe here insert a stop current audio code...
        elif self.instructions_audio_index == 4: # audio_phase ended
            self.is_practice_finished = True
            self.is_stp_practice_finished = True
            self.td.current_trial -= 1 #giving back the lost trial that was the stp practice end marker
            self._continue() # experiment starts
        else:
            pass
            #self._on_invalidated_phase()
            # some message - repeat - inform experimenter


    def _finish_pratice_for_stp_practice(self):
        #  to enable getting into the stps practice
        self.is_practice_finished = True

    def start_audio_instructions(self):

        self.play_instructions_audio(self.instructions_audio_index)
        self.gui.after(self._get_input_delay_time(), self._bind_keyboard)

        self.current_instruction_duration = self.get_duration_of_audio(self.instructions_audio_index)

        if self.instructions_audio_index < self.n_instruction_audios:
            if self.instructions_audio_index == 3: # continue to stps practice:
                self.gui.after(self.current_instruction_duration, self._finish_pratice_for_stp_practice) # allowing input in delay
                self.gui.after(self.current_instruction_duration, self._continue) # experiment starts

            else: # continue to next instructions
                self.current_instruction_duration = self.get_duration_of_audio(self.instructions_audio_index)
                self.next_instruction_audio_id = self.gui.after(self.current_instruction_duration, self.next_audio_instructions)

    def __check(self, event):
        print("check")

    def start_task(self, user_event=None):
        # update gender audio path
        self._change_gender_audio_path(self.td.menu.menu_data["gender"])

        # Just for allowing fast skipping over the instruciton phase
        if BMM_DEBUG_MODE:
            self.gui.bind("c", self.__check)
            self.gui.bind("s", self.__skip_instructions)

        # On task first initiation
        if self.td.current_trial == -1:
            self.td.event_timed_init() # user dependet initment of the dct data class

            if BMM_DEBUG_MODE:
                self.td.trials_types_by_phase = self.td.trials_types_by_phase[:10]
                self.td.total_ammount_of_trials = len(self.td.trials_types_by_phase)
                RANDOM_TIME_LAPSE_BETWEEN_BMM_TRIALS = [500, 500]
            #ipdb.set_trace()

            self._create_task_label() # creating the main frame
            self.display_main_frame(text="+") # displaying main frame and setting text to fixation cross

            # starting audio instructions:
            self.td.updata_current_sentence() # such that any sentence object will be found for data saving
            self._unbind_keyboard()
            t1 = 0
            self.gui.after(t1, self.start_audio_instructions)

        # after instruction phase within this task
        elif self.is_practice_finished:
            self.exp.display_frame(FRAME_1, [LABEL_1])
            t1 = 0
            self.gui.after(t1, self._continue) # experiment was started

class BMMTaskData(TaskData):
    def __init__(self, menu, data_manager, subject_data, phase=None, sessions_names=None):
        super(BMMTaskData, self).__init__(menu, data_manager, subject_data, phase=phase, sessions_names=sessions_names)

    def record_time(self):
        self.last_RT = self.t1 # not actually RT but a response time stamp

    def record_trial(self):
        # saving key press in order to pass into Data package
        self.num_shown_type = None
        self.is_catch_trial = False
        self.correct = None
        self.last_trial_classification = None
        self.last_key_pressed = "Space"
        self.trial_phase = self.current_trial_type_intance.trial_phase

        # saving data
        self.sd.push_data_packge(self)

    def event_timed_init(self):
        super(BMMTaskData, self).event_timed_init()
        # filttering our instructions,change block and feefback trials
        self.trials_types_by_phase = self.filter_td_trial_types_for_BMM()
        self.total_ammount_of_trials =  len(self.trials_types_by_phase)

    def filter_td_trial_types_for_BMM(self):
        filtered_trial_types = [tp for tp in self.trials_types_by_phase \
                                    if not tp.is_instructions \
                                    and not tp.is_afact_feedback \
                                    and not tp.is_change_block_trial]
        return filtered_trial_types
