import os

filename = r"C:\APT_Images\CameraCCD_1\2021-05-06\L_2021-05-06_20-13-32_Bin1x1_1s__-10C.fit"

filename = filename.replace('\\','/')

drive, path_and_file = os.path.splitdrive(filename)

path, file = os.path.split(path_and_file)

new_loc = path + '/apt_thumbs/'


new_loc = drive + new_loc + file


new_loc = new_loc.replace('fit','png')
