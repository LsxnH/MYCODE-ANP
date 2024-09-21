#! /bin/sh
#       --ZjetsOR \
#       --ZjetsORreverse \
#       --doSherpa \
#       --do-prompt-sr \
#       --do-fake-cr \
TestArea="/home/hengli/testarea/AnpWH/build"
IFS=$'\n' read -d '' -r -a lines < $1
python $TestArea/../source/PhysicsAnpWH/macros/runWH.py \
       "${lines[@]}" \
       --ZjetsOR \
       --do-fake-cr \
       -o WH_HIST.root
