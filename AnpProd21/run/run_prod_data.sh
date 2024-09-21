#! /bin/sh
TestArea="/home/hengli/testarea/AnpProd21/build"
IFS=$'\n' read -d '' -r -a lines < $1
iflag=1
for element in "${lines[@]}"
do 
	  if [ $iflag -eq 1 ]
		then
        flist=\'$element\'
	      iflag=0
    else flist=$flist,\'$element\'
		fi
done
athena $TestArea/../source/PhysicsAnpProd/share/PhysicsAnpProd_ReadxAODr21.py -c "inputFile=[$flist];IS_DATA=True;dumpSG=False;EvtMax=-1;mcSubCampaign='mc16a'"
