import tkinter as tk
from tkinter import filedialog, messagebox
from pdf2docx import Converter
import os
import traceback
from typing import Callable, Optional

class ConfigManager:
    """配置管理类，存储应用程序的配置信息"""
    
    # 应用版本信息
    VERSION = "Alpha 1.0.1"
    TITLE = f"PDF转Word工具 {VERSION}"
    
    # 帮助文档
    HELP_TEXT = """PDF转Word工具使用说明:
        
1. 点击"选择PDF"按钮选择要转换的PDF文件
2. 点击"转换为Word"按钮开始转换
3. 选择保存位置和文件名
        
注意: 
- 转换时间取决于PDF文件大小
- 转换过程中请勿关闭程序
提示:
- 作者:叁垣伍瑞肆凶廿捌宿宿
- 联系方式:https://space.bilibili.com/556216088
- 版权:Apache-2.0 License
"""
    
    # 更新日志
    CHANGELOG = """PDF转Word工具 更新日志

版本 α1.0.0 (Alpha)
- 初始版本发布
- 实现基本PDF转Word功能
- 添加帮助文档
α1.0.1 （2025-5-29）
- 添加更新日志
- 修复:针对大型pdf文件转换完成后，无法正常打开的问题
"""

class ErrorHandler:
    """错误处理类，提供统一的错误处理机制"""
    
    @staticmethod
    def handle_error(error: Exception, status_callback: Callable[[str], None]) -> str:
        """处理错误并返回用户友好的错误消息
        
        Args:
            error: 捕获的异常
            status_callback: 更新状态栏的回调函数
            
        Returns:
            用户友好的错误消息
        """
        error_message = str(error)
        status_callback("转换失败!")
        
        # 映射常见错误到用户友好的消息
        if "Permission denied" in error_message:
            return "无法访问输出文件，请确保文件未被其他程序占用且有写入权限。"
        elif "not found" in error_message.lower():
            return "找不到指定的PDF文件，请确保文件路径正确。"
        elif "index out of range" in error_message.lower():
            return "PDF文件格式异常，无法正确读取页面内容。"
        elif "memory" in error_message.lower():
            return "内存不足，请尝试转换较小的PDF文件或关闭其他应用程序后重试。"
        else:
            # 记录详细错误信息到日志（这里简化为打印）
            print(f"Error details: {traceback.format_exc()}")
            return f"转换过程中发生错误:\n{error_message}"
    
    @staticmethod
    def show_error(message: str):
        """显示错误消息对话框
        
        Args:
            message: 要显示的错误消息
        """
        messagebox.showerror("错误", message)


class PDFConverter:
    """PDF转换类，处理PDF到Word的转换逻辑"""
    
    def __init__(self, update_status: Callable[[str], None], update_ui: Callable[[], None]):
        """初始化PDF转换器
        
        Args:
            update_status: 更新状态栏的回调函数
            update_ui: 更新UI的回调函数
        """
        self.update_status = update_status
        self.update_ui = update_ui
        self.cv = None
    
    def convert(self, pdf_path: str, output_path: str) -> bool:
        """将PDF转换为Word文档
        
        Args:
            pdf_path: PDF文件路径
            output_path: 输出Word文件路径
            
        Returns:
            转换是否成功
        """
        try:
            self.update_status("正在转换...")
            self.update_ui()
            
            # 创建转换器实例
            self.cv = Converter(pdf_path)
            total_pages = len(self.cv.pages)
            
            # 尝试使用tqdm进行进度显示
            try:
                self._convert_with_tqdm(output_path, total_pages)
            except ImportError:
                self._convert_simple(output_path, total_pages)
            
            self.update_status("转换完成!")
            return True
            
        except Exception as e:
            error_message = ErrorHandler.handle_error(e, self.update_status)
            ErrorHandler.show_error(error_message)
            return False
        finally:
            if self.cv:
                self.cv.close()
    
    def _convert_with_tqdm(self, output_path: str, total_pages: int):
        """使用tqdm库进行带进度条的转换
        
        Args:
            output_path: 输出Word文件路径
            total_pages: PDF总页数
        """
        from tqdm import tqdm
        
        # 创建进度条
        with tqdm(total=total_pages, desc="转换进度", unit="页") as progress_bar:
            # 一次性转换所有页面
            self.cv.convert(output_path)
            # 更新进度条
            progress_bar.update(total_pages)
            self.update_status(f"已完成转换: 共 {total_pages} 页")
            self.update_ui()
    
    def _convert_simple(self, output_path: str, total_pages: int):
        """使用简单模式进行转换（无tqdm库时）
        
        Args:
            output_path: 输出Word文件路径
            total_pages: PDF总页数
        """
        self.update_status("正在转换(简单模式)...")
        self.update_ui()
        
        # 一次性转换所有页面
        self.cv.convert(output_path)
        self.update_status(f"已完成转换: 共 {total_pages} 页 (简单模式)")
        self.update_ui()


class UIComponents:
    """UI组件类，管理应用程序的界面元素"""
    
    def __init__(self, master: tk.Tk, app_instance):
        """初始化UI组件
        
        Args:
            master: tkinter主窗口
            app_instance: 应用程序实例，用于回调
        """
        self.master = master
        self.app = app_instance
        self.pdf_path = tk.StringVar()
        self.status_var = tk.StringVar()
        self.status_var.set("准备就绪")
    
    def create_widgets(self):
        """创建所有UI组件"""
        self.create_file_frame()
        self.create_action_frame()
        self.create_status_bar()
    
    def create_file_frame(self):
        """创建文件选择区域"""
        file_frame = tk.LabelFrame(self.master, text="PDF文件")
        file_frame.pack(padx=10, pady=5, fill="x")
        
        tk.Entry(file_frame, textvariable=self.pdf_path, width=50).pack(side="left", padx=5)
        tk.Button(file_frame, text="选择PDF", command=self.app.select_pdf).pack(side="left", padx=5)
    
    def create_action_frame(self):
        """创建操作按钮区域"""
        action_frame = tk.Frame(self.master)
        action_frame.pack(padx=10, pady=5, fill="x")
        
        tk.Button(action_frame, text="帮助", command=self.app.show_help).pack(side="left", padx=5)
        tk.Button(action_frame, text="更新日志", command=self.app.show_changelog).pack(side="left", padx=5)
        tk.Button(action_frame, text="转换为Word", command=self.app.convert_to_word).pack(side="right", padx=5)
    
    def create_status_bar(self):
        """创建状态栏"""
        tk.Label(
            self.master, 
            textvariable=self.status_var, 
            bd=1, 
            relief=tk.SUNKEN, 
            anchor=tk.W
        ).pack(side=tk.BOTTOM, fill=tk.X)
    
    def update_status(self, message: str):
        """更新状态栏消息
        
        Args:
            message: 状态消息
        """
        self.status_var.set(message)
    
    def update_ui(self):
        """强制更新UI"""
        self.master.update()


class PDFtoWordApp:
    """PDF转Word应用程序主类"""
    
    def __init__(self, master: tk.Tk):
        """初始化应用程序
        
        Args:
            master: tkinter主窗口
        """
        self.master = master
        self.master.title(ConfigManager.TITLE)
        
        # 初始化UI组件
        self.ui = UIComponents(master, self)
        self.ui.create_widgets()
        
        # 初始化PDF转换器
        self.converter = PDFConverter(self.ui.update_status, self.ui.update_ui)
    
    def select_pdf(self):
        """选择PDF文件"""
        file_path = filedialog.askopenfilename(
            title="选择PDF文件",
            filetypes=[("PDF文件", "*.pdf")]
        )
        if file_path:
            self.ui.pdf_path.set(file_path)
            self.ui.update_status(f"已选择: {os.path.basename(file_path)}")
    
    def show_help(self):
        """显示帮助信息"""
        messagebox.showinfo("帮助", ConfigManager.HELP_TEXT)
    
    def show_changelog(self):
        """显示更新日志"""
        messagebox.showinfo("更新日志", ConfigManager.CHANGELOG)
    
    def convert_to_word(self):
        """将PDF转换为Word文档"""
        pdf_path = self.ui.pdf_path.get()
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
        
        if self.converter.convert(pdf_path, output_path):
            messagebox.showinfo("成功", f"PDF转换完成!\n保存到: {output_path}")


def main():
    """应用程序入口点"""
    root = tk.Tk()
    app = PDFtoWordApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()