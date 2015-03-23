import sys, traceback, Ice
import x10, Mod
from Mod import Mod
from Colors import Colors

Modules = []


class NetI(x10.Net):
  def sendMsg(self, s, current=None):
    print s
    
  def showEnvironment(self, current=None):
    print txt.underline(txt.bold(txt.warning("House " + props["x10server.HouseCode"] + " Environment")))
    print "Name\t\tCode\t\tType\t\tActive"
    for i in Modules:
      if i.active:
        print txt.green(str(i))
      else:
        print txt.gray(str(i))
  
  def setActive(self, name, current=None):
    found = False
    for i in Modules:
      if i.name == name:
        print txt.warning("Activating module " + i.name + "...")
        i.setActive()
        found = True
        break
    if found == False:
      print txt.warning("Module " + name + " not found.")
   
  def setInactive(self, name, current=None):
    found = False
    for i in Modules:
      if i.name == name:
        print txt.warning("Desactivating module " + i.name + "...")
        i.setInactive()
        found = True
        break
    if found == False:
      print txt.warning("Module " + name + " not found.")

      
        
        
def checkModules(props):
  for i in range(1,17):
    if "x10server.HouseModule." + str(i) + ".name" in props:
      Modules.append(Mod(props["x10server.HouseModule." + str(i) + ".name"], props["x10server.HouseCode"] + str(i) , props["x10server.HouseModule." + str(i) + ".type"]))

txt = Colors()
status = 0
ic = None
try:
    ic = Ice.initialize(sys.argv)
    props = ic.getProperties().getPropertiesForPrefix("x10server")
    checkModules(props)
    adapter = ic.createObjectAdapterWithEndpoints("NetAdapter", ic.getProperties().getProperty("x10server.Endpoints"))
    object = NetI()
    object.showEnvironment()
    object.setActive("lampara")
    object.showEnvironment()
    object.setInactive("lampara")
    object.showEnvironment()
    adapter.add(object, ic.stringToIdentity("Net"))
    adapter.activate()
    ic.waitForShutdown()
except:
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
