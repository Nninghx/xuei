import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import os
import sys

class ToolLauncher:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("工具启动器-V1.0.0")
        self.root.geometry("400x500")
        
        # 工具列表
        self.tools = {
            'PDF工具': {
                'PDF拆分': 'PDF Chai Fen Alpha1.0.2.py',
                'PDF合并': 'PDF He Bing Alpha1.0.1.py',
                'PDF转Word': 'PDF_to_Word_Alpha1.0.0.py',
                'PDF加水印': 'PDF_Watermark_Alpha1.0.0.py'
            },
            '图片工具': {
                '九宫格分割': 'Tu Pian Fen Ge Jiu Gong Ge-Alpha1.0.0.py',
                '格式转换': 'Tu Pian Ge Shi Zhuan Huan-Alpha1.0.0.py',
                'ICO转换': 'Tu Pian Zhuan ico-Alpha1.0.0.py',
                '图片合成': 'Tu_Pian_He_Cheng_Alpha.py'
            },
            '音频工具': {
                '音频提取': 'Yin Pin Ti Qu-Alpha1.0.1.py'
            }
        }
        
        # 设置窗口图标
        try:
            icon_path = os.path.join(os.path.dirname(__file__), 'icon.ico')
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
        except:
            pass
        
        # 检查工具完整性
        self.check_tools()
        
        self.setup_ui()
        
    def check_tools(self):
        """检查工具完整性"""
        missing_tools = []
        
        for category, tools in self.tools.items():
            for tool_name, file_name in tools.items():
                tool_path = os.path.join(os.path.dirname(__file__), file_name)
                if not os.path.exists(tool_path):
                    missing_tools.append(f"{category} - {tool_name} ({file_name})")
        
        if missing_tools:
            warning_message = "以下工具未找到：\n\n" + "\n".join(missing_tools)
            messagebox.showwarning("工具缺失", warning_message)
        
    def setup_ui(self):
        # 创建顶部按钮框架
        top_frame = ttk.Frame(self.root)
        top_frame.pack(fill="x", padx=10, pady=5)
        
        # 添加刷新按钮
        refresh_button = ttk.Button(top_frame, text="刷新", command=self.refresh_tools)
        refresh_button.pack(side="left", padx=5)
        
        # 添加帮助和关于按钮
        help_button = ttk.Button(top_frame, text="帮助", command=self.show_help)
        help_button.pack(side="right", padx=5)
        
        about_button = ttk.Button(top_frame, text="关于", command=self.show_about)
        about_button.pack(side="right", padx=5)
        
        # 创建工具列表框架
        frame = ttk.LabelFrame(self.root, text="可用工具", padding="10")
        frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # 动态创建工具按钮
        for category, tools in self.tools.items():
            # 添加分类标签
            ttk.Label(frame, text=f"{category}：", font=("", 10, "bold")).pack(anchor="w", pady=(10,0))
            
            # 添加工具按钮
            for tool_name, file_name in tools.items():
                # 检查工具是否存在
                tool_path = os.path.join(os.path.dirname(__file__), file_name)
                button = ttk.Button(frame, text=tool_name, width=30,
                                  command=lambda f=file_name: self.run_tool(f))
                
                # 如果工具不存在，禁用按钮
                if not os.path.exists(tool_path):
                    button.state(['disabled'])
                    self.create_tooltip(button, f"工具文件不存在: {file_name}")
                else:
                    self.create_tooltip(button, f"启动{tool_name}")
                    
                button.pack(pady=2)
        
        # 状态栏
        self.status_var = tk.StringVar(value="就绪")
        self.status_bar = ttk.Label(self.root, textvariable=self.status_var, relief="sunken")
        self.status_bar.pack(side="bottom", fill="x", padx=10, pady=5)
        
    def refresh_tools(self):
        """刷新工具状态并更新界面"""
        # 更新状态
        self.status_var.set("正在刷新工具列表...")
        self.root.update()
        
        # 清除当前的工具列表框架
        for widget in self.root.winfo_children():
            if isinstance(widget, ttk.LabelFrame):
                widget.destroy()
                
        # 重新检查工具
        self.check_tools()
        
        # 重新创建工具列表框架
        frame = ttk.LabelFrame(self.root, text="可用工具", padding="10")
        frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # 重新创建工具按钮
        available_tools = 0
        total_tools = 0
        
        for category, tools in self.tools.items():
            # 添加分类标签
            ttk.Label(frame, text=f"{category}：", font=("", 10, "bold")).pack(anchor="w", pady=(10,0))
            
            # 添加工具按钮
            for tool_name, file_name in tools.items():
                total_tools += 1
                # 检查工具是否存在
                tool_path = os.path.join(os.path.dirname(__file__), file_name)
                button = ttk.Button(frame, text=tool_name, width=30,
                                  command=lambda f=file_name: self.run_tool(f))
                
                # 如果工具不存在，禁用按钮
                if not os.path.exists(tool_path):
                    button.state(['disabled'])
                    self.create_tooltip(button, f"工具文件不存在: {file_name}")
                else:
                    available_tools += 1
                    self.create_tooltip(button, f"启动{tool_name}")
                    
                button.pack(pady=2)
        
        # 更新状态栏
        self.status_var.set(f"刷新完成 - 可用工具: {available_tools}/{total_tools}")
        
    def create_tooltip(self, widget, text):
        """为控件创建工具提示"""
        def enter(event):
            x, y, _, _ = widget.bbox("insert")
            x += widget.winfo_rootx() + 25
            y += widget.winfo_rooty() + 25
            
            # 创建工具提示窗口
            self.tooltip = tk.Toplevel()
            self.tooltip.wm_overrideredirect(True)
            self.tooltip.wm_geometry(f"+{x}+{y}")
            
            label = ttk.Label(self.tooltip, text=text, background="#ffffe0", 
                            relief="solid", borderwidth=1)
            label.pack()
            
        def leave(event):
            if hasattr(self, 'tooltip'):
                self.tooltip.destroy()
                self.tooltip = None
                
        widget.bind('<Enter>', enter)
        widget.bind('<Leave>', leave)
        
    def run_tool(self, tool_name):
        """运行指定的工具"""
        try:
            # 获取工具的完整路径
            tool_path = os.path.join(os.path.dirname(__file__), tool_name)
            
            # 检查文件是否存在
            if not os.path.exists(tool_path):
                raise FileNotFoundError(f"找不到工具文件：{tool_name}")
            
            # 更新状态
            self.status_var.set(f"正在启动：{tool_name}")
            self.root.update()
            
            # 使用Python解释器运行工具
            subprocess.Popen([sys.executable, tool_path])
            
            # 更新状态
            self.status_var.set(f"已启动：{tool_name}")
            
        except Exception as e:
            self.status_var.set("启动失败！")
            messagebox.showerror("错误", f"工具启动失败：{str(e)}")
    
    def show_about(self):
        """显示关于信息"""
        about_text = """
三垣工具启动器 V1.0.0
这是一个用于启动各种三垣开发的小工具模块的程序，提供了统一的启动界面。
版本说明，本启动器为正式发布版本，但目前配套的工具模块均为Alphaha版本，可能存在未知bug。
本项目在部署完整的开发环境后，可以离线本地运行。
- 作者:叁垣伍瑞肆凶廿捌宿宿
- 联系方式:https://space.bilibili.com/556216088
- 版权:Apache-2.0 License
        """
        
        # 创建关于窗口
        about_window = tk.Toplevel(self.root)
        about_window.title("关于")
        about_window.geometry("400x300")
        about_window.resizable(False, False)
        
        # 添加图标标签（如果有的话）
        try:
            icon_path = os.path.join(os.path.dirname(__file__), 'icon.ico')
            if os.path.exists(icon_path):
                from PIL import Image, ImageTk
                icon = Image.open(icon_path)
                icon = icon.resize((64, 64), Image.Resampling.LANCZOS)
                icon_photo = ImageTk.PhotoImage(icon)
                icon_label = ttk.Label(about_window, image=icon_photo)
                icon_label.image = icon_photo  # 保持引用
                icon_label.pack(pady=10)
        except:
            pass
        
        # 添加关于文本
        text_widget = tk.Text(about_window, wrap="word", padx=20, pady=10, height=10)
        text_widget.pack(fill="both", expand=True)
        text_widget.insert("1.0", about_text)
        text_widget.config(state="disabled")  # 设置为只读
        
        # 添加关闭按钮
        close_button = ttk.Button(about_window, text="关闭", command=about_window.destroy)
        close_button.pack(pady=10)
        
    def show_help(self):
        """显示帮助信息"""
        help_text = """
工具启动器使用帮助

1. 功能说明
   本程序用于启动各种工具模块，包括PDF处理、图片处理和音频处理工具。

2. 使用方法
   - 在界面上选择需要使用的工具，点击对应按钮
   - 工具将在独立窗口中启动
   - 可以同时运行多个工具
   - 状态栏会显示工具的启动状态

3. 工具说明
   PDF工具：
   - PDF拆分：将PDF文件拆分为单页文件
   - PDF合并：将多个PDF文件合并为一个文件
   - PDF转Word：将PDF转换为Word文档并保留格式
   - PDF加水印：为PDF文件添加水印

   图片工具：
   - 九宫格分割：将图片分割为九宫格
   - 格式转换：转换图片格式
   - ICO转换：将图片转换为ICO图标
   - 图片合成：将多张图片合成为一张

   音频工具：
   - 音频提取：从视频文件中提取音频

4. 注意事项
   - 确保所有工具脚本与启动器在同一目录下
   - 部分工具可能需要额外的依赖库
   - 音频提取功能需要系统安装FFmpeg
        """
        
        # 创建帮助窗口
        help_window = tk.Toplevel(self.root)
        help_window.title("帮助")
        help_window.geometry("500x600")
        help_window.resizable(True, True)
        
        # 添加帮助文本
        text_widget = tk.Text(help_window, wrap="word", padx=10, pady=10)
        text_widget.pack(fill="both", expand=True)
        text_widget.insert("1.0", help_text)
        text_widget.config(state="disabled")  # 设置为只读
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(text_widget, command=text_widget.yview)
        scrollbar.pack(side="right", fill="y")
        text_widget.config(yscrollcommand=scrollbar.set)
        
        # 添加关闭按钮
        close_button = ttk.Button(help_window, text="关闭", command=help_window.destroy)
        close_button.pack(pady=10)
        
    def run(self):
        """运行启动器"""
        self.root.mainloop()

if __name__ == "__main__":
    app = ToolLauncher()
    app.run()