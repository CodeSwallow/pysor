import base64
import hmac
import hashlib
import time
import urllib.parse


def generate_sas_token(uri: str, key: str, policy_name: str, expiry: int = 3600) -> str:
    """
    Generate a Shared Access Signature (SAS) token.

    :param uri: URI of the resource (URL encoded).
    :param key: Key used for creating the token.
    :param policy_name: Name of the Shared Access Policy.
    :param expiry: Token expiry time in seconds.
    :return: SAS token as a string.
    """
    ttl = time.time() + expiry
    sign_key = "%s\n%d" % ((urllib.parse.quote_plus(uri)), int(ttl))
    signature = base64.b64encode(hmac.HMAC(base64.b64decode(key), sign_key.encode('utf-8'), hashlib.sha256).digest())

    raw_token = {
        'sr':  uri,
        'sig': signature,
        'se': str(int(ttl))
    }

    if policy_name is not None:
        raw_token['skn'] = policy_name

    return 'SharedAccessSignature ' + urllib.parse.urlencode(raw_token)
