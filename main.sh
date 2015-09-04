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

# # sed the original script
# sed -i 's/^\([ \t]*\)lines = getProv.*/\1lines = \"Processing History:\\n asdf \(c186b1d0b14a7353cd3d6e46639ccbbc\)\"/g' CMSRunAnalysis.py

# # sed the script which is inside the tar in case it overwrites the original script
# tarfile="CMSRunAnalysis.tar.gz"
# rm -rf blah
# mkdir blah
# tar xvzmf $tarfile -C blah
# sed -i 's/^\([ \t]*\)lines = getProv.*/\1lines = \"Processing History:\\n asdf \(c186b1d0b14a7353cd3d6e46639ccbbc\)\"/g' blah/CMSRunAnalysis.py
# cd blah
# tar cvzf new.tar.gz *
# cd ..
# mv blah/new.tar.gz $tarfile
# rm -rf blah

cmsRun -j FrameworkJobReport.xml -p PSet.py

linenum=$((jobnum))
# linenum=$((jobnum + 1)) # FIXME. when doing --dryrun, need + 1 since it counts starting with 0

filepath=$(sed -n "${linenum}p" < $filelist)
echo $filepath


# sed -i 's/^\([ \t]*\)lines = getProv.*/\1lines = \"Processing History:\\n asdf \(c186b1d0b14a7353cd3d6e46639ccbbc\)\"/g' CMSRunAnalysis.py

rm output.root
xrdcp root://xrootd.unl.edu/$filepath output.root

