import pandas as pd
import os
import shutil


class BeforeRunnigPreparation(object):
    def __init__(self, sub_dir):
        self.sub_dir = sub_dir

    def edit_audio_data(self, subject_num):
        '''TO USE THIS FUNCTION ON EACH AUDIO FILE FROM THE STP SERVER >> EDITED DATA (HIPPA DRIVE)'''
        if not os.path.exists(self.sub_dir +"/" + "subject " +str(subject_num) +"/" + "audio_files"):
            path = self.sub_dir+"/"+"edited_audio_"+str(subject_num)+'/'
            dir = os.listdir(path)
            audio_file_name = [s for s in dir if "audio_data" in s][0] #look for audio_data_19...
            df = pd.read_csv(path+audio_file_name)
            df['SentenceType'].replace({'Negative':'neg'}, regex=True,inplace = True)
            df['SentenceType'].replace({'Neutral':'ntr'}, regex=True,inplace = True)
            filepath_out = path+'audio_data.xlsx'
            df.to_excel(filepath_out)
            os.rename(path,self.sub_dir+"/subject "+str(subject_num))
        else:
            pass

    def bodymapTOP20(self, subject_num):
        path = self.sub_dir+'/subject '+subject_num
        path_BM = r'Tasks/bodymap/input/Audio/'
        if not os.path.exists(os.path.join(path_BM, str(subject_num))):
            df = pd.read_excel(path+r"/audio_data.xlsx")
            neutral_top20 = df['TAPlistNumber'].iloc[0:20]
            negative_top20 = df['TAPlistNumber'].iloc[40:60]
            audio_dir = os.listdir(path+r"/audio_files")
            for file in audio_dir:
                if file[0] == 'r':
                    # find sentecne num in audio name
                    ie = file.rfind("e")
                    audio_num = file[ie + 1:ie + file[ie:].find('_')]
                    for i, TAP_number in enumerate(neutral_top20):
                        if int(TAP_number) == int(audio_num):
                            if not os.path.exists(path_BM + subject_num):
                                 os.mkdir(path_BM + subject_num)
                                 os.mkdir(path_BM + subject_num +'/neu')
                            src = path + '/audio_files/'+file
                            dst = path_BM + subject_num +'/neu'
                            shutil.copy(src, dst)
                            os.rename(path_BM + subject_num +'/neu/'+file, path_BM + subject_num +'/neu/' +str(i)+'_' +file)
            for file in audio_dir:
                if file[0] == 'r':
                    # find sentecne num in audio name
                    ie = file.rfind("e")
                    audio_num = file[ie + 1:ie + file[ie:].find('_')]
                    for i, TAP_number in enumerate(negative_top20):
                        if int(TAP_number) == int(audio_num):
                            if not os.path.exists(path_BM + subject_num+ '/neg'):
                                os.mkdir(path_BM + subject_num + '/neg')
                            src = path + '/audio_files/' + file
                            dst = path_BM + subject_num + '/neg'
                            shutil.copy(src, dst)
                            os.rename(path_BM + subject_num +'/neg/'+file, path_BM + subject_num + '/neg/' + str(i) + '_' + file)
        else:
            pass

    def run_for_all_subjects_for_IA_Tasks(self):
        '''organize audio_data.csv into xlsx
        copy all audio files into a new directory called audio files'''
        dir = os.listdir(self.sub_dir)
        ###organise audio data xlsx and rename the file- TO ACTIVATE WHEN I'll HAVE THE NEW PARTICIPANTS
        for file_name in dir:#FOR EXAMPLE  'edited_audio_10 ' ####move all the audio files into a file called audio_files
            dir = os.listdir(self.sub_dir+'/'+file_name)
            if not os.path.exists(self.sub_dir+'/'+file_name+'/audio_files'):
                os.mkdir(self.sub_dir+'/'+file_name+'/audio_files')
            source = self.sub_dir + '/' + file_name
            dest1 = self.sub_dir + '/' + file_name + '/audio_files'
            files = os.listdir(source)
            for f in files:
                if 'rerecorded' in f: ###to remove the string 'rerecorded' for the IA tasks
                    os.rename(self.sub_dir +'/'+ file_name +'/'+ f, self.sub_dir +'/'+ file_name + '/'+ f[11:])
                    shutil.move(source + '/' + f[11:], dest1)
                elif 're' in f:
                    shutil.move(source + '/' + f, dest1)
            #SUBJECT_ID = file_name[file_name.index('_')+1:]
            self.edit_audio_data(str(file_name[-3:]))  # subject Number ###FOR 3 digist
            #edit_audio_data(str(file_name[-2:])) #retreat - ID with 2 digits
            ##TO CHANGE THE WAY IT TAKE IT
            self.bodymapTOP20(str(file_name[-3:])) #for control - ###FOR 3 digist
            #bodymapTOP20(str(file_name[-2:])) #retreat - ID with 2 digits

def main():
    brp = BeforeRunnigPreparation("Subjects")
    brp.run_for_all_subjects_for_IA_Tasks()

if __name__ == "__main__":
   main()
