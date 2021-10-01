#!/bin/bash

packagename="deploymentpackage.zip"
venvname="deploymentvirtualenv"
echo "Creating Virtual Environment"
python3 -m venv --clear ${venvname}
echo "Virtual Environment created"
echo "Downloading dependencies"
source "./${venvname}/bin/activate"
pip install -r requirements.txt
deactivate
echo "Dependencies downloaded"
echo "Creating zip file"
cd "${venvname}/lib/python3.6/site-packages"
rm -f "${OLDPWD}/${packagename}"
zip -r9 "${OLDPWD}/${packagename}" . 
cd ${OLDPWD}
zip -g $packagename requirements.txt
zip -g $packagename lambda_function.py
rm -Rf "./$venvname"
echo "Finished"