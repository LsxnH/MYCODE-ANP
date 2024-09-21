#! /bin/sh
#       --ZjetsOR \
#       --ZjetsORreverse \
#       --doSherpa \
#       --do-fake-cr \
#       --do-prompt-sr \
TestArea="/home/hengli/testarea/AnpWH/build"
IFS=$'\n' read -d '' -r -a lines < $1
python $TestArea/../source/PhysicsAnpWH/macros/runWH.py \
       "${lines[@]}" \
       --do-fake-cr \
       -o WH_HIST.root
