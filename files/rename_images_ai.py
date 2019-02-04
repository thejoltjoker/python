import time
import os
from clarifai.rest import ClarifaiApp
import string


def validate_filename(file_name):
    valid_chars = " -_.{letters}{digits}".format(letters=string.ascii_letters, digits=string.digits)
    valid_file_name = file_name.replace('å', 'a')
    valid_file_name = valid_file_name.replace('ä', 'a')
    valid_file_name = valid_file_name.replace('ö', 'o')
    valid_file_name = ''.join(c for c in valid_file_name if c in valid_chars)
    valid_file_name = valid_file_name.replace(' ', '_')
    return valid_file_name


def get_image_content(img_path, keywords=3, separator='-'):
    app = ClarifaiApp(api_key=os.environ['CLARIFAI_API_KEY'])

    # Shrink image for upload
    temp_img_path = shrink_image(img_path)

    # Upload image and get content
    model = app.public_models.general_model
    response = model.predict_by_filename(temp_img_path)

    return separator.join([validate_filename(x['name']) for x in response['outputs'][0]['data']['concepts']][:keywords])
    # return response['outputs'][0]['data']['concepts'][0]['name']


def shrink_image(img_path, pixels=65000):
    path, filename = os.path.split(img_path)

    shrunken_image = os.path.join(path, '_img_ai_rename_temp.jpg')
    os.system(
        "magick convert {in_img} -resize {px}@ {out_img}".format(in_img=img_path, out_img=shrunken_image, px=pixels))
    return shrunken_image


def get_file_date(file_path):
    return time.strftime('%y%m%d', time.gmtime(os.path.getmtime(file_path)))


def get_insta_author(file_name):
    return os.path.splitext(file_name)[0].split('_')[-1]


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
                insta = get_insta_author(file_path)
                img_content = get_image_content(file_path)
                new_name = '{date}_{content}_{insta}_{inc:03d}{ext}'.format(date=date,
                                                                            content=img_content,
                                                                            insta=insta,
                                                                            inc=increment,
                                                                            ext=file_ext)
                new_file_path = os.path.abspath(os.path.join(r'K:\insta_renamed', new_name))

                while os.path.exists(new_file_path):
                    increment += 1
                    new_name = '{date}_{content}_{insta}_{inc:03d}{ext}'.format(date=date,
                                                                                content=img_content,
                                                                                insta=insta,
                                                                                inc=increment,
                                                                                ext=file_ext)
                    new_file_path = os.path.abspath(os.path.join(r'K:\insta_renamed', new_name))

                os.rename(file_path, new_file_path)

                print("{old} -> {new}".format(old=file_path, new=new_file_path))

    # Remove temp file
    temp_file = os.path.join(base_path, '_img_ai_rename_temp.jpg')
    if os.path.exists(temp_file):
        os.remove(temp_file)


if __name__ == '__main__':
    rename_images(r'Q:/')
