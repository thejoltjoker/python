import os

path = r"/Volumes/data_a/media/dv/tapes"

for i in range(50):

    new_folder = os.path.join(path, "{:03d}".format(i+1))
    print(new_folder)
#     if not os.path.exists(new_folder):
#         os.makedirs(new_folder)
