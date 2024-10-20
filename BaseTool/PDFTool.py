#!/usr/bin/env python  
# -*- coding:utf-8 _*-
""" 
@author:wangjianlong
@file: PDFTool.py
@time: 2024/10/12
@contact: jlwang108@gmail.com
@site:  
@software: PyCharm 
"""
from PyPDF2 import PdfReader, PdfWriter


def decrypt_pdf(input_pdf_path, output_pdf_path, password):
	# 打开加密的 PDF 文件
	reader = PdfReader(input_pdf_path)

	# 检查是否加密
	if reader.is_encrypted:
		# 解密 PDF 文件
		reader.decrypt(password)

		# 创建 PDF 写入对象
		writer = PdfWriter()

		# 将解密后的每一页加入到新的 PDF 文件中
		for page_num in range(len(reader.pages)):
			page = reader.pages[page_num]
			writer.add_page(page)

		# 保存解密后的 PDF
		with open(output_pdf_path, "wb") as output_pdf_file:
			writer.write(output_pdf_file)
	else:
		print("PDF is not encrypted.")


def merge_pdfs(pdf_list, output_path):
	# 创建 PDF 写入对象
	writer = PdfWriter()

	# 遍历每个 PDF 文件并添加页
	for pdf in pdf_list:
		reader = PdfReader(pdf)
		for page_num in range(len(reader.pages)):
			page = reader.pages[page_num]
			writer.add_page(page)

	# 保存合并后的 PDF
	with open(output_path, "wb") as output_pdf_file:
		writer.write(output_pdf_file)


def mergePDF():
	pdf_files_to_merge = ["/Users/jl/Downloads/aa.pdf", "/Users/jl/Downloads/2-1.pdf"]
	output_merged_pdf_path = "/Users/jl/Downloads/merged_output.pdf"
	merge_pdfs(pdf_files_to_merge, output_merged_pdf_path)

def mergeEncryptedPDF():
	# 输入文件路径
	encrypted_pdf_path = "/Users/jl/Downloads/aa.pdf"  # 加密的 PDF 文件
	decrypted_pdf_path = "/Users/jl/Downloads/2-1.pdf"  # 解密后的 PDF 文件
	password = "TODO"  # 加密 PDF 的密码

	# 解密加密的 PDF 文件
	decrypt_pdf(encrypted_pdf_path, decrypted_pdf_path, password)

	# 合并所有 PDF 文件
	pdf_files_to_merge = ["/Users/jl/Downloads/1.pdf", decrypted_pdf_path]
	output_merged_pdf_path = "/Users/jl/Downloads/merged_output.pdf"
	merge_pdfs(pdf_files_to_merge, output_merged_pdf_path)
	print("PDFs merged successfully.")


# 拆分
def split_pdf_pages(input_pdf_path, output_dir):
	# 打开 PDF 文件
	with open(input_pdf_path, "rb") as input_pdf_file:
		reader = PdfReader(input_pdf_file)

		# 获取 PDF 的总页数
		num_pages = len(reader.pages)

		# 遍历每一页
		for page_index in range(num_pages):
			# 创建一个新的 PDF 写入器
			writer = PdfWriter()

			# 将当前页添加到写入器
			page = reader.pages[page_index]
			writer.add_page(page)

			# 生成输出文件路径
			output_file_path = f"{output_dir}/page_{page_index + 1}.pdf"

			# 保存当前页为新的 PDF 文件
			with open(output_file_path, "wb") as output_pdf_file:
				writer.write(output_pdf_file)

			print(f"成功保存：{output_file_path}")

if __name__ == '__main__':
	mergePDF()

	# input_pdf_path = "/Users/jl/Downloads/a.pdf"
	# output_dir = "/Users/jl/Downloads"
	#
	# split_pdf_pages(input_pdf_path, output_dir)
