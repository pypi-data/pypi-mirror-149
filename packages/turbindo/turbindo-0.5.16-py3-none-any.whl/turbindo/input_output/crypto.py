import crypt
import string
from random import random, sample

from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.x509 import load_pem_x509_certificate

from turbindo.runtime.instrumented_object import InstrumentedIO
import datetime

from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa


class CryptographyManager(InstrumentedIO):
    def load_key(self, filename, pw: str = None):
        with open(filename, 'rb') as pem_in:
            pemlines = pem_in.read()
        private_key = load_pem_private_key(pemlines, pw.encode("UTF-8"), default_backend())
        return private_key

    def load_cert(self, filename):
        with open(filename, 'rb') as pem_in:
            pem_data = pem_in.read()
        cert = load_pem_x509_certificate(pem_data, default_backend())

        return cert

    def create_ca(self, crt_path: str,
                  key_path: str,
                  country_name: str,
                  state_name: str,
                  city_name: str,
                  org_name: str,
                  common_name: str,
                  ca_key_pw: str = None,
                  size=2048,
                  exponent=65537,
                  days_valid=3650):
        root_key = rsa.generate_private_key(
            public_exponent=exponent,
            key_size=size,
            backend=default_backend()
        )
        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, country_name),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, state_name),
            x509.NameAttribute(NameOID.LOCALITY_NAME, city_name),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, org_name),
            x509.NameAttribute(NameOID.COMMON_NAME, common_name),
        ])
        root_cert = x509.CertificateBuilder().subject_name(
            subject
        ).issuer_name(
            issuer
        ).public_key(
            root_key.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.datetime.utcnow()
        ).not_valid_after(
            datetime.datetime.utcnow() + datetime.timedelta(days=days_valid)
        ).sign(root_key, hashes.SHA256(), default_backend())

        with open(key_path, "wb") as f:
            if ca_key_pw is None:
                ea = serialization.NoEncryption()
            else:
                ea = serialization.BestAvailableEncryption(ca_key_pw.encode("UTF-8"))
            f.write(root_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=ea
            ))

        with open(crt_path, "wb") as f:
            f.write(root_cert.public_bytes(
                encoding=serialization.Encoding.PEM,
            ))

    def issue_cert(self,
                   issue_crt_path: str,
                   issue_key_path: str,
                   ca_crt_path: str,
                   ca_key_path: str,
                   country_name: str,
                   state_name: str,
                   city_name: str,
                   org_name: str,
                   dns_name: str,
                   issue_key_pw=None,
                   ca_key_pw=None,
                   size=2048,
                   exponent=65537,
                   days_valid=365):
        ca_crt = self.load_cert(ca_crt_path)
        ca_key = self.load_key(ca_key_path, pw=ca_key_pw)
        issue_key = rsa.generate_private_key(
            public_exponent=exponent,
            key_size=size,
            backend=default_backend()
        )
        new_subject = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, country_name),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, state_name),
            x509.NameAttribute(NameOID.LOCALITY_NAME, city_name),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, org_name),
        ])
        issue_cert = x509.CertificateBuilder().subject_name(
            new_subject
        ).issuer_name(
            ca_crt.issuer
        ).public_key(
            issue_key.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.datetime.utcnow()
        ).not_valid_after(
            datetime.datetime.utcnow() + datetime.timedelta(days=days_valid)
        ).add_extension(
            x509.SubjectAlternativeName([x509.DNSName(dns_name)]),
            critical=False,
        ).sign(ca_key, hashes.SHA256(), default_backend())

        with open(issue_key_path, "wb") as f:
            if issue_key_pw is None:
                ea = serialization.NoEncryption()
            else:
                ea = serialization.BestAvailableEncryption(issue_key_pw.encode("UTF-8"))
            f.write(issue_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=ea
            ))

        with open(issue_crt_path, "wb") as f:
            f.write(issue_cert.public_bytes(
                encoding=serialization.Encoding.PEM,
            ))

    def gen_ssh_keypair(self, name, path, pw=None):
        pass

    def shadow_hash(self, password):
        result = crypt.crypt(password, crypt.mksalt(crypt.METHOD_SHA512))
        return result
