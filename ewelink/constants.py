from typing import ClassVar

def api_key(key):
    import json

    with open("/var/www/html/dev/api_keys/api_keys.json") as f:
        keys = json.load(f)
    if key in keys:
        api_key = keys[key]
        #print(api_key)
        return api_key
    else:
        print(f'Not found api key:[{key}]')
        print (keys)
        return 'dummy_key'

def api_key_binary(key):
    import json

    with open("/var/www/html/dev/api_keys/api_keys.json") as f:
        keys = json.load(f)
    if key in keys:
        api_key = keys[key]
        api_key_bin = api_key.encode("utf-8")
        return api_key_bin
    else:
        print(f'Not found api key:[{key}]')
        return 'dummy_key'



class Constants:
    APP_ID: ClassVar[str] = api_key('EWELINK_APP_ID')
    APP_SECRET: ClassVar[bytes] = api_key_binary('EWELINK_APP_SECRET_BINARY')
    errors: ClassVar[dict[int, str]] =\
    {
        400: 'Parameter error',
        401: 'Wrong account or password',
        402: 'Email inactivated',
        403: 'Forbidden',
        404: 'Device does not exist',
        406: 'Authentication failed',
        503: 'Service Temporarily Unavailable or Device is offline'
    }
    customErrors: ClassVar[dict[str, str]] =\
    {
        'ch404': 'Device channel does not exist',
        'unknown': 'An unknown error occurred',
        'noDevices': 'No devices found',
        'noPower': "No power usage data found",
        'noSensor': 'Can\'t read sensor data from device',
        'noFirmware': "Can't get model or firmware version",
        'invalidAuth': 'Library needs to be initialized using email and password',
        'invalidCredentials': 'Invalid credentials provided',
        'invalidPower': 'Invalid power state. Expecting: "on", "off" or "toggle"',
    }
