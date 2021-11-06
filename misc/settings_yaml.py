
class Settings:
    def __init__(self, path='settings.yml', **default_settings):
        self.host = platform.node()
        self.file = Path(str(path).format(host=self.host))

        # Create file if it doesn't exist
        if not self.file.is_file():
            self.file.touch()

        # Write default settings
        self._write(**default_settings)

    def _read(self):
        with self.file.open('r') as file:
            data = yaml.load(file)
            if data:
                return data
            return {}

    def _write(self, **settings):
        data = self._read()
        data.update(**settings)
        with self.file.open('w') as file:
            yaml.dump(data, file)

    def set(self, **settings):
        self._write(**settings)

    def get(self, *settings, fallback=None):
        logging.debug(settings)
        data = []
        for k, v in self._read().items():
            if k in settings:
                data.append(v)
        if len(data) == 1:
            return data[0]
        elif len(data) > 1:
            return data
        else:
            return fallback