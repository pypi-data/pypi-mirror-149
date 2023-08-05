import sys
import urllib.parse
import requests
import subprocess
import base64
from cryptography import x509
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.hashes import SHA256, SHA1
from cryptography.x509 import ExtensionNotFound, ocsp
from cryptography.x509.oid import ExtensionOID
from cryptography.hazmat.backends import default_backend


def main():
    if len(sys.argv) >= 4:

        if sys.argv[2] == "-f" or sys.argv[2] == "--file":
            fromFile(sys.argv[3])

        elif sys.argv[2] == "-d" or sys.argv[2] == "--domain":
            print("Feature Not Yet Implemented")

        elif sys.argv[2] == "-c" or sys.argv[2] == "--crtsh":
            crtsh(sys.argv[3])

        else:
            print(incorrectSyntax())
            print()
            help()

    elif len(sys.argv) == 2:
        if sys.argv[1] == "-h":
            help()

        else:
            print(incorrectSyntax())
            print()
            help()

    elif len(sys.argv) == 1:
        help()

    else:
        print(incorrectSyntax())
        print()
        help()


def getOCSPResponse(OCSPResponse):
    OCSPResp = ocsp.load_der_ocsp_response(OCSPResponse)
    print(OCSPResp.response_status)



def sendOCSPRequestPOST(base64Request, ocspUrl):

    OCSPPostRequest = requests.post(
        ocspUrl,
        data=base64Request,
        headers={"Content-Type": "application/ocsp-request"},
    )

    getOCSPResponse(OCSPPostRequest.content)


def sendOCSPRequestGET(base64Request, ocspUrl):

    OCSPPostRequest = requests.get(
        ocspUrl + "/" + urllib.parse.quote(base64Request),

        headers={"Content-Type": "application/ocsp-request"},
    )

    getOCSPResponse(OCSPPostRequest.content)


def prepareOCSPRequest(certificate):
    ocspUrl = getOCSPServerURL(certificate)

    if len(sys.argv) > 4:
        if(sys.argv[4] == "-if"):
            CACertificateFile = open(sys.argv[5], 'rb')
            CACertificateData = CACertificateFile.read()

        else:
            print("ERROR: Invalid argument (" + sys.argv[4] + ")")
            exit(-1)

    else:
        CACertificateURL = getCAIssuer(certificate)

        CACertificateData = requests.get(CACertificateURL).content

    try:
        CACertificate = x509.load_pem_x509_certificate(CACertificateData, default_backend())
    except ValueError:
        try:
            CACertificate = x509.load_der_x509_certificate(CACertificateData, default_backend())
        except ValueError:
            print("ERROR: Unable to decode certificate as PEM or DER encoded certificate. Quitting.")
            exit(-1)

    ocspRequest = ocsp.OCSPRequestBuilder()
    ocspRequest = ocspRequest.add_certificate(certificate, CACertificate, SHA1())

    req = ocspRequest.build()

    base64Request = base64.b64encode(req.public_bytes(serialization.Encoding.DER))

    if(sys.argv[1] == "-p" or sys.argv[1] == "--POST" or sys.argv[1] == "--post"):
        sendOCSPRequestPOST(req.public_bytes(serialization.Encoding.DER), ocspUrl)
    elif(sys.argv[1] == "-g" or sys.argv[1] == "--GET" or sys.argv[1] == "--get"):
        sendOCSPRequestGET(base64Request.decode(), ocspUrl)


def fromFile(fileName):

    base64CertificateFile = open(fileName, 'rb')
    base64Certificate = base64CertificateFile.read()
    certificate = x509.load_pem_x509_certificate(base64Certificate, default_backend())

    prepareOCSPRequest(certificate)


def crtsh(crtshId):

    base64Certificate = requests.get('https://crt.sh/?d=' + crtshId)
    certificate = x509.load_pem_x509_certificate(base64Certificate.content, default_backend())

    prepareOCSPRequest(certificate)


def help():
    print("ocsp_check")
    print("Usage Syntax: ocsp_check --POST/--GET -c/-d/-f target [-if issuer.pem]" 
          "\n\n"
          "Method Parameters: \n"
          "     --POST / -p      Perform the OCSP request using an HTTP POST call\n"
          "     --GET / -g      Perform the OCSP request using an HTTP GET call\n"
          "\n"
          "Source Parameters: \n"
          "     -c      Use a crt.sh ID as target\n"
          "     -d      Use a domain / live website as target\n"
          "     -f      Use a local file containing a certificate as target\n"
          "\n"
          "Target Parameter: In place of target should be a crt.sh ID, domain/website (including https://) or local filename\n"
          "\n"
          "Optional -if issuer.pem Parameter: Use a local file to indicate the issuing CA instead of finding it in the certificate\n"
          "\n"
          "ocsp_check version 0.0.13\n"
          "Author: Martijn Katerbarg")


def getCAIssuer(certificate):

    CACertificate = None
    try:
        authorityInfoAccess = certificate.extensions.get_extension_for_oid(
            ExtensionOID.AUTHORITY_INFORMATION_ACCESS).value

        for authorityInfoAccessMethod in iter((authorityInfoAccess)):
            if authorityInfoAccessMethod.__getattribute__("access_method")._name == "caIssuers":
                CACertificate = authorityInfoAccessMethod.__getattribute__("access_location").value

        if CACertificate is None:
            print("ERROR: No CA Issuer URL found in certificate. Quitting.")
            exit(-1)
        else:
             return CACertificate

    except ExtensionNotFound:
        print("ERROR: Certificate AIA Extension Missing. Possible Root Certificate.")


def getOCSPServerURL(certificate):

    ocspUrl = None

    try:
        authorityInfoAccess = certificate.extensions.get_extension_for_oid(
            ExtensionOID.AUTHORITY_INFORMATION_ACCESS).value

        for authorityInfoAccessMethod in iter((authorityInfoAccess)):
            if authorityInfoAccessMethod.__getattribute__("access_method")._name == "OCSP":
                ocspUrl = authorityInfoAccessMethod.__getattribute__("access_location").value

        if ocspUrl is None:
            print("ERROR: No OCSP Server URL found in certificate. Quitting.")
            exit(-1)

        else:
            return ocspUrl

    except ExtensionNotFound:
        print("ERROR: Certificate AIA Extension Missing. Possible Root Certificate.")


def incorrectSyntax():
    print("Incorrect Syntax. Please see 'ocsp_check -h' for usage and help")

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
