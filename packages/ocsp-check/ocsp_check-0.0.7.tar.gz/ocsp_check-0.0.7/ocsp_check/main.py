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
    if len(sys.argv) == 4:

        if sys.argv[2] == "-f" or sys.argv[2] == "--file":
            print("Feature Not Yet Implemented")

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
    CACertificateURL = getCAIssuer(certificate)

    CACertificateData = requests.get(CACertificateURL)

    try:
        CACertificate = x509.load_pem_x509_certificate(CACertificateData.content, default_backend())
    except ValueError:
        try:
            CACertificate = x509.load_der_x509_certificate(CACertificateData.content, default_backend())
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

def crtsh(crtshId):

    base64Certificate = requests.get('https://crt.sh/?d=' + crtshId)
    certificate = x509.load_pem_x509_certificate(base64Certificate.content, default_backend())

    prepareOCSPRequest(certificate)


def help():
    print("ocsp_check")
    print("Usage Syntax: ocsp_check --POST/--GET -c/-d/-f target"
          "\n\n"
          "Method Parameters: \n"
          "     --POST / -p      Perform the OCSP request using an HTTP POST call\n"
          "     --GET / -g      Perform the OCSP request using an HTTP GET call\n"
          "\n\n"
          "Source Parameters: \n"
          "     -c      Use a crt.sh ID as target\n"
          "     -d      Use a domain / live website as target\n"
          "     -f      Use a local file containing a certificate as target\n"
          "\n\n"
          "Target Parameter: In place of target should be a crt.sh ID, domain/website (including https://) or local filename\n"
          "\n\n"
          "ocsp_check version 0.0.7\n"
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
            print("ERROR: No OCSP Server URL found in certificate. Quitting.")
            exit(-1)
        else:
             return CACertificate


    except ExtensionNotFound:
        raise ValueError("Certificate AIA Extension Missing. Possible Root Certificate."
                         ) from None


def getOCSPServerURL(certificate):
    global ocsp_url

    try:
        authorityInfoAccess = certificate.extensions.get_extension_for_oid(
            ExtensionOID.AUTHORITY_INFORMATION_ACCESS).value

        for authorityInfoAccessMethod in iter((authorityInfoAccess)):
            if authorityInfoAccessMethod.__getattribute__("access_method")._name == "OCSP":
                ocsp_url = authorityInfoAccessMethod.__getattribute__("access_location").value

        if len(ocsp_url) > 6:
            return ocsp_url

        else:
            raise ValueError("No OCSP Server URL found in certificate")

    except ExtensionNotFound:
        raise ValueError("Certificate AIA Extension Missing. Possible Root Certificate."
                         ) from None


def incorrectSyntax():
    print("Incorrect Syntax. Please see 'ocsp_check -h' for usage and help")

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
