from ssl import PROTOCOL_TLS_SERVER, CERT_REQUIRED, SSLContext

class SSLCertificateManager():
    certfile: str
    keyfile: str
    ssl_config: SSLContext

    def __init__(self, config):
        self.certfile = config["certfile"]
        self.keyfile = config["keyfile"]
        self.ssl_config = SSLContext(PROTOCOL_TLS_SERVER)
        self.ssl_config.load_cert_chain(certfile=self.certfile, keyfile=self.keyfile)
        self.ssl_config.verify_mode = CERT_REQUIRED
        self.ssl_config.check_hostname = True
        self.ssl_config.load_default_certs()
