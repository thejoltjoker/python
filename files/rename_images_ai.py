import time
import os
from clarifai.rest import ClarifaiApp


def get_image_content(img_path, keywords=3, separator='-'):
    app = ClarifaiApp(api_key=os.environ['CLARIFAI_API_KEY'])

    # Shrink image for upload
    temp_img_path = shrink_image(img_path)

    # Upload image and get content
    model = app.public_models.general_model
    response = model.predict_by_filename(temp_img_path)

    return separator.join([x['name'] for x in response['outputs'][0]['data']['concepts']][:keywords])
    # return response['outputs'][0]['data']['concepts'][0]['name']


def shrink_image(img_path, pixels=65000):
    path, filename = os.path.split(img_path)

    shrunken_image = os.path.join(path, '_img_ai_rename_temp.jpg')
    os.system(
        "magick convert {in_img} -resize {px}@ {out_img}".format(in_img=img_path, out_img=shrunken_image, px=pixels))
    return shrunken_image


def get_file_date(file_path):
    return time.strftime('%y%m%d', time.gmtime(os.path.getmtime(file_path)))


def rename_images(base_path):
    # base_path = r'E:\Dropbox\Pictures\other\cats'
    print(base_path)
    for subdir, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith(('jpg', 'png', 'gif')):
                increment = 1
                file_ext = os.path.splitext(file)[1]
                file_path = os.path.join(subdir, file)
                date = get_file_date(file_path)
                img_content = get_image_content(file_path)
                new_name = '{date}_{content}_{inc:03d}{ext}'.format(date=date,
                                                                    content=img_content,
                                                                    inc=increment,
                                                                    ext=file_ext)
                new_file_path = os.path.join(subdir, new_name)

                while os.path.exists(new_file_path):
                    increment += 1
                    new_name = '{date}_{content}_{inc:03d}{ext}'.format(date=date,
                                                                        content=img_content,
                                                                        inc=increment,
                                                                        ext=file_ext)
                    new_file_path = os.path.join(subdir, new_name)

                os.rename(file_path, new_file_path)

                print("{old} -> {new}".format(old=file_path, new=new_file_path))

    # Remove temp file
    temp_file = os.path.join(base_path, '_img_ai_rename_temp.jpg')
    if os.path.exists(temp_file):
        os.remove(temp_file)


if __name__ == '__main__':
    rename_images(r'E:\Dropbox\resources\reference\whiteShark')
