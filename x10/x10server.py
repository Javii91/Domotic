import sys, traceback, Ice, os
import x10
from Mod import Mod
from Colors import Colors
import subprocess
from threading import Thread


Modules = []


class NetI(x10.Net):
  def sendMsg(self, s, current=None):
    print s
    
  def showEnvironment(self, current=None):
    print txt.underline(txt.bold("House " + props["x10server.HouseCode"] + " Environment"))
    print "Name\t\tCode\t\tType\t\tActive"
    for i in Modules:
      if i.active:
        print txt.green(str(i))
      else:
        print txt.gray(str(i))
  
  def setActive(self, name, current=None):
    found = False
    for i in Modules:
      if (i.name == name) and not i.isSensor:
        print txt.warning("Activating module " + i.name + "...")
        i.setActive()
        found = True
        break
    if found == False:
      print txt.warning("Module " + name + " not found.")
   
  def setInactive(self, name, current=None):
    found = False
    for i in Modules:
      if (i.name == name) and not i.isSensor:
        print txt.warning("Desactivating module " + i.name + "...")
        i.setInactive()
        found = True
        break
    if found == False:
      print txt.warning("Module " + name + " not found.")
   
  def addModule (self, name, code, mtype, current=None):
    Modules.append(Mod(name, code, mtype))
    
  def changeNamebyCode(self, name, code, current=None):
    for i in Modules:
      if i.code == code:
        i.setName(name)
        break
  
  def changeName(self, newname, name, current=None):
    for i in Modules:
      if i.name == name:
        i.setName(newname)
        break
  
  def isActivebyCode(self, code, current=None):
    for i in Modules:
      if i.code == code:
        return i.active
  
  def isActive(self, name, current=None):
    for i in Modules:
      if i.name == name:
        return i.active

  def checkSensor (self, current=None):
    sys.stdout.write(txt.warning("Monitoring sensor modules..."))
    sys.stdout.flush()
    p = subprocess.Popen("heyu monitor", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    print txt.bold(txt.green("Running"))
    while True:
      out = p.stdout.readline()
      if out.find("rcvi addr unit") != -1:
        mcode = out[44:46]
        out = p.stdout.readline()
        for i in Modules:
          found = False
          if i.code == mcode and i.isSensor:
            found = True
            if out.find("rcvi func           On : hc") != -1:
              print txt.warning("  Module '" + txt.bold(i.name)) + txt.warning("' has been activated.")
              i.setActive()
              break
            if out.find("rcvi func          Off : hc") != -1:
              print txt.warning("  Module '" + txt.bold(i.name)) + txt.warning("' has been deactivated.")
              i.setInactive()
              break
        if found == False:
          print txt.warning("  Recognised module not added before. Now added as noName.")
          self.addModule("noName", mcode, "Unknown")  
          for i in Modules:
            if i.code == mcode and i.isSensor:
              if out.find("rcvi func           On : hc") != -1:
                print txt.warning("  Module '" + txt.bold(i.name)) + txt.warning("' has been activated.")
                i.setActive()
                break
              if out.find("rcvi func          Off : hc") != -1:
                print txt.warning("  Module '" + txt.bold(i.name)) + txt.warning("' has been deactivated.")
                i.setInactive()
                break
    
    

        
        
def checkModules(props):
  sys.stdout.write(txt.warning("Loading environment..."))
  sys.stdout.flush()
  for i in range(1,17):
    if "x10server.HouseModule." + str(i) + ".name" in props:
      Modules.append(Mod(props["x10server.HouseModule." + str(i) + ".name"], props["x10server.HouseCode"] + str(i) , props["x10server.HouseModule." + str(i) + ".type"]))
  print txt.bold(txt.green("Done"))

txt = Colors()
status = -1
ic = None

## Initialize HEYU system
sys.stdout.write(txt.warning("Initializing x10 system... "))
sys.stdout.flush()
proc = subprocess.Popen("sudo heyu start", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
(out, err) = proc.communicate()

try:
    ic = Ice.initialize(sys.argv)
    adapter = ic.createObjectAdapterWithEndpoints("NetAdapter", ic.getProperties().getProperty("x10server.Endpoints"))
    if err != "":
      print txt.bold(txt.fail("Failed"))
      print txt.fail("Can't open tty line.  Check the permissions.")
      status = 1
      sys.exit(status)
    else:
      print txt.bold(txt.green("Done"))
    status = 0
    
    props = ic.getProperties().getPropertiesForPrefix("x10server")
    checkModules(props)
    
    object = NetI()
    #object.showEnvironment()
    #object.setActive("lampara")
    #object.showEnvironment()
    #object.setInactive("lampara")
    #object.showEnvironment()
    thread = Thread(target = object.checkSensor())
    thread.start()
    
    adapter.add(object, ic.stringToIdentity("Net"))
    adapter.activate()
    print txt.warning("Reading client request...")
    ic.waitForShutdown()
except:
    if status == -1:
      print txt.bold(txt.fail("Failed"))
      print txt.fail("Address already in use")
      sys.exit(status = 1)
    traceback.print_exc()
    status = 1

if ic:
    # Clean up
    try:
        ic.destroy()
    except:
        traceback.print_exc()
        status = 1

sys.exit(status)
