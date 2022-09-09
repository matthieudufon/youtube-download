class VideoOnly:
   
   def __init__(self, itag, resolution, fps, fileFormat):
      self.itag = itag
      self.resolution = resolution
      self.fps = fps
      self.fileFormat = fileFormat.replace("video", "")
