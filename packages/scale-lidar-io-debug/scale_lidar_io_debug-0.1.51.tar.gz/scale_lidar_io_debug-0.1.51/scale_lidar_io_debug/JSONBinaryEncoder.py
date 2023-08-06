import numpy as np
import ujson


class JSONBinaryEncoder:
    block_size = 4

    def fill_block(self, data, fill=b'\00'):
        return data + fill * (self.block_size - len(data) % self.block_size)

    def encode_object(self, obj, keys=None, items=None, buffer=None, **params):
        keys = keys or []
        items = items or []
        buffer = buffer or bytes(self.block_size)

        if isinstance(obj, dict):
            obj = dict(obj)
            for k, v in obj.items():
                obj[k], items, buffer = self.encode_object(v, keys + [k], items, buffer, **params)

        if isinstance(obj, list):
            obj = list(obj)
            for k, v in enumerate(obj):
                obj[k], items, buffer = self.encode_object(v, keys + [k], items, buffer, **params)

        elif isinstance(obj, bytes):
            offset = len(buffer)
            items.append(dict(params, keys=keys, length=len(obj), offset=offset))
            buffer += self.fill_block(obj)
            obj = ''

        elif isinstance(obj, np.ndarray):
            obj, dtype, shape = obj.tobytes(), obj.dtype.name, obj.shape
            obj, items, buffer = self.encode_object(obj, keys, items, buffer, dtype=dtype, shape=shape)

        return obj, items, buffer

    def set_nested(self, obj: dict, keys: list, value):
        while len(keys) > 1:
            obj = obj[keys.pop(0)]
        obj[keys[0]] = value

    def dumps(self, obj: dict):
        obj, items, buffer = self.encode_object(obj)
        header = dict(obj)
        header['$items'] = items
        encoded_header = self.fill_block(ujson.dumps(header).encode('utf-8'), b' ')
        return encoded_header + buffer

    def loads(self, data: bytes):
        header_length = data.find(bytes(1))
        obj = ujson.loads(data[:header_length].decode('utf-8'))
        items = obj.pop('$items')
        data = data[header_length:]

        for item in items:
            value = data[item['offset']:item['offset'] + item['length']]
            if 'dtype' in item:
                value = np.frombuffer(value, dtype=item['dtype'])
            if 'shape' in item:
                value = value.reshape(item['shape'])
            self.set_nested(obj, item['keys'], value)

        return obj

    def write_file(self, file_path: str, obj: dict):
        with open(file_path, 'wb') as fp:
            fp.write(self.dumps(obj))

    def read_file(self, file_path: str) -> dict:
        with open(file_path, 'rb') as fp:
            return self.loads(fp.read())
