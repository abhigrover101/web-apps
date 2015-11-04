SET DLPATH="C:\Program Files\salesforce.com\Data Loader"
SET DLCONF="C:\Program Files\salesforce.com\Data Loader\cliq_process\eaccounts\config"
SET DLDATA="C:\Program Files\salesforce.com\Data Loader\cliq_process\eaccounts\write"
call %DLPATH%\Java\bin\java.exe -cp %DLPATH%\* -Dsalesforce.config.dir=%DLCONF% com.salesforce.dataloader.process.ProcessRunner process.name=eaccounts
REM To rotate your export files, uncomment the line below
REM copy %DLDATA%\eaccounts.csv %DLDATA%\%date:~10,4%%date:~7,2%%date:~4,2%-%time:~0,2%-eaccounts.csv
