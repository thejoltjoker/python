import os
import json
import subprocess


def get_exif(img_path):
    exif_data = subprocess.check_output('exiftool -j {}'.format(img_path)).decode('ascii')
    metadata = json.loads(exif_data)[0]

    return metadata


if __name__ == '__main__':
    exif = get_exif(r'C:\Users\thejoltjoker\Desktop\test\exif\f1284722688.dng')
    print(exif['RawFileName'])
