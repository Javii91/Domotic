import os

class Mod:
  name = ""
  code = ""
  mtype = ""
  active = True
  
  def __init__(self, name, code, mtype, active=True):
    self.name = name
    self.code = code
    self.mtype = mtype
    self.active = active
    #if self.isSensor():
    #  self.active = False
  
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
    if self.mtype == "Motion" or self.mtype == "Unknown":
      return True
    else:
      return False
