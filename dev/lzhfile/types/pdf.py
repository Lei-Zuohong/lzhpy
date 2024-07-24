# -*- coding: UTF-8 -*-
# Public package
# Private package
import lzhfile
# Internal package
import PIL.Image as Image
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True


def pics_to_pdf(path_pics=[],
                path_pdf=''):
    pic_list = []
    for count, path_pic in enumerate(path_pics):
        pic = Image.open(path_pic)
        if(len(pic.split()) == 4):
            r, g, b, a = pic.split()
            pic = Image.merge('RGB', (r, g, b))
            pic.convert('RGB')
        if(count == 0):
            pic_out = pic
        else:
            pic_list.append(pic)
    try:
        pic_out.save(path_pdf, 'PDF', resolution=100.0, save_all=True, append_images=pic_list)
    except:
        print('Error')
        print(path_pics)
    return 1


def folder_to_pdf(path_folder='',
                  path_output=''):
    # 读取图片列表
    folder_loca, folder_name = lzhfile.path_split(path_folder)
    files = lzhfile.get_leaf(path_folder)
    input_pic = []
    for file in files:
        if(file.is_picture()):
            input_pic.append(file.name)
    if(len(input_pic) == 0):
        return 0
    # 整理图片列表
    input_pic.sort()
    for count, i in enumerate(input_pic):
        input_pic[count] = '%s/%s' % (path_folder, input_pic[count])
    # 转换pdf
    pics_to_pdf(path_pics=input_pic,
                path_pdf='%s/%s.pdf' % (path_output, folder_name))
    print('Successful output:')
    print(folder_name)
    return 1
