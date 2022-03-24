


#Invoke-Expression "python -m pip install --upgrade pip setuptools virtualenv"

#Invoke-Expression "pip install kivy[full] "
#Invoke-Expression "python -m pip install sounddevice"
#Invoke-Expression "python -m pip install numpy"
#Invoke-Expression "python -m virtualenv kivy_venv"


kivy_venv\Scripts\activate

$commonRoot = [String]$PSScriptRoot 

#get path of kivy's python
$run = $commonRoot + "\kivy_venv\Scripts\python.exe "

#run tuner.py file using kivy's python
$tunerMain = $commonRoot + "\tuner.py"

$runStatement = $run + $tunerMain

Invoke-Expression $runStatement

exit 0
