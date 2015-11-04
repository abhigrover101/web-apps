SET DLPATH="C:\Program Files\salesforce.com\Data Loader"
SET DLCONF="C:\Program Files\salesforce.com\Data Loader\cliq_process\econtacts\config"
SET DLDATA="C:\Program Files\salesforce.com\Data Loader\cliq_process\econtacts\write"
call %DLPATH%\Java\bin\java.exe -cp %DLPATH%\* -Dsalesforce.config.dir=%DLCONF% com.salesforce.dataloader.process.ProcessRunner process.name=econtacts
REM To rotate your export files, uncomment the line below
REM copy %DLDATA%\econtacts.csv %DLDATA%\%date:~10,4%%date:~7,2%%date:~4,2%-%time:~0,2%-econtacts.csv
