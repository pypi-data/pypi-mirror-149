# coding: utf-8
import ldap
from django_auth_ldap.config import LDAPSearch, NestedActiveDirectoryGroupType

LDAP_DC_NAME = "example.com"
LDAP_GROUP = "mygroup"
AUTH_LDAP_SERVER_URI = "ldap://my.ldap.server"
AUTH_LDAP_BIND_DN = "CN=MYUSER,CN=Users,"
AUTH_LDAP_BIND_PASSWORD = "**************!"

LDAP_DC = ",".join("DC=" + x for x in LDAP_DC_NAME.split("."))
AUTH_LDAP_USER_SEARCH = LDAPSearch(
    LDAP_DC, ldap.SCOPE_SUBTREE, "(sAMAccountName=%(user)s)"
)
AUTH_LDAP_GROUP_SEARCH = LDAPSearch(LDAP_DC, ldap.SCOPE_SUBTREE, "(objectClass=group)")
AUTH_LDAP_GROUP_TYPE = NestedActiveDirectoryGroupType()
AUTH_LDAP_REQUIRE_GROUP = "CN=%s,%s" % (LDAP_GROUP, LDAP_DC)
AUTH_LDAP_MIRROR_GROUPS = True
AUTH_LDAP_USER_FLAGS_BY_GROUP = {
    "is_active": AUTH_LDAP_REQUIRE_GROUP,
    "is_staff": AUTH_LDAP_REQUIRE_GROUP,
}

LOCAL_AUTHENTICATION_BACKENDS = ("django_auth_ldap.backend.LDAPBackend",)
AUTH_LDAP_START_TLS = False
AUTH_LDAP_CONNECTION_OPTIONS = {ldap.OPT_REFERRALS: 0}  # otherwise we get bind error
AUTH_LDAP_USER_ATTR_MAP = {
    "first_name": "givenName",
    "last_name": "sn",
    "email": "mail",
}
