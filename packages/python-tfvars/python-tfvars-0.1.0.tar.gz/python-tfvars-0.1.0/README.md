# python-tfvars  
  
read secrets from terraform tfvars  
  
This module will read variables from [terraform tfvars files](https://www.terraform.io/language/values/variables#variable-definitions-tfvars-files) 
to facilitate the usage of python scripts from terraform resources.

Currently we do not support json format.  
  
## basic usage  
  
Assuming a terraform.tfvars file as follows:   
```
token = "some_token"
```
  
in your python script:
```
import tfvars

tfv = tfvars.LoadSecrets()
print(tfv["token"])
```  
  
optionally specify a file location:  
```
tfv = tfvars.LoadSecrets("../dev.auto.tfvars")
```

