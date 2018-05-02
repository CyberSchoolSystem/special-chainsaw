option explicit
DIM strComputer,strProcess

strComputer = "." ' local computer
strProcess = "chrome.exe"

' Check if Calculator is running on specified computer (. = local computer)
do
if not isProcessRunning(strComputer,strProcess) then

	Dim objShell
	Set objShell = WScript.CreateObject( "WScript.Shell" )
	objShell.Run("C:\Users\henning.klatt\AppData\Local\Google\Chrome\Application\chrome.exe 10.1.10.62:3000 --kiosk")
	Set objShell = Nothing
end if
loop

' Function to check if a process is running
function isProcessRunning(byval strComputer,byval strProcessName)

	Dim objWMIService, strWMIQuery

	strWMIQuery = "Select * from Win32_Process where name like '" & strProcessName & "'"
	
	Set objWMIService = GetObject("winmgmts:" _
		& "{impersonationLevel=impersonate}!\\" _ 
			& strComputer & "\root\cimv2") 


	if objWMIService.ExecQuery(strWMIQuery).Count > 0 then
		isProcessRunning = true
	else
		isProcessRunning = false
	end if

end function

