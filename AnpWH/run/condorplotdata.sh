#! /bin/sh
TestArea="/home/hengli/testarea/AnpWH/build"
IFS=$'\n' read -d '' -r -a lines < $1
python $TestArea/../source/PhysicsAnpWH/macros/runWH.py \
       "${lines[@]}" \
			 -o WH_HIST_data.root
