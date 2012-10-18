

#!/usr/bin/python
###
# Copyright (C) 2012  Shrinidhi Rao shrinidhi@clickbeetle.in
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
###

# SERVER!!!!!!!!
import sys
import os
import logging
import time
import signal
import setproctitle
import tempfile
import rbhus.dbRbhus as dbRbhus
import rbhus.constants as constants
import psi
import psi.process
import multiprocessing

LOG_FILENAME = '/var/log/rbhusQueen_scheduler.log'
logging.BASIC_FORMAT = "%(asctime)s - %(funcName)s - %(levelname)s - %(message)s"
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)

db_conn = dbRbhus.dbRbhus()
tempDir = tempfile.gettempdir()
mainPidFile = tempDir + os.sep +"rbusServer.pids"

setproctitle.setproctitle("initTasks")

def getWaitingTasks(pendingTasks):
  setproctitle.setproctitle("get")
  while(1):
    rows = 0
    #logging.error("ROWS WTF2 : "+ str(rows))
    try:
      rows = db_conn.execute("SELECT * FROM tasks WHERE status="+ str(constants.taskWaiting), dictionary=True)
    except:
      logging.error("Screwed selecting waiting tasks : "+ str(sys.exc_info()))
      time.sleep(1)
      continue
    #logging.error("ROWS WTF3 : "+ str(rows))
    if(rows):
      for row in rows:
        if(row):
          pendingTasks.put(row)
          idTask = row['id']
          #logging.debug("Adding task wtf: "+ str(row))
          ##DO NOT REMOVE THE PENDING STATUS
          while(1):
            try:  
              db_conn.execute("UPDATE tasks SET status="+ str(constants.taskPending) +" WHERE (id = "+ str(idTask) +") and ( status = "+ str(constants.taskWaiting) +")")
              #logging.debug("updating tasks table with pending status wtf4")
              break
            except:
              logging.error("Screwed updating tasks table with pending status : "+ str(sys.exc_info()))
              continue
            time.sleep(0.1)
            
          try:
            db_conn.execute("INSERT INTO tasksLog (id) VALUES ("+ str(idTask) +")")
          except:
            logging.error("Screwed inserting into tasklog : "+ str(sys.exc_info()))
          #time.sleep(0.1)
    time.sleep(1)


def initWaitingTasks(pendingTasks):
  setproctitle.setproctitle("set")
  while(1):
    row = {}
    while(1):
      try:
        row = pendingTasks.get(False)
        break
      except:
        #logging.error("Screwed initWaitingTasks WTF1 : "+ str(sys.exc_info()))
        time.sleep(0.2)
    if(row):  
      idTask = row['id']
      fRange = row['fRange']
      frames = []
      
      for a in fRange.split(","):
        frange = a.split(":")
        pad = 1
        Frange = frange[0]
        if(len(frange) == 2):
          pad = frange[1]
        logging.debug("PAD : "+ str(pad))
        logging.debug(str(int(Frange.split("-")[0])))
        logging.debug(str(int(Frange.split("-")[-1]) + 1))
        for b in range(int(Frange.split("-")[0]), int(Frange.split("-")[-1]) + 1, int(pad)):
          frames.append(b)
          
      tFrames = []
      framesTable = 0
      while(1):
        try:
          framesTable = db_conn.getAllFrames(idTask)
          break
        except:
          pass
        time.sleep(0.5)
        
      if(framesTable):
        for frameTable in framesTable:
          tFrames.append(frameTable['frameId'])
      
      tFramesSet = set(tFrames)
      framesSet = set(frames)
      forDelSet = tFramesSet.difference(framesSet)
      for forDel in forDelSet:
        while(1):
          try:
            db_conn.execute("DELETE FROM frames WHERE frames.id="+ str(idTask) +" AND frameId="+ str(forDel))
            break
          except:
            logging.error("Screwed initWaitingTasks (Delete frames table (connection)) : "+ str(sys.exc_info()))
          time.sleep(0.1)
    
      for frame in frames:
        while(1):
          try:
            db_conn.execute("INSERT INTO frames (id, frameId) VALUES ("+ str(idTask) +", "+ str(frame) +")")
            break
          except:
            logging.error("Screwed initWaitingTasks (Insert frames table (connection)) : "+ str(idTask) +" : "+ str(sys.exc_info()))
            if(str(sys.exc_info()).find("IntegrityError") >= 0):
              break
          time.sleep(0.1)

      logging.debug("Initialized frames table")
      while(1):
        try:
          db_conn.execute("UPDATE tasks SET status="+ str(constants.taskActive) +" WHERE id="+ str(idTask))
          logging.debug("Updated task:"+ str(idTask) +" status to 2(active)")
          break
        except:
          logging.error("Screwed initWaitingTasks : "+ str(sys.exc_info()))
        time.sleep(0.1)
    time.sleep(0.1)
    
    
def initTasks():
  pendTasks = multiprocessing.Queue()
  
  getWaitingTasks_proc = multiprocessing.Process(target=getWaitingTasks,args=(pendTasks,))
  p.append(getWaitingTasks_proc)
  getWaitingTasks_proc.start()
  
  
  time.sleep(2)
  
  
  initWaitingTasks_proc = multiprocessing.Process(target=initWaitingTasks,args=(pendTasks,))
  p.append(initWaitingTasks_proc)
  initWaitingTasks_proc.start()
  
  pendTasks.close()
  
  pendTasks.join_thread()
  
  while(1):
    time.sleep(1)
    if(not p):
      break
    for i in range(0,len(p)):
      if(p[i].is_alive()):
        time.sleep(0.5)
      else: 
        logging.debug("MAIN Process dead : "+ str(p[i].pid))
        try:
          del(p[i])
        except:
          logging.debug("MAIN Process dead . cannot delete index")
        break