import sys, traceback, Ice
import Temp
import time
import random
from threading import Thread

class TemperatureI(Temp.Temperature):  
  def getTemperature(self, current=None):
    return T
    
    


if __name__ == "__main__":
  status = 0
  ic = None
  T = 26
  try:
    ic = Ice.initialize(sys.argv)
    adapter = ic.createObjectAdapterWithEndpoints("TemperatureAdapter", "default -p 10001")
    object = TemperatureI()
    adapter.add(object, ic.stringToIdentity("Temperature"))
    adapter.activate()
    while True:
      T = T + random.random() - 0.5
      time.sleep(3)
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
