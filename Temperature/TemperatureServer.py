#!/usr/bin/python

import sys, traceback, Ice
import Temp
import time
import random
import subprocess
from threading import Thread
from Colors import Colors

class TemperatureI(Temp.Temperature):  
  def getTemperature(self, current=None):
    return T
    
    


if __name__ == "__main__":
  status = 0
  ic = None
  T = 26
  txt = Colors()
  try:
    ic = Ice.initialize(sys.argv)
    adapter = ic.createObjectAdapterWithEndpoints("TemperatureAdapter", ic.getProperties().getProperty("TemperatureServer.Endpoints"))
    object = TemperatureI()
    adapter.add(object, ic.stringToIdentity("Temperature"))
    adapter.activate()
  except:
    status = 1
    traceback.print_exc()

  sys.stdout.write(txt.warning("Monitoring sensor...\t"))
  sys.stdout.flush()
  p = subprocess.Popen("sudo temper-poll", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
  out = p.stdout.readline()
  if out.find("Found 0 devices") == -1:
    print txt.bold(txt.green("Running --> " + out ))
  else:
    print txt.bold(txt.fail("Failed --> " + out ))
    sys.exit()
  while True:
    p = subprocess.Popen("sudo temper-poll -qc", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    T = p.stdout.readline()
    time.sleep(1)
  ic.waitForShutdown()

  
    

  if ic:
    # Clean up
    try:
      ic.destroy()
    except:
      traceback.print_exc()
      status = 1

  sys.exit(status)
