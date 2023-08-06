# OCSP Check

Usage Syntax: ocsp_check --POST/--GET -c/-d/-f target

Method Parameters:  
    -p      Perform the OCSP request using an HTTP POST call (--POST works too)  
    -g      Perform the OCSP request using an HTTP GET call (--GET works too)  

Source Parameters:  
    -c      Use a crt.sh ID as target  
    -d      Use a domain / live website as target  
    -f      Use a local file containing a certificate as target  

Target Parameter: In place of target should be a crt.sh ID, domain/website (including https://) or local filename

ocsp_check version 0.0.14  
Author: Martijn Katerbarg