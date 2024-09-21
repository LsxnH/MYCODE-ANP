#
# Latest releases:
#   https://twiki.cern.ch/twiki/bin/view/AtlasProtected/AnalysisRelease
#

myrelease=21.2.53

export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
source $ATLAS_LOCAL_ROOT_BASE/user/atlasLocalSetup.sh

if [ -e "../build" ]
then
    pushd ../build
    acmSetup AthAnalysis,$myrelease
    popd
else
    echo "Error: build directory does not exist"
fi

echo "---------------------------------------------------------------"
echo "Using AthAnalysisBase ${myrelease}"
echo "MAKEFLAGS=$MAKEFLAGS"
