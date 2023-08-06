# -*- coding: utf-8 -*-
import reportlab
import os
from PyPDF2 import PdfFileWriter, PdfFileReader
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFont
from fpdf import FPDF


def create_watermark(content):
    """创建PDF水印模板
    """
    # 创建一个PDF文件来作为一个水印文件
    c = canvas.Canvas('watermark.pdf')
    reportlab.pdfbase.pdfmetrics.registerFont(
        reportlab.pdfbase.ttfonts.TTFont('simfang', 'C:/Windows/Fonts/simfang.ttf'))
    c.setFont('simfang', 20)
    c.saveState()
    c.translate(305, 505)
    c.rotate(45)
    c.drawCentredString(0, 0, content)
    c.restoreState()
    c.save()
    pdf_watermark = PdfFileReader('watermark.pdf')
    return pdf_watermark


def pdf_add_watermark(pdf_file_in, pdf_file_mark, pdf_file_out):
    # print(pdf_file_out)
    pdf_output = PdfFileWriter()
    input_stream = open(pdf_file_in, 'rb')
    pdf_input = PdfFileReader(input_stream, strict=False)
    # 获取PDF文件的页数
    if pdf_input.getIsEncrypted():
        print("文件已被加密")
        PDF_Passwd = input("请输入PDF密码：")
        # 尝试用空密码解密
        try:
            pdf_input.decrypt(PDF_Passwd)
        except Exception:
            print(f"尝试用密码{PDF_Passwd}解密失败.")
            return False
    pageNum = pdf_input.getNumPages()
    # 读入水印pdf文件
    # print(pdf_file_mark)
    mark_stream = open(pdf_file_mark, mode='rb')
    pdf_watermark = PdfFileReader(mark_stream, strict=False)
    # 给每一页打水印
    for i in range(pageNum):
        page = pdf_input.getPage(i)
        page.mergePage(pdf_watermark.getPage(0))
        page.compressContentStreams()  # 压缩内容
        pdf_output.addPage(page)
    pdf_output.write(open(pdf_file_out, 'wb'))


def add_watermark():
    pdf_file_in = input("请输入需要添加水印的文件位置：")  # 需要添加水印的文件
    Watermark_Str = input("请输入需要添加的水印内容：")
    print('=' * 20)
    print('正在按要求，给你的PDF文件添加水印，请让程序飞一会儿~')
    print('=' * 20)
    pdf_file_mark = 'watermark.pdf'  # 水印文件
    create_watermark(str(Watermark_Str))
    pdf_file_out = '添加了水印的文件.pdf'  # 添加PDF水印后的文件
    pdf_add_watermark(pdf_file_in, pdf_file_mark, pdf_file_out)
    print("水印添加结束，请打开电脑上的这个位置，查看结果文件：{path}".format(path=os.getcwd()))


def txt2pdf():
    pdf = FPDF()
    pdf.add_page()  # Add a page
    pdf.set_font("Arial", size=15)  # set style and size of font
    f = open(
        'D:\\workplace\\code\\BaiduNetdiskWorkspace\\personal\\linux\\workplace\\pro\\git\\gitee\\python-office\\test\\allpackages.txt',
        "r")  # open the text file in read mode
    # insert the texts in pdf
    for x in f:
        pdf.cell(50, 5, txt=x, ln=1, align='C')
    # pdf.output("path where you want to store pdf file\\file_name.pdf")
    pdf.output("game_notes.pdf")
