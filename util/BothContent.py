class BothContent:

   def __init__(self, itag, resolution, fps, audioBtr, fileFormat):
      self.itag = itag
      self.resolution = resolution
      self.fps = fps
      self.audioBtr = audioBtr
      self.fileFormat = fileFormat.replace("video/", "")
