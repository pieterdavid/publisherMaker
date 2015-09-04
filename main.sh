#!/bin/bash

jobnum=$1
filelist="filelist.txt"
echo "This is job number $jobnum"
echo "hostname"
hostname
echo "ls"
ls -l
echo "pwd"
pwd

cmsRun -j FrameworkJobReport.xml -p PSet.py

linenum=$((jobnum))

filepath=$(sed -n "${linenum}p" < $filelist)
echo $filepath

rm output.root
xrdcp root://xrootd.unl.edu/$filepath output.root

