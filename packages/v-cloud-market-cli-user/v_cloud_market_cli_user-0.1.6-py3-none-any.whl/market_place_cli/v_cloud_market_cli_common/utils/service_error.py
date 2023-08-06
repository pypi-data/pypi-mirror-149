class ServiceException(Exception):
    pass

class WalletServiceException(Exception):
    pass

class WalletDecryptionException(WalletServiceException):
    pass

class WalletEncryptionException(WalletServiceException):
    pass

class WalletStorageLoadingException(WalletServiceException):
    pass

class WalletStorageSavingException(WalletServiceException):
    pass

class HttpNotFoundException(Exception):
    pass

class HttpInternalErrorException(Exception):
    pass

class HttpBadRequestException(Exception):
    pass
