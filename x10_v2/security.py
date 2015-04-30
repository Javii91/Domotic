from gi.repository import Gtk,GObject,Gdk,GLib,GdkPixbuf
from Mod import Mod
import sys, traceback, Ice
import x10
from Colors import Colors
from threading import Thread, Timer
import threading
import cv2
import cv
import sys
import cairo
import jderobot
import numpy
import Image
import time, datetime
from datetime import datetime




class viewGUI:

  Modus = []
  x10 = ["localhost", "10000"]
  Camera = ["localhost","9999"]
  CameraRun = False
  motion = False
  record_rdy1 = False
  record_rdy2 = False
  record = False

  def __init__(self, propsx10 = None, propscam= None):
    self.builder = Gtk.Builder()
    self.builder.add_from_file("security.glade")
    self.builder.connect_signals(self)
    self.window = self.builder.get_object("window1")
    self.window.connect("delete-event", Gtk.main_quit)
    style_provider = Gtk.CssProvider()

    css = """#Active {background: #04B404;}#NoActive {background: #B40404;}"""

    style_provider.load_from_data(css)

    Gtk.StyleContext.add_provider_for_screen(
      Gdk.Screen.get_default(), 
      style_provider,     
      Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
    )
    

      
    self.notebook = Gtk.Notebook()
    self.window.add(self.notebook)
    
    self.cameratab()
    self.load_other()
    
    if propsx10:
      self.checkModules(propsx10)
             
      self.environment()
      self.notebook.append_page(self.maingrid, Gtk.Label("Environment"))
      
      threading.Thread(target=self.askdformods).start()
      threading.Thread(target=self.checkAlarm).start()
      
      #self.maingrid.show_all()
    else: 
      self.load_environment()
      self.notebook.append_page(self.vbox2, Gtk.Label("Environment"))
    
    
    
    

    self.notebook.append_page(self.vbox, Gtk.Label("Camera"))
    self.notebook.append_page(self.vbox3, Gtk.Label("Other"))
    
    #threading.Thread(target=self.askdformods).start()
    #threading.Thread(target=self.checkAlarm).start()
    
    
    self.window.show_all()
    self.on_camrun()
    
  def load_other(self):
    self.vbox3 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
    self.vbox3.pack_start(Gtk.Label("Save cfg to file:"), False, False, 0)
    self.hbox2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=3)
    self.vbox3.pack_start(self.hbox2, False, False, 0)
    
    
    self.fileother = Gtk.Entry()
    self.fileother.set_text("security.cfg")
    image = Gtk.Image(stock=Gtk.STOCK_SAVE_AS)
    self.otheropt = Gtk.Button(label=" Save", image=image)
    self.otheropt.connect("clicked", self.save_config, self.fileother.get_text())
    self.hbox2.pack_start(self.fileother, True, False, 0)
    self.hbox2.pack_start(self.otheropt, True, False, 0)
    
  def save_config (self, button, name):
    f = open (name, "w")
    if self.x10[0] != "" and self.x10[1] != 0:
      f.write("# Environment configuration \n")
      f.write("x10.Proxy=Net:default -h "+self.x10[0]+" -p " + self.x10[1] +"\n")
      f.write("\n")
      for i in self.Modus:
        f.write("x10.Module."+i.code+".name="+  i.name +"\n")
        f.write("x10.Module."+i.code+".type="+  i.mtype +"\n")
        f.write("x10.Module."+i.code+".active="+  str(i.active) +"\n")
        f.write("x10.Module."+i.code+".alarm_act="+  str(i.alarm_act) +"\n")
        f.write("x10.Module."+i.code+".alarm_start="+  i.alarm_start +"\n")
        f.write("x10.Module."+i.code+".alarm_end="+  i.alarm_end +"\n")
        a = 0
        for n in i.rules:
          f.write("x10.Module."+i.code+".rules."+a+"="+ n+"\n")
          a += 1
        f.write("\n")
    if self.Camera[0] != "" and self.Camera[1] != 0:
      f.write("# Camera configuration \n")
      f.write("cam.Proxy=CameraA:default -h "+self.Camera[0]+" -p " + self.Camera[1] +"\n")
    f.close()

  def load_environment (self):
    self.vbox2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
    
    image = Gtk.Image(stock=Gtk.STOCK_PROPERTIES)
    self.envopt = Gtk.Button(label=" Properties", image=image)
    self.envopt.connect("clicked", self.cameracfg, "env")
    self.vbox2.pack_start(self.envopt, True, False, 0)
    
  def on_camrun (self):
    if self.CameraRun == False:
      self.motiontable.hide()
      self.motiontable2.hide() 
      self.labelmt.hide()
      self.ad.hide()
      motion = False
      self.radbut3.set_active(True)
      self.ad.set_active(False)
    else:
      self.motiontable2.show() 
      self.labelmt.show()
      self.ad.show()
      self.radbut3.set_active(True)
    
  def cameratab (self):
    self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
    self.cam=Gtk.Image()
    self.vbox.pack_start(self.cam, True, False, 0)
    

    image = Gtk.Image(stock=Gtk.STOCK_PROPERTIES)
    self.camopt = Gtk.Button(label=" Properties", image=image)
    self.camopt.connect("clicked", self.cameracfg, "cam")
    self.vbox.pack_start(self.camopt, True, False, 0)
    
    
    
    self.hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
    self.vbox.pack_start(self.hbox, True, False, 0)
    
    
    self.labelmt = Gtk.Label("Motion detection ")
    self.hbox.pack_start(self.labelmt, True, True, 0)
    self.ad = Gtk.Switch()
    self.ad.connect("button-press-event", self.on_motion)
    self.ad.set_active(False)
    self.hbox.pack_start(self.ad, True, True, 0)
    
    self.radbut3 = Gtk.RadioButton(group=None,label="No record")
    
    
    self.hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
    self.motiontable = Gtk.Table(4, 2, True)
    self.motiontable.attach(Gtk.Label(""), 0, 1, 0, 1,yoptions=Gtk.AttachOptions.SHRINK)
    self.motiontable.attach(Gtk.Label(""), 0, 1, 2, 3,yoptions=Gtk.AttachOptions.SHRINK)
    self.motiontable.attach(Gtk.Label("Objects in motion:"), 0, 1, 1, 2,yoptions=Gtk.AttachOptions.SHRINK)
    self.campeoplecounter = Gtk.Label("0")
    self.motiontable.attach(self.campeoplecounter, 1, 2, 1, 2,yoptions=Gtk.AttachOptions.SHRINK)
    self.radbut1 = Gtk.RadioButton(group=self.radbut3,label="Record when motion of")
    self.motiontable.attach(self.radbut1, 0, 1, 3, 4,yoptions=Gtk.AttachOptions.SHRINK)
    self.motiontable.attach(Gtk.Label("Camera"), 1, 2, 3, 4,yoptions=Gtk.AttachOptions.SHRINK)
    self.vbox.pack_start(self.motiontable, True, True, 0)
    
    
    self.motiontable2 = Gtk.Table(2, 2, False)
    self.radbut2 = Gtk.RadioButton(group=self.radbut3, label="Record when motion of")
    self.motiontable2.attach(self.radbut2, 0, 1, 0, 1,yoptions=Gtk.AttachOptions.SHRINK)
    self.motiontable2.attach(self.radbut3, 0, 1, 1, 2,yoptions=Gtk.AttachOptions.SHRINK)
    self.combomotion = Gtk.ComboBoxText()
    self.load_sensors_combotext(self.combomotion)
    self.motiontable2.attach(self.combomotion, 1, 2, 0, 1,yoptions=Gtk.AttachOptions.SHRINK)  
    self.vbox.pack_start(self.motiontable2, True, True, 0)
   
    self.radbut1.connect("toggled", self.motionrec_tog, 1)
    self.radbut2.connect("toggled", self.motionrec_tog, 2)
    self.radbut3.connect("toggled", self.motionrec_tog, 3)
    
  def load_sensors_combotext(self, widget):
    widget.remove_all()
    for i in self.Modus:
      if i.isSensor():
        widget.append_text("("+i.code+") "+i.name)
    widget.set_active(0)
  
  def motionrec_tog (self, button, n):
    if n == 1:
      self.record_rdy1 = True
      self.record_rdy2 = False
    if n == 2:
      self.record_rdy2 = True
      self.record_rdy1 = False
    if n == 3:
      self.record_rdy1 = False
      self.record_rdy2 = False
      self.record = False
    

  def on_motion (self, button, event):
    if self.motion == False:
      self.motion = True
      self.motiontable.show() 
    else:
      self.motion = False
      self.motiontable.hide() 
      self.radbut3.set_active(True)
    
  def cameracfg (self, button, tab):
    self.window6 = self.builder.get_object("dialog5")
    self.window6.connect("delete_event", self.on_button10_clicked)
    if tab == "cam":
      self.builder.get_object("entry4").set_text(self.Camera[0])
      self.builder.get_object("entry5").set_text(self.Camera[1])
    elif tab == "env":
      self.builder.get_object("entry4").set_text(self.x10[0])
      self.builder.get_object("entry5").set_text(self.x10[1])
    self.lastsignal0 = self.builder.get_object("button11").connect("clicked", self.on_button11_clicked, tab)
    self.window6.show_all()

    
    
  def camera (self):
    def data_to_image (data, rgbObgr):
      img= Image.fromstring('RGB', (data.description.width,data.description.height), data.pixelData, 'raw', rgbObgr)
      pix = numpy.array(img)
      return pix
  
    try:
      #ic2 = Ice.initialize()    
      #obj2 = ic2.stringToProxy('cameraA:default -h '+self.Camera[0]+' -p ' + self.Camera[1])
      obj2 = ic.stringToProxy('cameraA:default -h '+self.Camera[0]+' -p ' + self.Camera[1])
      cam = jderobot.CameraPrx.checkedCast(obj2)
    except:
      print "Connection Failed"
      Gdk.threads_enter()
      self.CameraRun = False
      self.on_camrun()
      Gdk.threads_leave()
      return
    
    # motion
    frame_size = (320,240)
    color_image = cv.CreateImage(frame_size, 8, 3)
    grey_image = cv.CreateImage(frame_size, cv.IPL_DEPTH_8U, 1)
    moving_average = cv.CreateImage(frame_size, cv.IPL_DEPTH_32F, 3)
    
    first = True
    first_rec = True
    first_zero = False
    
    
    while True:
      if threads == False or self.CameraRun == False:
        break
      
      data = cam.getImageData("RGB8")
      if self.record == False:
        first_rec = True
      
      if first_rec == True and self.record == True:
        out = cv2.VideoWriter(datetime.now().ctime() + '.avi',cv2.cv.CV_FOURCC('X','V','I','D'), 10.0, frame_size)
        first_rec = False
        
      if self.motion == True:
        # motion
        imagen = data_to_image (data, "RGB")
        color_image = cv.fromarray(imagen)
      
        # Smooth to get rid of false positives
        cv.Smooth(color_image, color_image, cv.CV_GAUSSIAN, 3, 0)

        if first:
          difference = color_image
          temp = color_image
          cv.ConvertScale(color_image, moving_average, 1.0, 0.0)
          first = False
        else:
          cv.RunningAvg(color_image, moving_average, 0.030, None)

        # Convert the scale of the moving average.
        cv.ConvertScale(moving_average, temp, 1.0, 0.0)

        # Minus the current frame from the moving average.
        cv.AbsDiff(color_image, temp, difference)

        # Convert the image to grayscale.
        cv.CvtColor(difference, grey_image, cv.CV_RGB2GRAY)

        # Convert the image to black and white.
        cv.Threshold(grey_image, grey_image, 70, 255, cv.CV_THRESH_BINARY)

        # Dilate and erode to get people blobs
        cv.Dilate(grey_image, grey_image, None, 18)
        cv.Erode(grey_image, grey_image, None, 10)

        storage = cv.CreateMemStorage(0)
        contour = cv.FindContours(grey_image, storage, cv.CV_RETR_CCOMP, cv.CV_CHAIN_APPROX_SIMPLE)
        points = []
        
        n = 0
        while contour:
          n = n +1
          bound_rect = cv.BoundingRect(list(contour))
          contour = contour.h_next()

          pt1 = (bound_rect[0], bound_rect[1])
          pt2 = (bound_rect[0] + bound_rect[2], bound_rect[1] + bound_rect[3])
          points.append(pt1)
          points.append(pt2)
          cv.Rectangle(color_image, pt1, pt2, cv.CV_RGB(0,255,0), 1)
      
        if self.record_rdy1 and n > 0:
          self.record = True
          first_zero = True
          
        if first_rec == True and self.record == True:
          out = cv2.VideoWriter(datetime.now().ctime() + '.avi',cv2.cv.CV_FOURCC('X','V','I','D'), 10.0, frame_size)
          first_rec = False
        
        
          
        if self.record and n == 0 and first_zero:
          first_zero = False
          t_start = time.time()
        elif self.record and n == 0 and time.time() - t_start > 5:
          self.record = False
      
        if self.record:
          imagen2 = data_to_image (data, "BGR")
          out.write(imagen2)
        Gdk.threads_enter()
        self.campeoplecounter.set_markup("<b>"+str(n)+"</b>")
        self.img_pixbuf = GdkPixbuf.Pixbuf.new_from_data(Image.fromarray(numpy.array(color_image)).tostring('raw'), GdkPixbuf.Colorspace.RGB, False, 8, data.description.width,data.description.height, data.description.width*3,None, None)
        self.cam.set_from_pixbuf(self.img_pixbuf)
        Gdk.threads_leave()
        
        
      
      else:
        if self.record:
          imagen = data_to_image (data, "BGR")
          out.write(imagen)
        Gdk.threads_enter()
        self.img_pixbuf = GdkPixbuf.Pixbuf.new_from_data(data.pixelData, GdkPixbuf.Colorspace.RGB, False, 8, data.description.width,data.description.height, data.description.width*3,None, None)
        self.cam.set_from_pixbuf(self.img_pixbuf)
        Gdk.threads_leave()
        
        

          
      
      
    #ic2.destroy()
  
  def setAlarm(self, name, sh, sm, eh, em, act):
    for i in self.Modus:
      if i.name == name:
        i.setcfgAlarm(sh,sm,eh,em,act)
        break
  
  
  def getAlarm(self, name):
    for i in self.Modus:
      if i.name == name:
        alarm = i.getcfgAlarm()
        return [alarm[0], int(alarm[1]), int(alarm[2])/5, int(alarm[3]),int(alarm[4])/5]



  def checkAlarm (self):
    while True:
      if threads == False:
        break
      now = datetime.now()
      t = str(now.hour).zfill(2)  + ":" + str(now.minute)
      for i in self.Modus:
        if i.alarm_act:
          if t == i.alarm_start:
            self.net.setActive(i.name)
          if t == i.alarm_end:
            self.net.setInactive(i.name)
      time.sleep(1) 
      
      
  def askdformods (self):
    while True:
      if threads == False:
        break
      newmod = self.parseMod(self.net.getEnvironment())
      if len(self.Modus) != len(newmod):
        Gdk.threads_enter()
        self.table.destroy()
        self.modtable()
        Gdk.threads_leave()
      else:
        for i in self.Modus:
          for n in newmod:
            found = False
            if i.compare(n):
              found = True
              break
          if found == False:
            Gdk.threads_enter()
            self.table.destroy()
            self.modtable()
            Gdk.threads_leave()
            break
              


  def parsemymods (self):
    rdymods = []
    for i in self.Modus:
      if i.isSensor() == False:
        rdymods.append("("+i.code+") "+i.name)

    return rdymods

  def parseRules (self, s): 
    pieces = []
    if s != "":
      pieces = s.split("|")
    return pieces
    
    
  def getRule(self, name):
    for i in self.Modus:
      if i.name == name:
        alarm = i.getRules()
        return "|".join(alarm)

  def setRule(self, name, SenState, selectMod, Action):
    for i in self.Modus:
      if i.name == name:
        i.setRules(SenState,selectMod,Action)
        break

  def delRule(self, name, rule):
    for i in self.Modus:
      if i.name == name:
        i.delRules(rule)
        break

  def doRules(self,name, state):
    for i in self.Modus:
      if i.name == name:
        rules = i.getRules()
        for r in rules:
          pieces = r.split("|")
          if pieces[0] == "On" and state == True:
            if pieces[2] == "Activate":
              for m in self.Modus:
                if m.name == pieces[1].split(")")[1][1:]:
                  self.net.setActive(m.name)
            else:
              for m in self.Modus:
                if m.name == pieces[1].split(")")[1][1:]:
                  self.net.setInactive(m.name)
          elif pieces[0] == "Off" and state == False:
            if pieces[2] == "Activate":
              for m in self.Modus:
                if m.name == pieces[1].split(")")[1][1:]:
                  self.net.setActive(m.name)
            else:
              for m in self.Modus:
                if m.name == pieces[1].split(")")[1][1:]:
                  self.net.setInactive(m.name)
        


  def on_button9_clicked (self, button, mod):
    self.setRule(mod.name,self.builder.get_object("comboboxtext7").get_active_text(),self.combotextmodus.get_active_text(), self.builder.get_object("comboboxtext9").get_active_text())
    self.builder.get_object("label13").set_label("")
    self.window5.hide()
    self.change3.disconnect(self.lastsignal3)
    self.table2.destroy()
    self.rultable(mod)
    return True

  def on_delrul (self, button, mod, rule):
    self.net.delRule(mod.name, rule)
    self.table2.destroy()
    self.rultable(mod)
		

  def changerule (self, button, mod):
    self.window5 = self.builder.get_object("dialog4")
    self.builder.get_object("label13").set_label(mod.name)
    self.window5.connect("delete_event", self.on_button8_clicked)
    self.window5.show_all()
    self.change3 = self.builder.get_object("button9")
    self.lastsignal3 = self.change3.connect("clicked", self.on_button9_clicked, mod)
    self.combotextmodus = self.builder.get_object("comboboxtext8")
    self.builder.get_object("comboboxtext7").set_active(0)
    self.builder.get_object("comboboxtext9").set_active(0)
    rdymods = self.parsemymods()
    self.combotextmodus.remove_all()
    for i in rdymods:
      self.combotextmodus.append_text(i)
    self.combotextmodus.set_active(0)


  def rultable (self, mod):
    rules = self.parseRules(self.getRule(mod.name))

    if len(rules) == 0:
      self.table2 = Gtk.Table(2, 4, False)
    else:
      self.table2 = Gtk.Table(len(rules)/3, 4, False)
    self.box5.pack_start(self.table2, True, True, 0)
    
    optionsLabel = Gtk.Label()
    optionsLabel.set_markup("<b>Del</b>")
    self.table2.attach(optionsLabel, 0, 1, 0, 1)
    
    codeLabel = Gtk.Label()
    codeLabel.set_markup("<b>State</b>")
    self.table2.attach(codeLabel, 1, 2, 0, 1)
    
    nameLabel = Gtk.Label()
    nameLabel.set_markup("<b>Module</b>")
    self.table2.attach(nameLabel, 2, 3, 0, 1)
    
    typeLabel = Gtk.Label()
    typeLabel.set_markup("<b>Action</b>")
    self.table2.attach(typeLabel, 3, 4, 0, 1)
    
    
    if len(rules) == 0:
      self.window3.show_all()
      return
    
    for i in range(len(rules)/3):
      deletebuttonimage = Gtk.Image(stock=Gtk.STOCK_CANCEL)
      deletebutton = Gtk.Button(image=deletebuttonimage)
      deletebutton.connect("clicked", self.on_delrul, mod, i) 
      self.table2.attach(deletebutton, 0, 1, 3*i+1, 3*i+2)
      self.table2.attach(Gtk.Label(rules[3*i]), 1, 2, 3*i+1, 3*i+2)
      self.table2.attach(Gtk.Label(rules[3*i+1]), 2, 3, 3*i+1, 3*i+2)
      self.table2.attach(Gtk.Label(rules[3*i+2]), 3, 4, 3*i+1, 3*i+2)

    self.window3.show_all()

    
  def changename (self, button, mod):
    self.window3 = self.builder.get_object("dialog1")
    self.builder.get_object("entry1").set_text(mod.name)
    self.window3.connect("delete_event", self.on_button4_clicked)
    self.window3.show_all()
    self.change = self.builder.get_object("button5")
    self.box5 = self.builder.get_object("box5")
    self.lastsignal = self.change.connect("clicked", self.on_button5_clicked, mod)
    self.senalarm = self.builder.get_object("switch1")
    self.addrule = self.builder.get_object("button3")
    self.lastsignal4 = self.addrule.connect("clicked", self.changerule, mod)
    self.rultable(mod)
    
    




  def changenamepro (self, button, mod):
    self.window4 = self.builder.get_object("dialog3")
    self.window4.show_all()
    self.builder.get_object("entry3").set_text(mod.name)
    self.window4.connect("delete_event", self.on_button1_clicked)
    self.change2 = self.builder.get_object("button2")
    self.lastsignal2 = self.change2.connect("clicked", self.on_button2_clicked, mod)
    self.toff = self.builder.get_object("radiobutton1")
    self.ton = self.builder.get_object("radiobutton2")
    self.starth = self.builder.get_object("comboboxtext3")
    self.startm = self.builder.get_object("comboboxtext4")
    self.endh = self.builder.get_object("comboboxtext5")
    self.endm = self.builder.get_object("comboboxtext6")
    # if no estaba programado antes
    alarm = self.getAlarm(mod.name)
    self.starth.set_active(alarm[1])
    self.startm.set_active(alarm[2])
    self.endh.set_active(alarm[3])
    self.endm.set_active(alarm[4])
    if alarm[0]:
      self.ton.set_active(True)
    else:
      self.toff.set_active(True)
    # else si lo estaba, valor dado
    
    
  def on_button1_clicked(self, button, event=None):
    self.builder.get_object("entry3").set_text("")
    self.window4.hide()
    self.change2.disconnect(self.lastsignal2)
    return True
    
  def on_button2_clicked(self, button, mod):
    name = self.builder.get_object("entry3").get_text()
    if mod.name != name:
      self.net.changeNamebyCode(name, mod.code)
    self.setAlarm(mod.name, self.starth.get_active_text(), self.startm.get_active_text(),self.endh.get_active_text(),self.endm.get_active_text(),self.ton.get_active())
    self.table.destroy()
    self.modtable()
    self.builder.get_object("entry3").set_text("")
    self.window4.hide()
    self.change2.disconnect(self.lastsignal2)
    
  def on_button4_clicked(self, button, event=None):
    self.builder.get_object("entry1").set_text("")
    self.window3.hide()
    self.change.disconnect(self.lastsignal)
    self.addrule.disconnect(self.lastsignal4)
    self.table2.destroy()
    return True

  def on_button8_clicked(self, button, event=None):
    self.builder.get_object("label13").set_label("")
    self.window5.hide()
    self.change3.disconnect(self.lastsignal3)
    return True
    
  def on_button10_clicked(self, button, event=None):
    self.builder.get_object("button11").disconnect(self.lastsignal0)
    self.radbut3.set_active(True)
    self.CameraRun = False
    self.motion = False
    self.window6.hide()
    self.on_camrun()
    return True    

  def on_button11_clicked(self, button, tab):
    self.builder.get_object("button11").disconnect(self.lastsignal0)
    if tab == "cam":
      self.CameraRun = False
      self.window6.hide()
      self.Camera[0] = self.builder.get_object("entry4").get_text()
      self.Camera[1] = self.builder.get_object("entry5").get_text()
      if self.CameraRun == False:
        self.CameraRun = True
        self.on_camrun()
        self.radbut3.set_active(True)
        threading.Thread(target=self.camera).start()
    elif tab == "env":
      self.window6.hide()
      self.x10[0] = self.builder.get_object("entry4").get_text()
      self.x10[1] = self.builder.get_object("entry5").get_text()
      try:
        #ic = Ice.initialize()
        #base = ic.stringToProxy(ic.getProperties().getProperty("x10view.Proxy"))
        base = ic.stringToProxy('Net:default -h '+self.x10[0]+' -p ' + self.x10[1])
        self.net = x10.NetPrx.checkedCast(base)
      except:
        print "Connection Failed"
        #ic.destroy()
        return
        
      self.envopt.destroy()
      self.environment()
      self.vbox2.pack_start(self.maingrid, True, False, 0)
      
      threading.Thread(target=self.askdformods).start()
      threading.Thread(target=self.checkAlarm).start()
      self.maingrid.show_all()
      
  
    
  def on_button5_clicked(self, button, mod):
    name = self.builder.get_object("entry1").get_text()
    if mod.name != name:
      self.net.changeNamebyCode(name, mod.code)
    self.table.destroy()
    self.modtable()
    self.builder.get_object("entry1").set_text("")
    self.window3.hide()
    self.change.disconnect(self.lastsignal)
    self.addrule.disconnect(self.lastsignal4)
    self.table2.destroy()
    
  def environment(self):
    self.maingrid = Gtk.Table(2, 1, False)  
    
    self.modtable()
    
    image = Gtk.Image(stock=Gtk.STOCK_ADD)
    add_button = Gtk.Button(label="Add Module", image=image)
    add_button.connect("clicked", self.on_addModule)
    self.maingrid.attach(add_button, 0, 1, 1, 2,yoptions=Gtk.AttachOptions.SHRINK)
    
    
  def modtable (self):
    self.Modus = self.assingmod(self.parseMod(self.net.getEnvironment()))
    if len(self.Modus) == 0:
      self.table = Gtk.Table(1, 5, True)
    else:
      self.table = Gtk.Table(len(self.Modus), 5, True)
    self.maingrid.attach(self.table, 0, 1, 0, 1,yoptions=Gtk.AttachOptions.SHRINK)
    
    houseLabel = Gtk.Label()
    houseLabel.set_markup("<b><big>House A</big></b>")
    self.table.attach(houseLabel, 2, 3, 0, 1,yoptions=Gtk.AttachOptions.SHRINK)
    
    optionsLabel = Gtk.Label()
    optionsLabel.set_markup("<b>Options</b>")
    self.table.attach(optionsLabel, 0, 1, 1, 2,yoptions=Gtk.AttachOptions.SHRINK)
    
    codeLabel = Gtk.Label()
    codeLabel.set_markup("<b>Code</b>")
    self.table.attach(codeLabel, 1, 2, 1, 2,yoptions=Gtk.AttachOptions.SHRINK)
    
    nameLabel = Gtk.Label()
    nameLabel.set_markup("<b>Name</b>")
    self.table.attach(nameLabel, 2, 3, 1, 2,yoptions=Gtk.AttachOptions.SHRINK)
    
    typeLabel = Gtk.Label()
    typeLabel.set_markup("<b>Type</b>")
    self.table.attach(typeLabel, 3, 4, 1, 2,yoptions=Gtk.AttachOptions.SHRINK)
    
    activeLabel = Gtk.Label()
    activeLabel.set_markup("<b>Active</b>")
    self.table.attach(activeLabel, 4, 5, 1, 2,yoptions=Gtk.AttachOptions.SHRINK)
    
    if len(self.Modus) == 0:
      self.window.show_all()
      self.on_camrun()
      return
    
    for i in self.Modus:
      optionsbuttons = Gtk.Table(1, 2, True)
      self.table.attach(optionsbuttons, 0, 1, self.Modus.index(i)+2, self.Modus.index(i)+3,yoptions=Gtk.AttachOptions.SHRINK)
      deletebuttonimage = Gtk.Image(stock=Gtk.STOCK_CANCEL)
      deletebutton = Gtk.Button(image=deletebuttonimage)
      deletebutton.connect("clicked", self.on_delModule, i)
      changebuttonimage = Gtk.Image(stock=Gtk.STOCK_EXECUTE)
      changebutton = Gtk.Button(image=changebuttonimage)
      if (self.net.isSensor(i.name)):
        changebutton.connect("clicked", self.changename, i)
      else:
        changebutton.connect("clicked", self.changenamepro, i)
      optionsbuttons.attach(deletebutton, 0, 1, 0, 1)
      optionsbuttons.attach(changebutton, 1, 2, 0, 1)

      if i.active == False:
        
        self.table.attach(Gtk.Label(i.code), 1, 2, self.Modus.index(i)+2, self.Modus.index(i)+3,yoptions=Gtk.AttachOptions.SHRINK)
        self.table.attach(Gtk.Label(i.name), 2, 3, self.Modus.index(i)+2, self.Modus.index(i)+3,yoptions=Gtk.AttachOptions.SHRINK)
        self.table.attach(Gtk.Label(i.mtype), 3, 4, self.Modus.index(i)+2, self.Modus.index(i)+3,yoptions=Gtk.AttachOptions.SHRINK)
        if self.net.isSensor(i.name):
          l4 = Gtk.Button(" ")
          l4.set_name('NoActive')
        else:
          l4 = Gtk.Switch()
          l4.set_active(False)
          l4.connect("button-press-event", self.on_actModule, i)
        self.table.attach(l4, 4, 5, self.Modus.index(i)+2, self.Modus.index(i)+3,yoptions=Gtk.AttachOptions.SHRINK)

      else:
        l1 = Gtk.Label()
        l1.set_markup('<span color="#347C2C">' + i.code + '</span>')
        self.table.attach(l1, 1, 2, self.Modus.index(i)+2, self.Modus.index(i)+3,yoptions=Gtk.AttachOptions.SHRINK)
        
        l2 = Gtk.Label()
        l2.set_markup('<span color="#347C2C">' + i.name + '</span>')
        self.table.attach(l2, 2, 3, self.Modus.index(i)+2, self.Modus.index(i)+3,yoptions=Gtk.AttachOptions.SHRINK)
        
        l3 = Gtk.Label()
        l3.set_markup('<span color="#347C2C">' + i.mtype + '</span>')
        self.table.attach(l3, 3, 4, self.Modus.index(i)+2, self.Modus.index(i)+3,yoptions=Gtk.AttachOptions.SHRINK)
        
       
        if self.net.isSensor(i.name):
          l4 = Gtk.Button(label=" ")
          l4.set_name('Active')
        else:
          l4 = Gtk.Switch()
          l4.set_active(True)
          l4.connect("button-press-event", self.on_actModule, i)
        self.table.attach(l4, 4, 5, self.Modus.index(i)+2, self.Modus.index(i)+3,yoptions=Gtk.AttachOptions.SHRINK)

    self.window.show_all()
    self.on_camrun()
        

  def on_delModule(self, button, mod):
    self.net.delModulebyCode(mod.code)
    self.table.destroy()
    self.modtable()
  
  def on_actModule(self, button, event, mod):
    
    if mod.active:
      self.net.setInactive(mod.name)
    else:
      self.net.setActive(mod.name)
    self.table.destroy()
    self.modtable()

    


        
  def on_addModule(self, button):
    self.window2 = self.builder.get_object("dialog2")
    self.window2.connect("delete_event", self.on_del)
    self.window2.show_all()
    self.codex = self.builder.get_object("comboboxtext1")
    self.typex = self.builder.get_object("comboboxtext2")
    self.codex.remove_all()
    wombocode = ["A1","A2","A3","A4","A5","A6","A7","A8","A9","A10","A11","A12","A13","A14","A15","A16"]  
    for i in self.Modus:
      wombocode.remove(i.code)
    for n in wombocode:
      self.codex.append_text(n)
    self.codex.set_active(0)
    self.typex.set_active(0)
    
  def on_button7_clicked(self, button):
    code = self.builder.get_object("comboboxtext1").get_active_text()
    mtype = self.builder.get_object("comboboxtext2").get_active_text()
    name = self.builder.get_object("entry2").get_text()
    #Modus.append(Mod(name, code, mtype))
    #anadir modulo
    if len(self.Modus) <= 16:
      self.net.addModule(name, code, mtype)
    self.table.destroy()
    self.modtable()
    
    self.load_sensors_combotext(self.combomotion)
    
    self.builder.get_object("entry2").set_text("")
    self.window2.hide()
    
  def on_button6_clicked(self, button):
    self.builder.get_object("entry2").set_text("")
    self.window2.hide()
    
  def on_del(self, button, other):
    self.window2.hide()
    return True
    
      
      
  def parseMod (self,s):
    def str_to_bool(s):
      if s == 'True':
         return True
      else:
         return False
             
    pieces = []
    if s != "":
      mo = []
      pieces = s.split("|")
      for i in range(0,len(pieces)/4):
        newmod = Mod(pieces[i*4+1], pieces[i*4], pieces[i*4+2], str_to_bool(pieces[i*4+3]))
        mo.append(newmod)
      return mo
    return pieces
    
  def assingmod (self, mo):
    mo2 = list(self.Modus)
    if len(mo2) == 0:
      mo2 = mo
      return mo2
    if len(mo) > len(mo2):
      mo2.append(mo[-1])
      return mo2
    for n in mo2:
      found = False
      for i in mo:
        if i.code == n.code:
          if i.isSensor() and i.active != n.active:
            self.doRules(n.name, i.active)
            if self.record_rdy2 and self.combomotion.get_active_text() == "("+n.code+") "+n.name:
              if i.active:
                self.record = True
              else:
                self.record = False
              
          found = True
          n.name = i.name
          n.active = i.active
          n.mtype = i.mtype
          break
      if found == False:
        #elemento n borrado
        del mo2[mo2.index(n)]
    return mo2
    
  def checkModules(self, props):
    def str_to_bool(s):
      if s == 'True':
         return True
      else:
         return False
         
    if "x10.Proxy" in props:
      self.x10[0] = props["x10.Proxy"].split("Net:default -h ")[1].split(" -p")[0]
      self.x10[1] = props["x10.Proxy"].split(" -p")[1]
      
      try:
        base = ic.stringToProxy('Net:default -h '+self.x10[0]+' -p ' + self.x10[1])
        self.net = x10.NetPrx.checkedCast(base)
        self.Modus = self.assingmod(self.parseMod(self.net.getEnvironment()))
      except:
        print "Connection Failed"
        
    for i in range(1,17):
      if "x10.Module.A" + str(i) + ".name" in props:
        if self.net.isCode("A"+str(i)) == False:
          if props["x10.Module.A" + str(i) + ".type"] == "Lamp":
            mod = Mod(props["x10.Module.A" + str(i) + ".name"], "A" + str(i) , props["x10.Module.A" + str(i) + ".type"], str_to_bool(props["x10.Module.A" + str(i) + ".active"]))
            mod.setcfgAlarm(int(props["x10.Module.A" + str(i) + ".alarm_start"][0:2]),int(props["x10.Module.A" + str(i) + ".alarm_start"][3:5]),
                            int(props["x10.Module.A" + str(i) + ".alarm_end"][0:2]),int(props["x10.Module.A" + str(i) + ".alarm_end"][3:5]), 
                            str_to_bool(props["x10.Module.A" + str(i) + ".alarm_act"]))        
            self.Modus.append(mod)
            self.net.addModule(mod.name, mod.code, mod.mtype)
          else:
  
            mod = Mod(props["x10.Module.A" + str(i) + ".name"], "A" + str(i) , props["x10.Module.A" + str(i) + ".type"], str_to_bool(props["x10.Module.A" + str(i) + ".active"]))
            #if "x10.Module.A" + str(i) + ".rules" in props:
            #  mod.setRules()
            self.Modus.append(mod)
            self.net.addModule(mod.name, mod.code, mod.mtype)

            
     
        

if __name__ == "__main__":
  settings = Gtk.Settings.get_default()
  settings.props.gtk_button_images = True
  #GObject.threads_init()
  threads =True
  
  ic = Ice.initialize(sys.argv)
  
  if (sys.argv):
    propsx10 = ic.getProperties().getPropertiesForPrefix("x10")
    propscam = ic.getProperties().getPropertiesForPrefix("cam")
    GUI = viewGUI(propsx10, propscam)
  else:
    GUI = viewGUI()
    
  GLib.threads_init()
  Gdk.threads_init()
  Gdk.threads_enter()
  Gtk.main()
  Gdk.threads_leave()
    
  threads =False
    
         
    
  
  sys.exit()

