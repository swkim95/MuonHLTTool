#!/usr/bin/env python
import subprocess
import os
import sys
import gc

if __name__ == '__main__':

  crabDirBase = sys.argv[1]
  # proxy = '"/tmp/x509up_u556950669"'
  # proxy = '"/tmp/x509up_u41056"'
  proxy = '"/tmp/x509up_u139254"'

  verbos = True
  if 'verbos' in sys.argv:
    verbos = True

  resubmit = True
  if 'resubmit' in sys.argv:
    resubmit = True

  hadd = False
  if 'hadd' in sys.argv:
    hadd = True

  report = False
  if 'report' in sys.argv:
    report = True

  killall = False
  if 'kill' in sys.argv:
    killall = True

  FileList = os.listdir("./%s" % crabDirBase)
  List_CRABDir = []

  if verbos:
    print "available crabDir list: "
  for filename in FileList:
    if "crab_" in filename and os.path.isdir( crabDirBase+'/'+filename ):
      if verbos:
        print "'"+filename+"',"
      List_CRABDir.append( filename )

  CRABDirs = List_CRABDir # -- all crab directories in crabDirBase -- #
  CRABDirs.sort()

  print '\n'
  print '# of CRAB dirs : ', len(CRABDirs)

  FailedList = []
  RunningList = []
  SubmitFailedList = []
  CompletedList = []
  UnknownList = []
  OthersList = []
  HaddList = []

  Pending60 = []
  Pending80 = []

  sys.stdout.flush()
  gc.collect()

  for crabDir in CRABDirs:
    crabDirPath = "%s/%s" % (crabDirBase, crabDir)

    if killall:
      killcmd = 'crab kill -d '+crabDirPath+ ' --proxy='+proxy
      print '\n', killcmd
      sys.stdout.flush()
      gc.collect()
      os.system(killcmd)
      sys.stdout.flush()
      gc.collect()
      continue

    if report:
      reportcmd = 'crab report -d '+crabDirPath+' --outputdir=crab_Report/'+crabDir+' --proxy='+proxy
      print '\n', reportcmd
      sys.stdout.flush()
      gc.collect()
      os.system(reportcmd)
      sys.stdout.flush()
      gc.collect()
      continue

    cmd = 'crab status "'+crabDirPath+'" --proxy='+proxy
    result = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    (stdout, stderr) = result.communicate()

    fIdle = 0.
    fUnsu = 0.
    nJobs = 'NotYet'
    task_date = 'None'
    print_status = False
    for line in stdout.splitlines():
      if 'idle' in line and 'run and stay idle forever' not in line:
        fIdle = float( (line.split('idle'))[1].split('%')[0] )
      if 'unsubmitted' in line:
        fUnsu = float( (line.split('unsubmitted'))[1].split('%')[0] )
      if 'finished' in line:
        nJobs = (line.split('/'))[1].split(')')[0]
      if 'Task name:' in line:
        task_date = ((line.split(':'))[1])
    nJobs = nJobs.replace(' ','').replace('\t','').replace('\n','')
    task_date = task_date.replace(' ','').replace('\t','').replace('\n','')

    print '\n' + ( '-' * 50 )

    print 'Name:' + crabDir
    print 'task:' + task_date
    if nJobs == 'NotYet':
      print 'No finished jobs yet...'
    else:
      print 'nJobs='+nJobs

    for line in stdout.splitlines():
      print line
      # if 'Warning:' in line:
      #   print line
      # if ("Status on the scheduler" in line):
      #   print_status = True
      # if ("No publication information available yet" in line):
      #   print_status = False
      # if ("Summary of run jobs" in line):
      #   print_status = False
      # if print_status:
      #   print line

    if (fIdle + fUnsu) > 1000:
      print 'Pending jobs: forever'
    else:
      print 'Pending jobs: %d' % (fIdle + fUnsu)

    sys.stdout.flush()
    gc.collect()

    if (fIdle + fUnsu) > 60.:
      Pending60.append( crabDir )
      Pending80.append( crabDir )

    elif (fIdle + fUnsu) > 80.:
      Pending80.append( crabDir )

    if "COMPLETED" in stdout:
      print "\t COMPLETED in crab status"
      CompletedList.append( crabDir )

    # if verbos:
    #   print stdout

    elif "SUBMITFAILED" in stdout:
      print "SUBMITFAILED"
      SubmitFailedList.append( crabDir )

    elif "failed   " in stdout or "failed\t" in stdout or "FAILED" in stdout:
      FailedList.append( crabDir )
      # print stdout

    elif "running" in stdout:
      RunningList.append( crabDir )

    # elif "COMPLETED" in stdout:
    #   if nJobs != checkstdout:
    #     print "WARNING : nJobs != nTran"

    elif "UNKNOWN" in stdout:
      UnknownList.append( crabDir )

    else:
      OthersList.append( crabDir )

    sys.stdout.flush()
    gc.collect()

  print "\n\n#--SUMMARY --#"

  print "\n[Pending > 60\%]"
  for one in Pending60:
    print one

  print "\n[Pending > 80\%]"
  for one in Pending80:
    print one

  print "\n[Completed list]"
  for one in CompletedList:
    print one

  sys.stdout.flush()
  gc.collect()

  if len(FailedList) > 0:
    print "\n[Failed list]"
    for one in FailedList:
      print one
      if resubmit:
        sys.stdout.flush()
        gc.collect()
        resubmitcmd = 'crab resubmit -d '+crabDirBase+'/'+one+' --proxy='+proxy+' --maxjobruntime=2750'
        os.system(resubmitcmd)
        sys.stdout.flush()
        gc.collect()

  if len(RunningList) > 0:
    print "\n[Running list]"
    for one in RunningList:
      print one

  if len(SubmitFailedList) > 0:
    print "\n[SubmitFailed list]"
    for one in SubmitFailedList:
      print one

  if len(UnknownList) > 0:
    print "\n[Unknown list]"
    for one in UnknownList:
      print one

  if len(OthersList) > 0:
    print "\n[Others]"
    for one in OthersList:
      print one

  sys.stdout.flush()
  gc.collect()
