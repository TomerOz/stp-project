import os
import pandas as pd
import shutil
import ipdb

class PreRunChecker(object):
    def __init__(self):
        self.subject_num = "SUBJECT NOT YET DEFINED" # will be defined via menu

    def run_check(self, subject_num):
        edited_audio_path = r'Subjects\edited_audio_{}'.format(str(subject_num))
        if os.path.exists(edited_audio_path):
            files = os.listdir(edited_audio_path)

            audio_data_file = ""
            i = 0
            while not "audio_data" in audio_data_file:
                audio_data_file = files[i]
                i+=1
                if i > len(files)-1:
                    print("Missing Audio File data")
                    break

            if not "audio_data" in audio_data_file:
                exit()

            files = [f for f in files if f.endswith(".wav")]

            audio_df = pd.read_csv('Subjects\edited_audio_{}'.format(subject_num) + "\\" + audio_data_file)
            audio_df["TAPlistNumber"].values

            matches = 0
            tap_list = audio_df["TAPlistNumber"].values.tolist()
            missing_sentences = []
            for tap_sentece in tap_list:
                tap_exist = False
                for f in files:
                    if not "silence_recording" in f:
                        if int(f.split("sentence")[1].split("_")[0]) == tap_sentece:
                            matches+=1
                            tap_exist = True
                if not tap_exist:
                    missing_sentences.append(tap_sentece)

            if matches == len(tap_list):
                text = "All recordings exist :)"
                print("All recordings exist :)")
            else:
                text = "Missing sentences:"
                print(text)
                for sentence in missing_sentences:
                    print(sentence)
                    text = text +"\n" + str(sentence)
            if len(missing_sentences)==0:
                error=False
            else:
                error=True
            state = (error, text)
            return state
        else:
            state = (True, "folder edited_audio_{} doesn't exist - restore it from drive and try checking again".format(str(subject_num)))
            return state

    def restore_bodymap(self):
        source = r'Tasks\bodymap\output'
        self.delete_content(source)
        os.makedirs(os.path.join(source, "actions"))
        os.makedirs(os.path.join(source, "cluster"))

    def delete_content(self, folder):
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))

def main():
    prc = PreRunChecker()
    prc.run_check(512)
    prc.restore_bodymap()

if __name__ == "__main__":
   main()
