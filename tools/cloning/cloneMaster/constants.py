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


dnsmasq = "blues0"

hostSystemUpdateDisable = 0
hostSystemUpdateScheduled = 1
hostSystemUpdatePending = 2
hostSystemUpdateRunning = 3
hostSystemUpdateFail = 4
hostSystemUpdateHung = 5
hostSystemUpdateKilled = 6
hostSystemUpdateDone = 7


restartImmidiate = 0
restartNextTime = 1

cloneTypeDisable = 0
cloneTypeLinux = 1
cloneTypeLinuxWin = 2
cloneType = {
  0 : False,
  1 : "linux",
  2 : "linuxWin",
}

cloneDisable = 0
cloneClone = 1
cloneGrubUpdate = 2
cloneNetboot = 3

clone = {
  0 : False,
  1 : "clone",
  2 : "grubUpdate",
  3 : "netboot"
}


cloneStatusDisable = 0
cloneStatusInitiate = 1
cloneStatusPending = 2
cloneStatusRunning = 3
cloneStatusDone = 4
cloneStatusFail = 5


#task table
taskWaiting = 0
taskPending = 1
taskActive = 2
taskStopped = 3
taskAutoStopped = 5
taskDone = 4

#task table assign hack
fastAssignEnable = 1
fastAssignDisable = 0

afterTaskSloppyEnable = 1
afterTaskSloppyDisable = 0


# batching 
batchActive = 1
batchDeactive = 0

batchStatus = {
  1 : "active",
  0 : "deactive",
  "active" : 1,
  "deactive" : 0
}

taskStatus = {
  0 : "waiting",
  1 : "pending",
  2 : "active",
  3 : "stopped",
  4 : "done",
  5 : "autoStopped"
}


#frames table
framesUnassigned = 0
framesAssigned = 1
framesPending = 2
framesRunning = 3
framesDone = 4
framesFailed = 5
framesHold = 6
framesAutoHold = 7
framesKilled = 9
framesHung = 10
framesBatched = 11


framesStatus = {
  0 : "unassigned",
  1 : "assigned",
  2 : "pending",
  3 : "running",
  4 : "done",
  5 : "failed",
  6 : "hold",
  7 : "autoHold",
  9 : "killed",
  10 : "hung",
  11 : "batched"
}

#hostInfo table
hostInfoDisable = 0
hostInfoEnable = 1

hostInfoStatus = {
  0 : "disabled",
  1 : "enabled"
}

#hostAlive table
hostAliveDead = 0
hostAliveAlive = 1

hostAliveStatus = {
  0 : "dead", 
  1 : "alive"
}
  

#hostResource
hostResourceActive = 1
hostResourceStopped = 2
hostResourceForcedOff = 3


clientSingularityPort  = 6662
clientListenPort = 6660
clientCtrlListenPort = 6661
serverDNSDHCPPort = 6663

#proj table
projActive = 1
projDeactive = 0

