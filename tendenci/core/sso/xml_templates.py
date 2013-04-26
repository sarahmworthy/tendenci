"""
XML string templates for SAML 2.0 Service Provider AuthnRequest.
"""
SIGNED_INFO = (
    '<ds:SignedInfo xmlns:ds="http://www.w3.org/2000/09/xmldsig#">'
        '<ds:CanonicalizationMethod Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#"></ds:CanonicalizationMethod>'
        '<ds:SignatureMethod Algorithm="http://www.w3.org/2000/09/xmldsig#rsa-sha1"></ds:SignatureMethod>'
        '<ds:Reference URI="#${REFERENCE_URI}">'
            '<ds:Transforms>'
                '<ds:Transform Algorithm="http://www.w3.org/2000/09/xmldsig#enveloped-signature"></ds:Transform>'
                '<ds:Transform Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#"></ds:Transform>'
            '</ds:Transforms>'
            '<ds:DigestMethod Algorithm="http://www.w3.org/2000/09/xmldsig#sha1"></ds:DigestMethod>'
            '<ds:DigestValue>${SUBJECT_DIGEST}</ds:DigestValue>'
        '</ds:Reference>'
    '</ds:SignedInfo>'
)


SIGNATURE = (
    '<ds:Signature xmlns:ds="http://www.w3.org/2000/09/xmldsig#">'
        '${SIGNED_INFO}'
    '<ds:SignatureValue>${RSA_SIGNATURE}</ds:SignatureValue>'
    '<ds:KeyInfo>'
        '<ds:X509Data>'
            '<ds:X509Certificate>${CERTIFICATE}</ds:X509Certificate>'
        '</ds:X509Data>'
    '</ds:KeyInfo>'
'</ds:Signature>'
)


AUTHN_REQUEST = (
    '<?xml version="1.0" encoding="UTF-8"?>'
        '<samlp:AuthnRequest AssertionConsumerServiceURL="${ACS_URL}" '
                'Destination="${DESTINATION}" '
                'ID="${AUTHN_REQUEST_ID}" '
                'IssueInstant="${ISSUE_INSTANT}" '
                'ProtocolBinding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST" '
                'Version="2.0" '
                'xmlns:samlp="urn:oasis:names:tc:SAML:2.0:protocol">'
            '<saml:Issuer xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion">${ISSUER}</saml:Issuer>'
            '${AUTHN_REQUEST_SIGNATURE}'
    '</samlp:AuthnRequest>'
)
