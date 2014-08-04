#! /usr/bin/env python
# -*- coding: utf-8 -*-

import pygtk
import gtk, pango
import os, socket, re, datetime
import sys, glob
import gobject
import sharemem, DomoData

class param:
    Audio = {
             "Cuisine"     :0,
             "Chambre"     :0,
             "Salon"       :0,
             "SalleDeBain" :0}
    VMC = {
             "VMC"            :0,
             "Ventilo SdB"    :0,
             "Ventilo Couloir":0}
    VMCSpeed = {
             "Ventilo SdB"    :0,
             "Ventilo Couloir":0}
    di    = {
             "Porte"        :0,
             "Cave"         :0,
             "Chaudiere"    :0  }
    sensors = {
            "PC"            :{
                "Temperature" : {"Value" : 0, "Unit" : "°C", "Max" : 35, "Norm" : 30, "Min" : 20},
                "Humidity"    : {"Value" : 0, "Unit" : "%" , "Max" : 70, "Norm" : 50, "Min" : 10}},
            "Cave"          :{
                "Temperature" : {"Value" : 0, "Unit" : "°C", "Max" : 20, "Norm" : 18, "Min" : 12},
                "Humidity" :    {"Value" : 0, "Unit" : "%" , "Max" : 85, "Norm" : 80, "Min" : 60}},
            "Exterieur"     :{
                "Temperature" : {"Value" : 0, "Unit" : "°C", "Max" : 30, "Norm" : 25, "Min" : 10},
                "Humidity" :    {"Value" : 0, "Unit" : "%" , "Max" : 60, "Norm" : 50, "Min" : 10}},
            "Salon"         :{
                "Temperature" : {"Value" : 0, "Unit" : "°C", "Max" : 30, "Norm" : 25, "Min" : 10},
                "Humidity" :    {"Value" : 0, "Unit" : "%" , "Max" : 60, "Norm" : 50, "Min" : 10}},
            "SalleDeBain" :{
                "Temperature" : {"Value" : 0, "Unit" : "°C", "Max" : 30, "Norm" : 25, "Min" : 10},
                "Humidity" :    {"Value" : 0, "Unit" : "%" , "Max" : 60, "Norm" : 50, "Min" : 10}}}
    
class Interface_Domotic:
    def __init__(self, param=None):
        try :
            self.shm = sharemem.Globshm()
        except:
            self.shm = shm

        self.param = param
        self.AudioRoom_CheckButton = {}
        self.Logic_CheckButton = {}
        self.VMC_CheckButton = {}
        self.scale = {}
        self.monitoringFrame = {}

        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect("delete_event", self.delete)
        self.window.set_border_width(10)

        self.table = gtk.VBox()
        self.window.add(self.table)
        # Create a new notebook, place the position of the tabs
        self.notebook = gtk.Notebook()
        self.notebook.set_tab_pos(gtk.POS_TOP)
        self.table.pack_start(self.notebook, True, True, 0)
        self.notebook.show()
        self.show_tabs = True
        self.show_border = True

        self.AudioInit()
        self.VMCInit()
        self.MonitoringInit()
        self.LogInit()

        # Set what page to start at 
        self.notebook.set_current_page(2)

        button = gtk.Button("close")
        button.connect("clicked", self.delete)
        self.table.pack_start(button, False, True, 0)

        button.show()
        self.table.show()
        self.window.show()

        self.refresh()


    def MonitoringInit(self):
        self.monitoringFrame["main"] = gtk.Frame("Monitoring")
        self.monitoringFrame["main"].set_border_width(10)

        for sensor in self.param.sensors.keys():
            self.monitoringFrame[sensor] = gtk.Frame(sensor)
            self.monitoringFrame[sensor].set_border_width(10)
            self.monitoringFrame[sensor].set_size_request(150, 130)

        self.monitoringFrame["Logic"] = gtk.Frame("Logic")
        self.monitoringFrame["Logic"].set_border_width(10)

        label = gtk.Label("Monitoring")
        self.monit_main_vbox = gtk.VBox()
        self.monit1_hbox = gtk.HBox()
        self.monit2_hbox = gtk.HBox()
        self.monit_vboxLogic = gtk.VBox()

        for directInput in self.param.di.keys():
            self.Logic_CheckButton[directInput] = gtk.CheckButton(directInput)
            self.Logic_CheckButton[directInput].connect("clicked",self.monitorLogic,directInput)
            self.Logic_CheckButton[directInput].modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse("grey"))
            self.Logic_CheckButton[directInput].modify_bg(gtk.STATE_SELECTED, gtk.gdk.color_parse("grey"))
            self.monit_vboxLogic.pack_start(self.Logic_CheckButton[directInput], False, True, 0)
        self.monitoringFrame["Logic"].add(self.monit_vboxLogic)
            
        for sensor in self.param.sensors.keys():
            self.sensorList = self.param.sensors[sensor].keys()
            self.param.sensors[sensor]["vbox"] = gtk.VBox()
            for parameter in self.sensorList:
                self.param.sensors[sensor][parameter]["hbox"] = gtk.HBox()
                self.param.sensors[sensor][parameter]["gtkVal"] = gtk.Label(str(self.param.sensors[sensor][parameter]["Value"]))
                self.param.sensors[sensor][parameter]["gtkUnit"] = gtk.Label(self.param.sensors[sensor][parameter]["Unit"])
                self.param.sensors[sensor][parameter]["hbox"].pack_end(self.param.sensors[sensor][parameter]["gtkUnit"], False, True, 10)
                self.param.sensors[sensor][parameter]["hbox"].pack_end(self.param.sensors[sensor][parameter]["gtkVal"], False, True, 0)
                self.param.sensors[sensor]["vbox"].pack_start(self.param.sensors[sensor][parameter]["hbox"], False, True, 4)
            self.param.sensors[sensor]["gtkButton"] = gtk.Button("Graph")
            self.param.sensors[sensor]["gtkButton"].connect("clicked",self.traceGraph,sensor)
            self.param.sensors[sensor]["vbox"].pack_end(self.param.sensors[sensor]["gtkButton"], False, True, 0)
            self.monitoringFrame[sensor].add(self.param.sensors[sensor]["vbox"])

        self.monit1_hbox.add(self.monitoringFrame["Cave"])
        self.monit1_hbox.add(self.monitoringFrame["Salon"])
        self.monit1_hbox.add(self.monitoringFrame["SalleDeBain"])
        self.monit2_hbox.add(self.monitoringFrame["PC"])
        self.monit2_hbox.add(self.monitoringFrame["Exterieur"])
        self.monit2_hbox.add(self.monitoringFrame["Logic"])
        self.monit_main_vbox.add(self.monit1_hbox)
        self.monit_main_vbox.add(self.monit2_hbox)
        self.monitoringFrame["main"].add(self.monit_main_vbox)
        self.monitoringFrame["main"].show_all()
        self.notebook.append_page(self.monitoringFrame["main"], label)

    def AudioInit(self):
        self.audio_frame = gtk.Frame("Audio")
        self.audio_frame.set_border_width(10)
        self.audio_frame.set_size_request(400, 250)

        label = gtk.Label("Audio")

        self.AudioManualAuto_Button = gtk.Button("Set Audio in Manual Mode")
        self.AudioManualAuto_Button.connect("clicked",self.AudioManualAuto)
        for room in self.param.Audio.keys():
            self.AudioRoom_CheckButton[room] = gtk.CheckButton("%s Ampli power"%room)
            self.AudioRoom_CheckButton[room].modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse("grey"))
            self.AudioRoom_CheckButton[room].modify_bg(gtk.STATE_SELECTED, gtk.gdk.color_parse("grey"))
            self.AudioRoom_CheckButton[room].connect("clicked", self.AudioRoom)

        self.AudioDelay_entry = gtk.Entry(3)
        self.AudioDelay_entry.set_width_chars(4)
        self.AudioDelay_entry.set_text(str(self.shm.audioMaxDelay))
        self.AudioDelay_Text1 = gtk.Label("Max delay")
        self.AudioDelay_Text2 = gtk.Label("s")
        self.AudioDelaySet_Button = gtk.Button(" Set Delay ")
        self.AudioDelaySet_Button.connect("clicked",self.AudioDelaySet)

        self.audio_hbox = gtk.HBox()
        self.audio_hbox.pack_start(self.AudioDelay_Text1, False, True, 2)
        self.audio_hbox.pack_start(self.AudioDelay_entry, False, True, 2)
        self.audio_hbox.pack_start(self.AudioDelay_Text2, False, True, 2)
        self.audio_hbox.pack_start(self.AudioDelaySet_Button, False, True, 50)

        self.audio_vbox = gtk.VBox()
        self.audio_vbox.pack_start(self.AudioManualAuto_Button, False, True, 10)
        for room in self.param.Audio.keys():
            self.audio_vbox.pack_start(self.AudioRoom_CheckButton[room], False, True, 0)
        self.audio_vbox.pack_start(self.audio_hbox, False, True, 10)

        self.audio_frame.add(self.audio_vbox)
        self.audio_frame.show_all()
        self.notebook.append_page(self.audio_frame, label)

    def LogInit(self):
        self.log_frame = gtk.Frame("Log")
        self.log_frame.set_border_width(10)
        self.log_frame.set_size_request(400, 250)

        label = gtk.Label("Log")

        self.Log_entry = gtk.TextView()
        self.LogBufferTexte = self.Log_entry.get_buffer()

        self.log_frame.add(self.Log_entry)
        self.log_frame.show_all()
        self.notebook.append_page(self.log_frame, label)

    def VMCInit(self):
        self.VMC_frame = gtk.Frame("VMC")
        self.VMC_frame.set_border_width(10)
        self.VMC_frame.set_size_request(100, 75)

        label = gtk.Label("VMC")

        self.VMCManualAuto_Button = gtk.Button("Set VMC in Manual Mode")
        self.VMCManualAuto_Button.connect("clicked",self.VMCManualAuto)

        adjustment = gtk.Adjustment(80, 0, 100, 5, 10, 0)

        for ventilo in self.param.VMC.keys():
            self.VMC_CheckButton[ventilo] = gtk.CheckButton(ventilo)
            self.VMC_CheckButton[ventilo].modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse("grey"))
            self.VMC_CheckButton[ventilo].modify_bg(gtk.STATE_SELECTED, gtk.gdk.color_parse("grey"))
            self.VMC_CheckButton[ventilo].connect("clicked",self.VMCCtrl)
            self.scale[ventilo] = gtk.HScale(adjustment)
            self.scale[ventilo].set_digits(0)
            self.scale[ventilo].set_update_policy(gtk.UPDATE_DELAYED)
            self.scale[ventilo].connect("value-changed", self.scale_moved,ventilo)

        self.VMC_vbox = gtk.VBox()
        self.VMC_vbox.pack_start(self.VMCManualAuto_Button, False, True, 10)
        for ventilo in self.param.VMC.keys():
            self.VMC_vbox.pack_start(self.VMC_CheckButton[ventilo], False, True, 0)
            if ventilo in self.param.VMCSpeed.keys():
               self.VMC_vbox.pack_start(self.scale[ventilo], False, True, 0)

        self.VMC_frame.add(self.VMC_vbox)
        self.VMC_frame.show_all()
        self.notebook.append_page(self.VMC_frame, label)

    def scale_moved(self, event, ventilo):
         self.param.VMCSpeed[ventilo] = int(self.scale[ventilo].get_value() / 100. * 1023.) 

    def sensor_update(self):
        self.param.sensors["PC"]["Temperature"]["Value"]          = self.shm.tempPC
        self.param.sensors["PC"]["Humidity"]["Value"]             = self.shm.humPC
        self.param.sensors["Exterieur"]["Temperature"]["Value"]   = self.shm.tempExt
        self.param.sensors["Exterieur"]["Humidity"]["Value"]      = self.shm.humExt
        self.param.sensors["Cave"]["Temperature"]["Value"]        = self.shm.tempCave
        self.param.sensors["Cave"]["Humidity"]["Value"]           = self.shm.humCave
        self.param.sensors["SalleDeBain"]["Temperature"]["Value"] = self.shm.tempSdb
        self.param.sensors["SalleDeBain"]["Humidity"]["Value"]    = self.shm.humSdb
        self.param.sensors["Salon"]["Temperature"]["Value"]       = self.shm.tempSalon
        self.param.sensors["Salon"]["Humidity"]["Value"]          = self.shm.humSalon

        for sensor in self.param.sensors.keys():
            for parameter in self.sensorList:
                self.param.sensors[sensor][parameter]["gtkVal"].set_text("%.1f"%self.param.sensors[sensor][parameter]["Value"])
                self.param.sensors[sensor][parameter]["gtkVal"].modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse(self.colorLable(sensor,parameter)))
                self.param.sensors[sensor][parameter]["gtkUnit"].modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse(self.colorLable(sensor,parameter)))
		self.param.sensors[sensor][parameter]["gtkVal"].modify_font(pango.FontDescription("12"))
		self.param.sensors[sensor][parameter]["gtkUnit"].modify_font(pango.FontDescription("12"))
        self.monitoringFrame["main"].show_all()

        self.param.Audio["Cuisine"] = self.shm.audioCuisinePower 
        self.param.Audio["SalleDeBain"] = self.shm.audioSdbPower 
        self.param.Audio["Salon"] = self.shm.audioSalonPower 
        self.param.Audio["Chambre"] = self.shm.audioChambrePower 

        for room in self.param.Audio.keys():
            if self.param.Audio[room]:
                self.AudioRoom_CheckButton[room].modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse("#008000"))
                self.AudioRoom_CheckButton[room].modify_bg(gtk.STATE_SELECTED, gtk.gdk.color_parse("#008000"))
                self.AudioRoom_CheckButton[room].set_active(self.param.Audio[room])
            else:
                self.AudioRoom_CheckButton[room].modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse("grey"))
                self.AudioRoom_CheckButton[room].modify_bg(gtk.STATE_SELECTED, gtk.gdk.color_parse("grey"))
                self.AudioRoom_CheckButton[room].set_active(self.param.Audio[room])

        self.param.VMC["VMC"] = self.shm.VMCPower 
        self.param.VMC["Ventilo SdB"] = self.shm.ventiloSdbPower 
        self.param.VMC["Ventilo Couloir"] = self.shm.ventiloCouloirPower 

        self.shm.ventiloSdbReq = self.param.VMCSpeed["Ventilo SdB"]
        self.shm.ventiloCouloirReq = self.param.VMCSpeed["Ventilo Couloir"]

        for ventilo in self.param.VMC.keys():
            if self.param.VMC[ventilo]:
                self.VMC_CheckButton[ventilo].modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse("#008000"))
                self.VMC_CheckButton[ventilo].modify_bg(gtk.STATE_SELECTED, gtk.gdk.color_parse("#008000"))
                self.VMC_CheckButton[ventilo].set_active(self.param.VMC[ventilo])
            else:
                self.VMC_CheckButton[ventilo].modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse("grey"))
                self.VMC_CheckButton[ventilo].modify_bg(gtk.STATE_SELECTED, gtk.gdk.color_parse("grey"))
                self.VMC_CheckButton[ventilo].set_active(self.param.VMC[ventilo])

        if not self.param.di["Cave"] and self.shm.presenceCave:
            presenceInput = True
        elif self.param.di["Cave"] and not self.shm.presenceCave:
            presenceOutput = True
        else:
            presenceInput = False
            presenceOutput = False

        self.param.di["Cave"] = self.shm.presenceCave
        self.param.di["Porte"] = self.shm.porteFermee
        self.param.di["Chaudiere"] = self.shm.forceChaudiere

        now = datetime.datetime.now()
        for directInput in self.param.di.keys():
            if self.param.di[directInput]:
                self.Logic_CheckButton[directInput].modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse("#008000"))
                self.Logic_CheckButton[directInput].modify_bg(gtk.STATE_SELECTED, gtk.gdk.color_parse("#008000"))
                if directInput == "Cave":
                    if presenceInput:
                        inputLogDate = "Presence detected the %s/%s/%s at %s:%s"%(now.day,now.month,now.year,now.hour,now.minute)
                        self.LogBufferTexte.insert(self.LogBufferTexte.get_start_iter(),"%s \n"%inputLogDate)
                        DomoUtils().printlog(inputLogDate)
            else:
                self.Logic_CheckButton[directInput].modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse("grey"))
                self.Logic_CheckButton[directInput].modify_bg(gtk.STATE_SELECTED, gtk.gdk.color_parse("grey"))
                if directInput == "Cave":
                    if presenceOutput:
                        outputLogDate = "End of presence the %s/%s/%s at %s:%s"%(now.day,now.month,now.year,now.hour,now.minute)
                        self.LogBufferTexte.insert(self.LogBufferTexte.get_start_iter(),"%s \n"%outputLogDate)
                        DomoUtils().printlog(outputLogDate)


    def colorLable(self,location,sensor):
        if self.param.sensors[location][sensor]["Value"] > self.param.sensors[location][sensor]["Max"]:
            return "#FF0000"  # red
        elif self.param.sensors[location][sensor]["Value"] > self.param.sensors[location][sensor]["Norm"]:
            return "#D2691E"  # Orange
        elif self.param.sensors[location][sensor]["Value"] < self.param.sensors[location][sensor]["Min"]:
            return "#0000CC"  # blue
        else:
            return "#008000"  # green

    def delete(self, widget):
        gtk.main_quit()
        return False

    def traceGraph(self, widget, sensor):
        path = "/home/dimi/prog/data"
        DomoData.trace_graph('temp'+sensor, 'hum'+sensor,path)

    def AudioDelaySet(self, widget):
        self.shm.audioMaxDelay = int(self.AudioDelay_entry.get_text())

    def AudioManualAuto(self, widget):
        if self.AudioManualAuto_Button.get_label() == "Set Audio in Manual Mode":
            self.AudioManualAuto_Button.set_label("Set Audio in Automatic Mode")
            self.shm.audioMan = 1
            self.shm.audioCurrentDelay = 0
        else:
            self.AudioManualAuto_Button.set_label("Set Audio in Manual Mode")
            self.shm.audioMan = 0
            self.shm.audioCurrentDelay = 0

    def VMCManualAuto(self, widget):
        if self.VMCManualAuto_Button.get_label() == "Set VMC in Manual Mode":
            self.VMCManualAuto_Button.set_label("Set VMC in Automatic Mode")
            self.shm.VMCMan = 1
        else:
            self.VMCManualAuto_Button.set_label("Set VMC in Manual Mode")
            self.shm.VMCMan = 0

    def monitorLogic(self,widget,directInput):
        if directInput == "Chaudiere":
            self.shm.forceChaudiere = int(self.Logic_CheckButton[directInput].get_active())

    def VMCCtrl(self, widget):
        if self.shm.VMCMan == True:
            self.shm.VMCPower = int(self.VMC_CheckButton["VMC"].get_active())
            self.shm.ventiloSdbPower = int(self.VMC_CheckButton["Ventilo SdB"].get_active())
            self.shm.ventiloCouloirPower = int(self.VMC_CheckButton["Ventilo Couloir"].get_active())

    def AudioRoom(self, widget ):
        if self.shm.audioMan == True:
            self.shm.audioCuisinePower = int(self.AudioRoom_CheckButton["Cuisine"].get_active())
            self.shm.audioSalonPower = int(self.AudioRoom_CheckButton["Salon"].get_active())
            self.shm.audioChambrePower = int(self.AudioRoom_CheckButton["Chambre"].get_active())
            self.shm.audioSdbPower = int(self.AudioRoom_CheckButton["SalleDeBain"].get_active())

    def refresh(self):
        self.sensor_update()
        gobject.timeout_add(1000, self.refresh)


if __name__ == '__main__':    

   Interface_Domotic(param)
   gtk.main()

