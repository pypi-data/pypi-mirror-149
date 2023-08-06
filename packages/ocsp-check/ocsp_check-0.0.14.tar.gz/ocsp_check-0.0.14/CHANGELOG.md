## Changelog

### 0.0.14
Actually quit if no AIA extension is found 

### 0.0.13
Proper error handling for certificates without an OCSP server

### 0.0.12 
Implemented feature to get certificate from file

### 0.0.11
Added ability to provide the issuing CA by file for cases where the Issuer CA is not provided in the certificate

### 0.0.10
Replaced No OCSP URL found with No CA Issuer found in CACertificate function

### 0.0.9
crt ID 5762896603 is missing AIA extensions. Error trapping was in place, but not correctly.

### 0.0.8
crt ID 5762896603 is missing AIA extensions. Error trapping was in place, but not correctly.

### 0.0.7
crt ID 4969192134 revealed an improper encoded DER certificate. Error trapping added 

### 0.0.6
crt ID 881434381 revealed an issue with error trapping when no CACertificate is found in the certificate

### 0.0.5
Initial Release
