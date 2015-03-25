import os

class Mod:
  name = ""
  code = ""
  mtype = ""
  active = True
  
  def __init__(self, name, code, mtype):
    self.name = name
    self.code = code
    self.mtype = mtype
  
  def __str__(self):
    return self.name + "\t\t" + self.code + "\t\t" + self.mtype + "\t\t" + str(self.active)
    
  def setName (self, name):
    self.name = name
    
  def setActive (self):
    self.active = True
    os.system("sudo heyu on " + self.code)
  
  def setInactive (self):
    self.active = False
    os.system("sudo heyu off " + self.code)
    
  def isSensor (self):
    if mtype == "Motion" or mtype == "Unknown":
      return True
    else:
      return False
