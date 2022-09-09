from pytube import YouTube
from tkinter import *
from tkinter.messagebox import *
import threading
import time

debug = False
bothContentObj = []
videoOnlyObj = []
audioOnlyObj = []
indexA = 0

class BothContent:

   def __init__(self, itag, resolution, fps, audioBtr, fileFormat):
      self.itag = itag
      self.resolution = resolution
      self.fps = fps
      self.audioBtr = audioBtr
      self.fileFormat = fileFormat.replace("video/", "")

class VideoOnly:
   
   def __init__(self, itag, resolution, fps, fileFormat):
      self.itag = itag
      self.resolution = resolution
      self.fps = fps
      self.fileFormat = fileFormat.replace("video/", "")

class AudioOnly:
   
   def __init__(self, itag, audioBtr, fileFormat):
      self.itag = itag
      self.audioBtr = audioBtr
      self.fileFormat = fileFormat.replace("audio/", "")


def callback(var):
   updateThread = threading.Thread(target=updateOnSeparateThread)
   updateThread.start()

def onselectUpdate():
   global indexA
   indexA = 0
   if indexA == 0:
      listboxAvailable.delete(0, listboxAvailable.size())
      listboxAvailable['height'] = 0
      for i in range(0, len(bothContentObj)):
         content = bothContentObj[i]
         labelTxt = content.resolution + " - " + str(content.fps) + "fps - " + content.audioBtr + " - " + content.fileFormat
         listboxAvailable.insert(i, labelTxt)
         listboxAvailable['height'] += 1
   elif indexA == 1:
      listboxAvailable.delete(0, listboxAvailable.size())
      listboxAvailable['height'] = 0
      for i in range(0, len(videoOnlyObj)):
         content = videoOnlyObj[i]
         labelTxt = content.resolution + " - " + str(content.fps) + "fps" + " - " + content.fileFormat
         listboxAvailable.insert(i, labelTxt)
         listboxAvailable['height'] += 1
   else:
      listboxAvailable.delete(0, listboxAvailable.size())
      listboxAvailable['height'] = 0
      for i in range(0, len(audioOnlyObj)):
         content = audioOnlyObj[i]
         labelTxt = content.audioBtr  + " - " + content.fileFormat
         listboxAvailable.insert(i, labelTxt)
         listboxAvailable['height'] += 1

def onselect(event):
   global indexA
   if len(event.widget.curselection()) > 0:
      selection = event.widget.curselection()
      indexA = selection[0]
      if indexA == 0:
         listboxAvailable.delete(0, listboxAvailable.size())
         listboxAvailable['height'] = 0
         for i in range(0, len(bothContentObj)):
            content = bothContentObj[i]
            labelTxt = content.resolution + " - " + str(content.fps) + "fps - " + content.audioBtr + " - " + content.fileFormat
            listboxAvailable.insert(i, labelTxt)
            listboxAvailable['height'] += 1
      elif indexA == 1:
         listboxAvailable.delete(0, listboxAvailable.size())
         listboxAvailable['height'] = 0
         for i in range(0, len(videoOnlyObj)):
            content = videoOnlyObj[i]
            labelTxt = content.resolution + " - " + str(content.fps) + "fps" + " - " + content.fileFormat
            listboxAvailable.insert(i, labelTxt)
            listboxAvailable['height'] += 1
      else:
         listboxAvailable.delete(0, listboxAvailable.size())
         listboxAvailable['height'] = 0
         for i in range(0, len(audioOnlyObj)):
            content = audioOnlyObj[i]
            labelTxt = content.audioBtr + " - " + content.fileFormat
            listboxAvailable.insert(i, labelTxt)
            listboxAvailable['height'] += 1

def downloadContent():
    try:
        if debug:
            print(str(urlVideo.get()))
        video = YouTube(str(urlVideo.get()))
        downloadThread = threading.Thread(target=dlOnSeparateThread, args=(video,))
        downloadThread.start()
    except Exception as e:
        if debug:
            print(e)
        errMsg = """L'URL « """ + str(urlVideo.get()) + """ » semble incorrecte ... """
        showerror("Erreur", errMsg)

def dlOnSeparateThread(video):
   if indexA == 0:
      chosenDownload = bothContentObj[listboxAvailable.curselection()[0]].itag
   elif indexA == 1:
      chosenDownload = videoOnlyObj[listboxAvailable.curselection()[0]].itag
   else:
      chosenDownload = audioOnlyObj[listboxAvailable.curselection()[0]].itag
   quitBtn['state'] = 'disabled'
   downloadBtn['state'] = 'disabled'
   video.streams.get_by_itag(chosenDownload).download()
   quitBtn['state'] = 'normal'
   downloadBtn['state'] = 'normal'

def updateOnSeparateThread():
   try:
      video = YouTube(str(urlVideo.get()))
      bothContent = video.streams.filter(progressive=True)
      videoOnly = video.streams.filter(adaptive=True, type="video")
      audioOnly = video.streams.filter(adaptive=True, type="audio")
      global bothContentObj
      for content in bothContent:
         bothContentObj.append(BothContent(content.itag, content.resolution, content.fps, content.abr, content.mime_type))
      global videoOnlyObj
      for content in videoOnly:
         videoOnlyObj.append(VideoOnly(content.itag, content.resolution, content.fps, content.mime_type))
      global audioOnlyObj
      for content in audioOnly:
         audioOnlyObj.append(AudioOnly(content.itag, content.abr, content.mime_type))
      print("URL valide")
      onselectUpdate()
   except Exception as e:
      print(e)
      print("URL invalide")

def onCloseAll():
    fenetre.quit()
    

fenetre = Tk()
titleLabel = Label(fenetre, text="YouTube downloader")
urlLabel = Label(fenetre, text="URL de la vidéo :")
downloadBtn=Button(fenetre, text="Télécharger")
downloadBtn['command'] = downloadContent
value = StringVar() 
value.set("")
value.trace("w", lambda name, index,mode, value=value: callback(value))
urlVideo = Entry(fenetre, textvariable=value, width=80)
quitBtn=Button(fenetre, text="Fermer", command=onCloseAll)
listboxDownloadType = Listbox(fenetre, width=100, height=3)
availableLabel = Label(fenetre, text="Contenu disponible :")
listboxAvailable = Listbox(fenetre, width=100, height=1)
titleLabel.pack(side=TOP)
quitBtn.pack(side=BOTTOM, padx=5, pady=5)
listboxAvailable.pack(side=BOTTOM, fill='both')
availableLabel.pack(side=BOTTOM)
listboxDownloadType.pack(side=BOTTOM, fill='both')
listboxDownloadType.insert(1, "Vidéo et audio")
listboxDownloadType.insert(2, "Vidéo uniquement")
listboxDownloadType.insert(3, "Audio uniquement")
listboxDownloadType.bind('<<ListboxSelect>>', onselect)
listboxDownloadType.select_set(0)
urlLabel.pack(side=LEFT, padx=5, pady=5)
urlVideo.pack(side=LEFT, padx=0, pady=5)
downloadBtn.pack(side=RIGHT, padx=5, pady=5)


fenetre.mainloop()
