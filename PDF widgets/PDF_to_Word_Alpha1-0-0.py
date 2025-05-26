import tkinter as tk
from tkinter import filedialog, messagebox
from pdf2docx import Converter
import os

class PDFtoWordApp:
    def __init__(self, master):
        self.master = master
        self.master.title("PDF转Word工具 Alpha 1.0.0")
        
        # 文件选择区域
        self.file_frame = tk.LabelFrame(master, text="PDF文件")
        self.file_frame.pack(padx=10, pady=5, fill="x")
        
        self.pdf_path = tk.StringVar()
        tk.Entry(self.file_frame, textvariable=self.pdf_path, width=50).pack(side="left", padx=5)
        tk.Button(self.file_frame, text="选择PDF", command=self.select_pdf).pack(side="left", padx=5)
        
        # 操作区域
        self.action_frame = tk.Frame(master)
        self.action_frame.pack(padx=10, pady=5, fill="x")
        
        tk.Button(self.action_frame, text="帮助", command=self.show_help).pack(side="left", padx=5)
        tk.Button(self.action_frame, text="转换为Word", command=self.convert_to_word).pack(side="right", padx=5)
        
        # 状态栏
        self.status_var = tk.StringVar()
        self.status_var.set("准备就绪")
        tk.Label(master, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W).pack(side=tk.BOTTOM, fill=tk.X)
    
    def select_pdf(self):
        file_path = filedialog.askopenfilename(
            title="选择PDF文件",
            filetypes=[("PDF文件", "*.pdf")]
        )
        if file_path:
            self.pdf_path.set(file_path)
            self.status_var.set(f"已选择: {os.path.basename(file_path)}")
    
    def show_help(self):
        help_text = """PDF转Word工具使用说明:
        
1. 点击"选择PDF"按钮选择要转换的PDF文件
2. 点击"转换为Word"按钮开始转换
3. 选择保存位置和文件名
        
注意: 
- 转换时间取决于PDF文件大小
- 转换过程中请勿关闭程序
- 本工具在处理大文件时，可能出现无法正常导出的情况，该问题会在后续版本中修复

提示:
- 作者:叁垣伍瑞肆凶廿捌宿宿
- 联系方式:https://space.bilibili.com/556216088
- 版权:Apache-2.0 License
"""
        messagebox.showinfo("帮助", help_text)

    def convert_to_word(self):
        pdf_path = self.pdf_path.get()
        if not pdf_path:
            messagebox.showwarning("警告", "请先选择PDF文件")
            return
        
        output_path = filedialog.asksaveasfilename(
            title="保存Word文档",
            defaultextension=".docx",
            filetypes=[("Word文档", "*.docx")]
        )
        
        if not output_path:
            return
        
        try:
            self.status_var.set("正在转换...")
            cv = Converter(pdf_path)
            cv.convert(output_path, start=0, end=None)
            cv.close()
            
            self.status_var.set("转换完成!")
            messagebox.showinfo("成功", f"PDF转换完成!\n保存到: {output_path}")
        except Exception as e:
            self.status_var.set("转换失败!")
            messagebox.showerror("错误", f"转换过程中发生错误: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFtoWordApp(root)
    root.mainloop()
