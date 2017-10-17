from urlparse import urljoin
from os import path
from saml2 import saml
import saml2

from common_settings import *


def get_saml_config(ROOT_URL, BASEDIR):
    """
    Build pysaml2 configuration options for a SAML service provider. See pysaml2 configuration docs for more
    information: http://pysaml2.readthedocs.io/en/stable/howto/config.html.

    :param ROOT_URL: Fully qualified root url, e.g. http://sp1.localhost or http://sp1.localhost:8000
    :param BASEDIR: Base directory of the Django project
    :return: pysaml2 configuration options
    """
    return {
        # full path to the xmlsec1 binary programm
        # 'xmlsec_binary': '/usr/bin/xmlsec1',
        'xmlsec_binary': '/usr/local/bin/xmlsec1',

        # your entity id, usually your subdomain plus the url to the metadata view
        'entityid': urljoin(ROOT_URL, "/saml2/metadata/"),

        # directory with attribute mapping
        'attribute_map_dir': path.join(BASEDIR, ATTRIB_MAP_DIR_PATH),

        # this block states what services we provide
        'service': {
            # we are just a lonely SP
            'sp': {
                # fixme!
                'allow_unsolicited': True,

                "logout_requests_signed": "true",
                "authn_requests_signed": "true",
                'name': 'Federated Django sample SP',
                'name_id_format': saml.NAMEID_FORMAT_TRANSIENT,
                'endpoints': {
                    # url and binding to the assetion consumer service view
                    # do not change the binding or service name
                    'assertion_consumer_service': [
                        (urljoin(ROOT_URL, "/saml2/acs/"),
                         saml2.BINDING_HTTP_POST),
                    ],
                    # url and binding to the single logout service view
                    # do not change the binding or service name
                    'single_logout_service': [
                        (urljoin(ROOT_URL, "/saml2/ls/"),
                         saml2.BINDING_HTTP_REDIRECT),
                        (urljoin(ROOT_URL, '/saml2/ls/post/'),
                         saml2.BINDING_HTTP_POST),
                    ],
                },

            },
        },

        # Where the remote metadata is stored. This can be local or remote, see:
        # http://pysaml2.readthedocs.io/en/stable/howto/config.html#metadata
        'metadata': {
            'local': [path.join(BASEDIR, IDP_META_PATH)],
        },

        # TODO: Disable this in production
        # set to 1 to output debugging information
        'debug': 1,
        'timeslack': 5000,
        'accepted_time_diff': 5000,

        # certificate
        'key_file': path.join(BASEDIR, SP_KEY_PATH),  # private part
        'cert_file': path.join(BASEDIR, SP_CRT_PATH),  # public part

        'valid_for': 24,  # how long is our metadata valid, in hours
    }
