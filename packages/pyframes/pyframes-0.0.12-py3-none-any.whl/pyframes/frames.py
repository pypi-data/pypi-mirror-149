import io
import base64
import requests
import numpy as np
from PIL import Image


class Record:
    def __init__(self):
        self.id = None
        self.pki = None
        self.enum_mode = None
        self.uint32_t_created = None
        self.uint32_t_modified = None
        self.uint32_t_detected = None
        self.bool_exists = None
        self.bool_moderated = None
        self.bool_processed = None
        self.fk_program = None
        self.uint8_t_locale = None
        self.fk_device = None

    def from_json(self, data):
        if 'id' in data:
            self.id = data['id']
        if 'pki' in data:
            self.pki = data['pki']
        if 'enum_mode' in data:
            self.enum_mode = data['enum_mode']
        if 'uint32_t_created' in data:
            self.uint32_t_created = data['uint32_t_created']
        if 'uint32_t_modified' in data:
            self.uint32_t_modified = data['uint32_t_modified']
        if 'uint32_t_detected' in data:
            self.uint32_t_detected = data['uint32_t_detected']
        if 'bool_exists' in data:
            self.bool_exists = data['bool_exists']
        if 'bool_moderated' in data:
            self.bool_moderated = data['bool_moderated']
        if 'bool_processed' in data:
            self.bool_processed = data['bool_processed']
        if 'fk_program' in data:
            self.fk_program = data['fk_program']
        if 'uint8_t_locale' in data:
            self.uint8_t_locale = data['uint8_t_locale']
        if 'fk_device' in data:
            self.fk_device = data['fk_device']


class Position:
    def __init__(self):
        self.id = None
        self.pki = None
        self.uint32_t_created = None
        self.uint32_t_modified = None
        self.float_latitude = None
        self.float_longitude = None
        self.float_latitude_uere = None
        self.float_longitude_uere = None
        self.point_position = None
        self.point_position_uere = None
        self.float_velocity = None
        self.float_altitude = None
        self.uint32_satellite_visible = None
        self.uint32_satellite_locked = None
        self.fk_record_id = None
        self.fki_record = None

    def from_json(self, data):
        if 'id' in data:
            self.id = data['id']
        if 'pki' in data:
            self.pki = data['pki']
        if 'uint32_t_created' in data:
            self.uint32_t_created = data['uint32_t_created']
        if 'uint32_t_modified' in data:
            self.uint32_t_modified = data['uint32_t_modified']
        if 'float_latitude' in data:
            self.float_latitude = data['float_latitude']
        if 'float_longitude' in data:
            self.float_longitude = data['float_longitude']
        if 'float_latitude_uere' in data:
            self.float_latitude_uere = data['float_latitude_uere']
        if 'float_longitude_uere' in data:
            self.float_longitude_uere = data['float_longitude_uere']
        if 'point_position' in data:
            self.point_position = data['point_position']
        if 'point_position_uere' in data:
            self.point_position_uere = data['point_position_uere']
        if 'float_velocity' in data:
            self.float_velocity = data['float_velocity']
        if 'float_altitude' in data:
            self.float_altitude = data['float_altitude']
        if 'uint32_satellite_visible' in data:
            self.uint32_satellite_visible = data['uint32_satellite_visible']
        if 'uint32_satellite_locked' in data:
            self.uint32_satellite_locked = data['uint32_satellite_locked']
        if 'fk_record_id' in data:
            self.fk_record_id = data['fk_record_id']
        if 'fki_record' in data:
            self.fki_record = data['fki_record']


class Weather:
    def __init__(self):
        self.id = None
        self.pki = None
        self.uint32_t_created = None
        self.uint32_t_modified = None
        self.vchar_station = None
        self.float_temp = None
        self.float_humidity = None
        self.float_pressure = None
        self.vchar_description = None
        self.vchar_icon = None
        self.fk_record_id = None

    def from_json(self, data):
        if 'id' in data:
            self.id = data['id']
        if 'pki' in data:
            self.pki = data['pki']
        if 'uint32_t_created' in data:
            self.uint32_t_created = data['uint32_t_created']
        if 'uint32_t_modified' in data:
            self.uint32_t_modified = data['uint32_t_modified']
        if 'vchar_station' in data:
            self.vchar_station = data['vchar_station']
        if 'float_temp' in data:
            self.float_temp = data['float_temp']
        if 'float_humidity' in data:
            self.float_humidity = data['float_humidity']
        if 'float_pressure' in data:
            self.float_pressure = data['float_pressure']
        if 'vchar_description' in data:
            self.vchar_description = data['vchar_description']
        if 'vchar_icon' in data:
            self.vchar_icon = data['vchar_icon']
        if 'fk_record_id' in data:
            self.fk_record_id = data['fk_record_id']


class Storage:
    def __init__(self):
        self.pki = None
        self.image = None
        self.meta = None
        self.fk_record_id = None
        self.fki_record_id = None

    def _b64_to_image(self, b64: np.array):
        bytes_array = base64.b64decode(b64.encode())
        # ensure numpy array
        bytes_array = np.array(bytes_array)
        # instantiate a BytesIO object
        bytesIO = io.BytesIO(bytes_array)
        # instantiate a Pillow Image object
        image = Image.open(bytesIO)
        # return a numpy array of the image
        return np.array(image)

    def from_json(self, data):
        if 'pki' in data:
            self.pki = data['pki']
        if 'base64_bytes_array' in data:
            # converts to image on load
            self.image = self._b64_to_image(data['base64_bytes_array'])
        if 'meta' in data:
            self.meta = data['meta']
        if 'fk_record_id' in data:
            self.fk_record_id = data['fk_record_id']
        if 'fki_record_id' in data:
            self.fki_record_id = data['fki_record_id']


class FramesManager:
    def __init__(self):
        self.url = 'https://api.spothole.sensorit.io'
        self.jwt = None

    def set_jwt(self, jwt):
        headers = {
            'content-type': 'application/json',
            'x-access-tokens': jwt
        }

        uri = "{}/protected".format(self.url)

        response = requests.get(uri, headers=headers)

        if response.status_code == 200:
            self.jwt = jwt
            print('JWT Accepted ({}).'.format(response.status_code))
        else:
            print('Invalid JWT ({})!'.format(response.status_code))

    def search(self, lat: float, lon: float, radius: float) -> list:
        uri = "{}/record/id/radius".format(self.url, id)
        params = {'lat': lat, 'lon': lon, 'radius': radius}

        return self._get(uri, params)['ids']

    def _get(self, uri, params=None) -> dict:
        headers = {
            'content-type': 'application/json',
            'x-access-tokens': self.jwt
        }

        response = requests.get(uri, headers=headers, params=params)

        if response.status_code == 200:
            return response.json()
        else:
            return {'code': response.status_code}

    def get_record(self, pki: str) -> Record:
        uri = "{}/record/{}".format(self.url, pki)

        r = Record()
        r.from_json(self._get(uri))
        return r

    def get_position(self, pki: str) -> Position:
        uri = "{}/position/{}".format(self.url, pki)

        p = Position()
        p.from_json(self._get(uri))
        return p

    def get_storage(self, pki: str) -> Storage:
        uri = "{}/storage/{}".format(self.url, pki)

        s = Storage()
        s.from_json(self._get(uri))
        return s

    def get_weather(self, id: int) -> Weather:
        uri = "{}/weather/{}".format(self.url, id)

        w = Weather()
        w.from_json(self._get(uri))
        return w


if __name__ == "__main__":
    fm = FramesManager()
    jwt = input("Token: ")
    fm.set_jwt(jwt)
    ids = fm.search(lat=-33.918861, lon=18.423300, radius=1000)

    for id in ids:
        record = fm.get_record(id)
        position = fm.get_position(id)
        weather = fm.get_position(id)
        storage = fm.get_storage(id)

        print(record.id)

    # import matplotlib
    # matplotlib.use('TkAgg')
    # import matplotlib.pyplot as plt
    # plt.figure()
    # plt.imshow(storage.image)
    # plt.show()
