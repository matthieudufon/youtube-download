class AudioOnly:
   
   def __init__(self, itag, audioBtr, fileFormat):
      self.itag = itag
      self.audioBtr = audioBtr
      self.fileFormat = fileFormat.replace("audio/", "")
