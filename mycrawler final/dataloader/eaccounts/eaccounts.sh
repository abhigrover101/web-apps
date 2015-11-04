#!/bin/sh
export DLPATH="C:\Program Files\salesforce.com\Data Loader"
export DLCONF="C:\Program Files\salesforce.com\Data Loader\cliq_process\eaccounts\config"
java -cp "$DLPATH/*" -Dsalesforce.config.dir=$DLCONF com.salesforce.dataloader.process.ProcessRunner process.name=eaccounts
