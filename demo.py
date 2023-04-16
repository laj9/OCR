import os
from ocr import ocr
import time
import shutil
import numpy as np
from PIL import Image
from glob import glob


def single_pic_proc(image_file):
    image = np.array(Image.open(image_file).convert('RGB'))
    result, image_framed = ocr(image)
    return result, image_framed


if __name__ == '__main__':
    image_files = glob('./test_images/*.*')
    result_dir = './test_result'
    if os.path.exists(result_dir):
        shutil.rmtree(result_dir)
    os.mkdir(result_dir)

    #现在是两个循环 每次会检测一张图片 第二个循环每次输入一个字符
    #可以设置一个总的文档每次都输入在同一个文档中
    #或者可以最后再新创建一个文档，依次将数据读入

    for image_file in sorted(image_files):
        t = time.time()
        result, image_framed = single_pic_proc(image_file)
        output_file = os.path.join(result_dir, image_file.split('\\')[-1])
        txt_file = os.path.join(result_dir, image_file.split('\\')[-1].split('.')[0]+'.txt')
        #print(txt_file)
        txt_f = open(txt_file, 'w')
        Image.fromarray(image_framed).save(output_file)
        print("Mission complete, it took {:.3f}s".format(time.time() - t))
        print("\nRecognition Result:\n")
        for key in result:
            print(result[key][1])
            txt_f.write(result[key][1]+'\n')
        txt_f.close()