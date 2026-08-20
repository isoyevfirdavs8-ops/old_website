import hashlib
import hmac


class SignatureVerifier:

    @staticmethod
    def hmac_sha256(message: str, secret: str) -> str:
        return hmac.new(
            secret.encode(),
            message.encode(),
            hashlib.sha256,
        ).hexdigest()

    @staticmethod
    def md5(message: str) -> str:
        return hashlib.md5(
            message.encode()
        ).hexdigest()