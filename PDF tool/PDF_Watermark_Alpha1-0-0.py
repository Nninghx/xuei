from PyPDF2 import PdfReader, PdfWriter
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io

class PDFWatermarkApp:
    def __init__(self, master):
        self.master = master
        self.master.title("PDF加水印工具Alpha1.0.0")
        
        # 主框架
        self.main_frame = ttk.Frame(self.master)
        self.main_frame.pack(padx=10, pady=10)
        
        # PDF文件选择
        self.pdf_frame = ttk.LabelFrame(self.main_frame, text="PDF文件")
        self.pdf_frame.pack(fill="x", padx=5, pady=5)
        
        self.pdf_path = tk.StringVar()
        ttk.Entry(self.pdf_frame, textvariable=self.pdf_path, width=50).pack(side="left", padx=5)
        ttk.Button(self.pdf_frame, text="选择PDF", command=self.select_pdf).pack(side="left", padx=5)
        
        # 水印选项
        self.options_frame = ttk.LabelFrame(self.main_frame, text="水印选项")
        self.options_frame.pack(fill="x", padx=5, pady=5)
        
        # 水印设置
        self.text_frame = ttk.Frame(self.options_frame)
        self.text_frame.pack(fill="x", pady=5)
        
        ttk.Label(self.text_frame, text="水印文字:").pack(side="left", padx=5)
        self.watermark_text = tk.StringVar(value="机密")
        ttk.Entry(self.text_frame, textvariable=self.watermark_text, width=20).pack(side="left")
        
        ttk.Label(self.text_frame, text="字体大小:").pack(side="left", padx=5)
        self.font_size = tk.IntVar(value=36)
        ttk.Spinbox(self.text_frame, from_=10, to=72, textvariable=self.font_size, 
                   width=5).pack(side="left")
        
        ttk.Label(self.text_frame, text="透明度:").pack(side="left", padx=5)
        self.opacity = tk.DoubleVar(value=0.5)
        ttk.Scale(self.text_frame, from_=0.1, to=1.0, variable=self.opacity, 
                 orient="horizontal", length=100).pack(side="left")
        
        # 水印位置
        self.position_frame = ttk.Frame(self.options_frame)
        self.position_frame.pack(fill="x", pady=5)
        
        ttk.Label(self.position_frame, text="位置:").pack(side="left", padx=5)
        self.position = tk.StringVar(value="center")
        positions = [("居中", "center"), ("左上", "topleft"), ("右上", "topright"), 
                    ("左下", "bottomleft"), ("右下", "bottomright")]
        for text, value in positions:
            ttk.Radiobutton(self.position_frame, text=text, variable=self.position, 
                           value=value).pack(side="left", padx=5)
        
        # 操作按钮
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.pack(fill="x", padx=5, pady=10)
        
        ttk.Button(self.button_frame, text="帮助", command=self.show_help).pack(side="left", padx=5)
        ttk.Button(self.button_frame, text="添加水印", command=self.add_watermark).pack(side="right", padx=5)
        
        # 帮助信息
        self.help_text = """PDF加水印工具使用说明:
1. 选择PDF文件
2. 选择水印类型:
   - 输入文字作为水印
3. 设置水印位置和透明度
4. 点击"添加水印"按钮

注意:
- 水印会自动生成
- 处理时间取决于PDF文件大小

提示:
- 作者:叁垣伍瑞肆凶廿捌宿宿
- 联系方式:https://space.bilibili.com/556216088
- 版权:Apache-2.0 License
"""
    
    def select_pdf(self):
        file_path = filedialog.askopenfilename(
            title="选择PDF文件",
            filetypes=[("PDF文件", "*.pdf")]
        )
        if file_path:
            self.pdf_path.set(file_path)
    
    def create_text_watermark(self):
        """创建文本水印PDF"""
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=letter)
        can.setFillColorRGB(0.5, 0.5, 0.5, self.opacity.get())
        can.setFont("Helvetica", self.font_size.get())
        
        text = self.watermark_text.get()
        width, height = letter
        
        # 根据位置设置文本坐标
        position = self.position.get()
        if position == "center":
            x, y = width/2, height/2
            can.drawCentredString(x, y, text)
        elif position == "topleft":
            x, y = 50, height - 50
            can.drawString(x, y, text)
        elif position == "topright":
            x, y = width - 50, height - 50
            can.drawRightString(x, y, text)
        elif position == "bottomleft":
            x, y = 50, 50
            can.drawString(x, y, text)
        elif position == "bottomright":
            x, y = width - 50, 50
            can.drawRightString(x, y, text)
        
        can.save()
        packet.seek(0)
        return PdfReader(packet)
    
    def show_help(self):
        """显示帮助信息"""
        messagebox.showinfo("使用帮助", self.help_text)
    
    def add_watermark(self):
        """添加水印到PDF"""
        pdf_path = self.pdf_path.get()
        if not pdf_path:
            messagebox.showwarning("警告", "请先选择PDF文件")
            return
        
        try:
            # 读取原始PDF
            pdf = PdfReader(pdf_path)
            if len(pdf.pages) == 0:
                messagebox.showerror("错误", "PDF文件没有有效页面")
                return
            
            # 获取文本水印
            watermark = self.create_text_watermark()
            
            # 创建PDF写入器
            writer = PdfWriter()
            
            # 为每一页添加水印
            for page in pdf.pages:
                page.merge_page(watermark.pages[0])
                writer.add_page(page)
            
            # 保存文件
            output_path = filedialog.asksaveasfilename(
                title="保存加水印的PDF",
                defaultextension=".pdf",
                filetypes=[("PDF文件", "*.pdf")]
            )
            
            if output_path:
                with open(output_path, "wb") as output_file:
                    writer.write(output_file)
                messagebox.showinfo("成功", f"PDF加水印完成!\n保存到: {output_path}")
        
        except Exception as e:
            messagebox.showerror("错误", f"加水印过程中发生错误: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFWatermarkApp(root)
    root.mainloop()
