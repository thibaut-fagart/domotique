#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, time, re, glob
import datetime, pickle, time
import sharemem
import matplotlib.pyplot as plt
import calendar
import pytz
import matplotlib.dates 
from calendar import timegm
from matplotlib.dates import DayLocator, HourLocator, DateFormatter
from matplotlib.ticker import NullFormatter
import gtk

def write_file(self, path):

    now = datetime.datetime.now()
    if (now - self.memoNowStore > self.deltaTimeStore):
        self.memoNowStore = now
        self.data[now.strftime("%Y-%m-%d-%H-%M-%S")] = {}
        self.data[now.strftime("%Y-%m-%d-%H-%M-%S")]["tempSalleDeBain"] = self.shm.tempSdb
        self.data[now.strftime("%Y-%m-%d-%H-%M-%S")]["humSalleDeBain"] = self.shm.humSdb
        self.data[now.strftime("%Y-%m-%d-%H-%M-%S")]["tempSalon"] = self.shm.tempSalon
        self.data[now.strftime("%Y-%m-%d-%H-%M-%S")]["humSalon"] = self.shm.humSalon
        self.data[now.strftime("%Y-%m-%d-%H-%M-%S")]["tempCave"] = self.shm.tempCave
        self.data[now.strftime("%Y-%m-%d-%H-%M-%S")]["humCave"] = self.shm.humCave
        self.data[now.strftime("%Y-%m-%d-%H-%M-%S")]["tempExterieur"] = self.shm.tempExt
        self.data[now.strftime("%Y-%m-%d-%H-%M-%S")]["humExterieur"] = self.shm.humExt
        self.data[now.strftime("%Y-%m-%d-%H-%M-%S")]["tempPC"] = self.shm.tempPC
        self.data[now.strftime("%Y-%m-%d-%H-%M-%S")]["humPC"] = self.shm.humPC

    if (now - self.memoNowWrite > self.deltaTimeWrite):
        fileList = glob.glob(os.path.join(path,"Sensor_*.dat"))
        fileList.sort()

        if len(fileList) == 0:
            lastFileDate =  datetime.datetime(2000, 1, 1)
        else:
            fileYear  = int(fileList[-1].split('_')[-3])
            fileMonth = int(fileList[-1].split('_')[-2])
            fileDay   = int(fileList[-1].split('_')[-1].split('.')[0])
            lastFileDate = datetime.datetime(fileYear, fileMonth, fileDay)

        if (now - lastFileDate > self.deltaTimeFile):
            fileToBeWriten = os.path.join(path,"Sensor_%i_%02i_%02i.dat"%(now.year,now.month,now.day))
            os.system("touch %s"%fileToBeWriten)
            self.firstFileReading = False
        else:
            fileToBeWriten = fileList[-1]
            if self.firstFileReading:
                self.firstFileReading = False
                fichierRead = open(fileToBeWriten,'rb')
                self.dataOld = pickle.load(fichierRead)
                fichierRead.close()

                begin_time = datetime.datetime(fileYear, fileMonth, fileDay).strftime("%Y-%m-%d-%H-%M-%S")
                self.data_new = {}
                for i in self.dataOld:
                   if (i > begin_time):
                      self.data_new[i]=self.dataOld[i]

                self.data.update(self.data_new)

        self.memoNowWrite = now
        fichierWrite = open(fileToBeWriten,'w+b')
        pickle.dump(self.data,fichierWrite)
        fichierWrite.close()


def trace_graph(param1, param2, path):
        fileToBeWriten = selectFile(path)
        #
        if fileToBeWriten != None:
            fichierRead = open(fileToBeWriten,'rb')
            dataGraph = pickle.load(fichierRead)
            fichierRead.close()
            #
            xPoint = []
            datePoint = []
            y1Point = []
            y2Point = []
            #
            for point in dataGraph.keys():
                xPoint.append(point)
            xPoint.sort()
            for point in xPoint:
                datePoint.append(plottm(time.mktime(time.strptime(point,"%Y-%m-%d-%H-%M-%S"))))
                y1Point.append(dataGraph[point][param1])
                y2Point.append(dataGraph[point][param2])
            fig = plt.figure()
            ax = fig.add_subplot(211)
            bx = fig.add_subplot(212)
            ax.plot(datePoint, y1Point)
            bx.plot(datePoint, y2Point)
            #
            ax.xaxis.set_major_locator( DayLocator() )
            bx.xaxis.set_major_locator( DayLocator() )
            ax.xaxis.set_minor_locator( HourLocator() )
            bx.xaxis.set_minor_locator( HourLocator() )
            ax.xaxis.set_major_formatter( NullFormatter() )
            bx.xaxis.set_major_formatter( DateFormatter('%d-%b') )
            #
            def valueTemp(y1): return '%1.1f°C'%y1
            def valueHum(y2): return '%1.1f%'%y2
            ax.fmt_xdata = DateFormatter('%Y-%m-%d %H:%M')
            ax.fmt_ydata = valueTemp
            bx.fmt_xdata = DateFormatter('%Y-%m-%d %H:%M')
            bx.fmt_ydata = valueHum
            datemin = datePoint[0]
            datemax = datePoint[-1]
            ax.set_xlim(datemin, datemax)
            ax.set_ylim(int(min(y1Point))-1, int(max(y1Point))+2)
            bx.set_xlim(datemin, datemax)
            bx.set_ylim(int(min(y2Point))-1, int(max(y2Point))+2)
            ax.set_xlabel('Date', fontsize=10)
            ax.set_ylabel("Temperature "+param1.split("temp")[-1], fontsize=10)
            bx.set_xlabel('Date', fontsize=10)
            bx.set_ylabel("Humidity "+param2.split("hum")[-1], fontsize=10)
            ax.grid(True)
            bx.grid(True)
            #
            plt.show()

def selectFile(path):
    dialogue = gtk.FileChooserDialog("Open",
                                   None,
                                   gtk.FILE_CHOOSER_ACTION_OPEN,
                                   (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                    gtk.STOCK_OPEN, gtk.RESPONSE_OK))
    dialogue.set_default_response(gtk.RESPONSE_OK)
    dialogue.set_current_folder(path)

    filtre = gtk.FileFilter()
    filtre.set_name("dat files")
    filtre.add_pattern("*.dat")
    dialogue.add_filter(filtre)
    
    reponse = dialogue.run()

    if reponse == gtk.RESPONSE_OK:
        errlog =  dialogue.get_filename(), 'Selected'
        DomoUtils.printlog(errlog)
        filename = dialogue.get_filename()
        dialogue.destroy()
        return filename
    elif reponse == gtk.RESPONSE_CANCEL:
        errlog = 'No file selected'
        DomoUtils.printlog(errlog)
        dialogue.destroy()
        return None


# Convert a unix time u to plot time p
def plottm(u):
    return matplotlib.dates.date2num(datetime.datetime.fromtimestamp(u, pytz.utc))

# Convert a plot time p to unix time u
def unixtm(p):
    return timegm(matplotlib.dates.num2date(p, pytz.utc).utctimetuple())


#========== Programme principal =============
if __name__ == '__main__':

  print "use this function with DomoInterface.py"

