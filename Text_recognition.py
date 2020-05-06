import tkinter as tk
from tkinter import filedialog
from tkinter import *


APP_ID = 'xxxxxxxx'  # 刚才获取的 ID，下同
API_KEY = 'xxxxxxxx'
SECRECT_KEY = 'xxxxxxxx'

import sys, os
if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']

import glob
from os import path
from aip import AipOcr
from PIL import Image

class textRecognition:
    def __init__(self):
        self.root = Tk()
        self.root.title('图片文本识别工具')
        self.root.geometry('800x600')
        self.wordText = tk.Text(self.root, width=800, height=600)
        # root.minsize(800, 600)
        # INSERT索引表示在光标处插入
        # text1.insert("insert", "我要吃饭")
        self.wordText.pack(expand=YES)

        self.mainmenu = Menu(self.root)
        self.mainmenu.add_command(label="文件选择", command=self.choose_files)
        self.mainmenu.add_command(label="文件夹选择", command=self.choose_dir)

        self.root.config(menu=self.mainmenu)
        self.root.bind('Button-3', self.popupmenu)  # 根窗体绑定鼠标右击响应事件
        self.root.mainloop()

    def popupmenu(self):
        mainmenu.post(self.x_root, self.y_root)

    def textinsert(self, str):
        self.wordText.insert(END, str+'\n')
        self.wordText.update()

    def choose_dir(self):
        dir_path = filedialog.askdirectory(initialdir=os.getcwd())
        if dir_path == "":
            print("\n取消选择")
            return

        print("\n你选择的文件夹为:")
        print(dir_path)
        self.textinsert("Path: " + dir_path)

        #遍历文件夹文件，含绝对路径
        files = []
        for (dirpath, dirnames, filenames) in os.walk(dir_path):
            for filename in filenames:
                files += [os.path.join(dirpath, filename)]
        self.text_recognize_func(files)

    def choose_files(self):
        files = filedialog.askopenfilenames(title='Select Files',
                                                 filetypes=[("BMP", "*.bmp"), ('PNG', '*.png'), ('JPG', '*.jpg'),
                                                            ('JPEG', '*.jpeg')], initialdir=os.getcwd())
        print(files)
        if len(files) == 0:
            print("\n取消选择")
            return

        text = ""
        for picfile in files:
            self.textinsert("Path: " + picfile)
            text = text + picfile
            text = text + "; "
        self.text_recognize_func(files)

    def convertimg(self, picfile, outdir):
        '''调整图片大小，对于过大的图片进行压缩
        picfile:    图片路径
        outdir：    图片输出路径
        '''
        img = Image.open(picfile)
        width, height = img.size
        while (width * height > 4000000):  # 该数值压缩后的图片大约 两百多k
            width = width // 2
            height = height // 2
        new_img = img.resize((width, height), Image.BILINEAR)
        new_img.save(path.join(outdir, os.path.basename(picfile)))

    def baiduOCR(self, picfile, outfile):
        """利用百度api识别文本，并保存提取的文字
        picfile:    图片文件名
        outfile:    输出文件
        """
        filename = path.basename(picfile)
        client = AipOcr(APP_ID, API_KEY, SECRECT_KEY)

        i = open(picfile, 'rb')
        img = i.read()

        seperate_line = "---------------------------------------------------------------------------------"
        print(seperate_line)
        self.textinsert(seperate_line)
        print("正在识别图片：\t" + filename)
        self.textinsert("正在识别图片： " + filename)
        self.textinsert("")  # 插入一个换行

        message = client.basicAccurate(img)   # 通用文字高精度识别，每天 500 次免费
        ecode = message.get('error_code')
        if None != ecode:
            print(ecode)
            print(message.get('error_message'))
            if 17 == ecode:    #每天请求超量，切换精度
                message = client.basicGeneral(img)  # 通用文字识别，每天 50 000 次免费
            else:
                return
        i.close();

        with open(outfile, 'a+') as fo:
            fo.writelines("+" * 60 + '\n')
            fo.writelines("识别图片：\t" + filename + "\n" * 2)
            fo.writelines("文本内容：\n")
            # 输出文本内容
            for text in message.get('words_result'):
                fo.writelines(text.get('words') + '\n')
                print(text.get('words'))
                self.textinsert(text.get('words'))
            self.textinsert('\n')
            fo.writelines('\n' * 2)
        print("文本导出成功！")
        print()

    def is_img(self, ext):
        print(ext)
        ext = ext.lower()
        if ext == '.jpg':
            return True
        elif ext == '.png':
            return True
        elif ext == '.jpeg':
            return True
        elif ext == '.bmp':
            return True
        else:
            return False

    def text_recognize_func(self, pic_files):
        outfile = 'export.txt'
        outdir = 'tmp'
        if path.exists(outfile):
            os.remove(outfile)
        if not path.exists(outdir):
            os.mkdir(outdir)
        print("文件预处理...")

        pflag = 0;
        for picfile in pic_files:
            print(picfile)
            fpath = os.path.dirname(picfile)
            fname = picfile[len(fpath)+1:]
            if True == self.is_img(os.path.splitext(fname)[1]):
                self.convertimg(picfile, outdir)
                pflag = 1;
            else:
                continue
        if 1 != pflag:
            return

        print("图片识别...")
        for picfile in glob.glob("tmp/*"):
            self.baiduOCR(picfile, outfile)
            os.remove(picfile)
        print('图片文本提取结束！文本输出结果位于 %s 文件中。' % outfile)
        os.removedirs(outdir)

def main():
    app = textRecognition()

if __name__ == '__main__':
    main()
