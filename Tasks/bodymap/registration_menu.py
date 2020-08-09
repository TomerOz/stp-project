from psychopy import gui

def registration(gui=gui):
        gui = gui.Dlg()
        gui.addField("Subject ID:")
        gui.addField("Condition Num:")
        gui.show()
        gui.close()
        #save data
        subj_id = gui.data[0]
        cond_num = int(gui.data[1])  # Control =0, retreat = 1
        return (subj_id, cond_num) #save this data as the excell name?
# cross object

# registration()