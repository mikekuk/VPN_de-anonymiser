
@echo off
setlocal enableextensions

REM Check if the script is running as administrator
NET FILE >NUL 2>&1
if '%errorlevel%' == '0' (goto START) else (goto UAC)

:UAC
REM Prompt the user to run the script as administrator
echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
echo UAC.ShellExecute "%~s0", "", "", "runas", 1 >> "%temp%\getadmin.vbs"
"%temp%\getadmin.vbs"
del "%temp%\getadmin.vbs"
exit /B

@echo off
setlocal enableextensions

REM Check if the script is running as administrator
NET FILE >NUL 2>&1
if '%errorlevel%' == '0' (goto START) else (goto UAC)

:UAC
REM Prompt the user to run the script as administrator
echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
echo UAC.ShellExecute "%~s0", "", "", "runas", 1 >> "%temp%\getadmin.vbs"
"%temp%\getadmin.vbs"
del "%temp%\getadmin.vbs"
exit /B

:START
REM Check if an argument was provided
if "%~1" == "" (
  echo Usage: %0 output_file_name
  exit /B
)

REM Run tshark with the specified arguments
"C:\Program Files\Wireshark\tshark.exe" -i 4 -s 128 -a duration:20 -w "C:\Users\Administrator\Documents\pcaps\%~1.pcap" host 154.16.196.216
aws s3 cp "C:\Users\Administrator\Documents\pcaps\%~1.pcap" s3://pcaps-for-wfa 
del "C:\Users\Administrator\Documents\pcaps\%~1.pcap" & exit

:end
