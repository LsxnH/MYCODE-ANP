#
# Latest releases:
#   https://twiki.cern.ch/twiki/bin/view/AtlasProtected/AnalysisRelease
#

myrelease=2.4.43

export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
source $ATLAS_LOCAL_ROOT_BASE/user/atlasLocalSetup.sh
source $AtlasSetup/scripts/asetup.sh AthAnalysisBase,${myrelease},here

echo "---------------------------------------------------------------"
echo "Using AthAnalysisBase ${myrelease}"
