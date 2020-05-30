#!/usr/bin/python
# home/shon/workspace/comptime.py
# by Shon Garrison
# Created on: Aug 1, 2012

import pygtk, gtk, os
pygtk.require('2.0')

globalBank = 0.0
globalPreview =""

class Base:
    
    def destroy(self, widget, data=None):
        print "\n"
        print "Application is Now Exiting..."
        gtk.main_quit()

    def get_Date(self, widget):
        year, month, day = widget.get_date()
        self.lblCurDate.set_text(str(month + 1) + "/" + str(day) + "/" + str(year))
        
    def on_clear(self, widget):
        print "\n"
        print "Now Clearing Form..."
        self.entryEarned.set_text("")
        self.entryTaken.set_text("")
        self.combobox1.set_active(0) #sets to [Enter One]
        self.lblPreview.set_text("") #clears preview
        self.lbl6.set_text("0.0")  #clears daily balance for next calculation
        self.rbtnEarned.set_active(True) #sets focus to Earned Radio Button
        self.window.show_all()
        self.lblTaken.hide()  #hides Taken information until Taken button chosen
        self.entryTaken.hide()
        self.lbl2.hide()

    def on_calc_clicked(self, widget):
        global globalBank
        global globalPreview
        print "\n"
        print "Calculating New Daily Bal..."
        #sets up variables and gets Earned or Taken Values
        date = self.lblCurDate.get_text()
        calcearned = self.entryEarned.get_text()
        calctaken = self.entryTaken.get_text()
        preview = self.combobox1.get_active_text()
        taken = self.entryTaken.get_text()
        bank = globalBank
        
        #If Earned is blank, it will be set to zero, otherwise it gets Earned
        #entry
        if calcearned == "":
            calcearned = 0.0
        else:
            calcearned = self.entryEarned.get_text()
        #if Taken is blank, it will be set to zero, otherwise it gets Taken
        #entry
        if calctaken == "":
            calctaken = 0.0
        else:
            calctaken = self.entryTaken.get_text() 
        #convert string variables to decimal(float) for calculation
        calcearned = float(calcearned) * 1.5
        calctaken = float(calctaken)
        newbal = calcearned - calctaken
        newbank = newbal + float(bank)
        #convert to back to string to display in label
        newbal = str(newbal)
        newbank = str(newbank)
        print "\n"
        print "Setting Preview of New Balance Applied..."
        #shows current calculation daily balance
        self.lbl6.set_text(newbal)
        
        
        #shows current preview of time entry prior to writing text file
        self.lblPreview.set_text("Total time to enter on affidavit = " 
        + newbal + " hrs\n" + "-"*145 + "\n" + "Date" + " "*25 + "Reason"
        + " "*25 + "Earned" + " "*25 + "Taken" + " "*25 + "New Balance\n"
        + "-"*9 + " "*24 + "-"*12 + " "*25 + "-"*12 + " "*25 + "-"*10
        + " "*25 + "-"*21 + "\n" + str(date) + " "*13 + str(preview)
        + " "*25 + str(calcearned) + " "*40 + str(taken) + " "*30
        + newbank)

        globalPreview = (str(date) + " "*8 + str(preview) 
        + " "*10 + str(calcearned) + " "*18 + str(taken) + " "*17 
        + newbank + "\n"
        + "-"*90 + "\n")

    def on_apply_clicked(self, widget):
        global globalBank #access global variable
        print "\n"
        print "Applying New Daily Balance to Bank..."
        
        #incorporate to opening file
        bank2 = globalBank
        newDaybal= self.lbl6.get_text() #get daily balance text
        newbank2 = float(newDaybal) + bank2
        
        globalBank = (newbank2) #update global variable with new balance
        newbank2 = str(newbank2) #convert to string to put into label and file
        self.lbl5.set_text(newbank2) #put in bank label
        
        #writes to the bankfile
        f = open("/home/sgarrison/temp/test1.txt", "w")
        f.write(newbank2)
        f.close()
        
        #writes to runfile
        f2 = open("/home/sgarrison/temp/test2.txt", "a")
        f2.write(globalPreview)
        f2.close()
        
        
        self.on_clear(widget)

    def on_visible_callback(self, button, name):
        if button.get_active():
            state = "on"            
        else:
            state ="off"
        #print "Button", name, " is ", state
        if name == "Earned" and state == "on":
            #turns Earned Entry on for calculation and clear/hides
            #Taken Entry. Resets Daily Balance and Preview Labels
            self.entryEarned.show()
            self.lblPreview.set_text("")
            self.lbl6.set_text("0.0")
            self.entryEarned.set_text("")
            self.entryTaken.set_text("0.0")
            self.lblTaken.hide()
            self.entryTaken.hide()
            self.lbl2.hide()
        elif name == "Taken" and state == "on":
            #turns Taken Entry on for calculation and clear/hides
            #Earned Entry. Resets Daily Balance and Preview Labels
            self.entryEarned.set_text("0.0")
            self.entryTaken.set_text("")
            self.lblPreview.set_text("")
            self.lbl6.set_text("0.0")
            self.lblEarned.hide()
            self.entryEarned.hide()
            self.lbl1.hide()
            self.entryTaken.show()
        else:
            self.window.show_all()
            
    def on_text_changed(self, widget):
        self.entryEarned.set_text("")
        self.entryTaken.set_text("")
        self.lblPreview.set_text("") #clears preview
        self.lbl6.set_text("")  #clears daily balance for next calculation
        self.rbtnEarned.set_active(True) #sets focus to Earned Radio Button    

    #start program
    def __init__(self):

        #create new window, position, and size
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_position(gtk.WIN_POS_CENTER)
        self.window.set_size_request(600, 600)

        #connect x button on window to destroy event
        self.window.connect("destroy", self.destroy)

        #creates the applicable buttons
        self.btnClear = gtk.Button("Clear")
        self.btnCalc = gtk.Button("Calculate")
        self.btnApply = gtk.Button("Apply")
        self.btnClose = gtk.Button("Exit")
        
        #pulls bank amount from text file and loads it for globaBank and lbl5
        global globalBank
        #checks to see if the bankfile exists.  If it does, it pulls from it.
        if os.path.isdir("/home/sgarrison/temp/") and os.path.isfile("/home/sgarrison/temp/test1.txt"):
            f = open("/home/sgarrison/temp/test1.txt", "r")
            text = f.readline()
            globalBank = float(text)        
            f.close()
            
        else:
            #if bankfile dosen't exist, it creates it with a 0.0 balance then
            #reads from it.
            startBal = "0.0"
            f = open("/home/sgarrison/temp/test1.txt", "w")
            f.write(startBal)
            f.close()
            
            f = open("/home/sgarrison/temp/test1.txt", "r")
            text = f.readline()
            globalBank = float(text)        
            f.close()
            
            f = open("/home/sgarrison/temp/test2.txt", "w")
            f.write("Orange County Juvenile Probation Dept.\n"
            + "-"*40 + "\n" 
            + "Personal Comptime Sheet for: Shon Garrison\n"
            + "\n" 
            + "Date" + " "*13 + "Reason" + " "*11 + "Earned" + " "*16 
            + "Taken" + " "*15 + "New Balance\n"
            + "-"*9 + " "*7 + "-"*12 + " "*6 + "-"*7 + " "*15 
            + "-"*6  + " "*14 + "-"*12 + "\n")
        
        #creates the applicable labels
        self.lblPreview = gtk.Label("Preview")
        self.lbl7 = gtk.Label("Current Date Selected:")
        self.lblCurDate = gtk.Label("Select Activity Date")
        self.lblCase = gtk.Label("Case / Reason:")
        self.lbl1 = gtk.Label("hrs")
        self.lblEarned = gtk.Label("Earned")
        self.lblTaken = gtk.Label("Taken")
        self.lbl2 = gtk.Label("hrs")
        self.lbl3 = gtk.Label("Bank:")
        self.lbl5 = gtk.Label(text)
        self.lbl4 = gtk.Label("Daily Total:")
        self.lbl6 = gtk.Label("0.0")
        

        #creates the applicable text entry's
        self.entryEarned = gtk.Entry()
        self.entryTaken = gtk.Entry()
        
        #creates the applicable radio buttons and rbtnEarned group
        self.rbtnEarned = gtk.RadioButton(None, "Earned")
        self.rbtnTaken = gtk.RadioButton(self.rbtnEarned, "Taken")
        
        #sets Earned as active
        self.rbtnEarned.set_active(True)
        
        #connects radio buttons to visible function definition
        self.rbtnEarned.connect("toggled", self.on_visible_callback, "Earned")
        self.rbtnTaken.connect("toggled", self.on_visible_callback, "Taken")
        
        #creates the applicable comboBox
        self.combobox1 = gtk.combo_box_entry_new_text()
        
        #creates the list for the combobox
        self.combobox1.append_text("[Enter One]")
        self.combobox1.append_text("On-Call")
        self.combobox1.append_text("Det Visit")
        self.combobox1.append_text("Special Grp")
        self.combobox1.append_text("Transport")
        self.combobox1.append_text("Program")
        self.combobox1.append_text("Personal")
        self.combobox1.append_text("Sick")
        
        self.combobox1.connect("changed", self.on_text_changed)
        
        self.combobox1.set_active(0) #sets to [Enter One] on Load
        
        #creates calendar and separators
        calendar1 = gtk.Calendar()
        separator1 = gtk.HSeparator()
        separator2 = gtk.VSeparator()
        
        self.lbl6 = gtk.Label("0.0")
               
        #Sets up buttons to receive the appropriate signal
        #when clicked
        self.btnClose.connect("clicked", self.destroy)
        self.btnClear.connect("clicked", self.on_clear)
        self.btnCalc.connect("clicked", self.on_calc_clicked)
        self.btnApply.connect("clicked", self.on_apply_clicked)
        calendar1.connect("day_selected", self.get_Date)
        
        #builds widgets and containers and places them in the main 
        #window
        self.vbox5 = gtk.VBox()
        self.vbox5.pack_start(self.lbl3, expand=False, fill=True)
        self.vbox5.pack_start(self.lbl5, expand=False, fill=True)

        self.vbox6 = gtk.VBox()
        self.vbox6.pack_start(self.lbl4, expand=False, fill=True)
        self.vbox6.pack_start(self.lbl6, expand=False, fill=True)
       
        self.vbox4 = gtk.VBox()
        self.vbox4.pack_start(self.lbl7, expand=False, fill=True)
        self.vbox4.pack_start(self.lblCurDate, expand=True, fill=True)
        self.vbox4.pack_start(self.lblCase, expand=False, fill=True)
        self.vbox4.pack_start(self.combobox1, expand=False, fill=True)

        self.hbox1 = gtk.HBox()
        self.hbox1.pack_start(self.entryEarned)
        self.hbox1.pack_start(self.lbl1, expand=False, fill=True)

        self.hbox5 = gtk.HBox()
        self.hbox5.pack_start(self.entryTaken)
        self.hbox5.pack_start(self.lbl2, expand=False, fill=True)

        self.vbox2 = gtk.VBox()
        self.vbox2.pack_start(self.lblEarned)
        self.vbox2.pack_start(self.hbox1)
        self.vbox2.pack_start(self.lblTaken)
        self.vbox2.pack_start(self.hbox5)

        self.vbox3 = gtk.VBox()
        self.vbox3.pack_start(self.rbtnEarned, expand=True, fill=True)
        self.vbox3.pack_start(self.rbtnTaken, expand=True, fill=True)

        self.hbox7 = gtk.HBox(homogeneous=True)
        self.hbox7.pack_start(self.btnClear)
        self.hbox7.pack_start(self.btnCalc)
        self.hbox7.pack_start(self.btnApply)
        self.hbox7.pack_start(self.btnClose)

        self.hbox2 = gtk.HBox()
        self.hbox2.pack_start(calendar1)
        self.hbox2.pack_start(self.vbox4)

        self.hbox4 = gtk.HBox()
        self.hbox4.pack_start(self.vbox3, expand=True, fill=True)
        self.hbox4.pack_start(self.vbox2, expand=False, fill=True)

        self.hbox3 = gtk.HBox()
        self.hbox3.pack_start(self.vbox5)
        self.hbox3.pack_start(separator2)
        self.hbox3.pack_start(self.vbox6)

        self.vbox1 = gtk.VBox()
        self.vbox1.pack_start(self.hbox7)
        self.vbox1.pack_start(self.hbox2)
        self.vbox1.pack_start(self.hbox4)
        self.vbox1.pack_start(separator1)
        self.vbox1.pack_start(self.hbox3)
        self.vbox1.pack_start(self.lblPreview, expand=True, fill=True)
        
        #Packs everything in the Window
        self.window.add(self.vbox1)

        #Shows everything in the Window
        self.window.show_all()
        self.lblTaken.hide()
        self.entryTaken.hide()
        self.lbl2.hide()



    def main(self):
        gtk.main()

if __name__ == "__main__":
    base = Base()
    base.main()

