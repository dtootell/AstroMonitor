import os, time

def watchdog(path_to_watch):
    #path_to_watch = "C:\APT_Images\CameraCCD_1\\2021-05-07\\apt_thumbs"
    before = dict ([(f, None) for f in os.listdir (path_to_watch)])
    while 1:
      time.sleep (2)
      after = dict ([(f, None) for f in os.listdir (path_to_watch)])
      added = [f for f in after if not f in before]
      removed = [f for f in before if not f in after]
      if added: print("Added: ", ", ".join (added))
      if removed: print("Removed: ", ", ".join (removed))
      before = after
      return