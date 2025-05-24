import os
import sys
import threading
from queue import Queue
from datetime import datetime
from PIL import Image
from tkinter import Tk, filedialog, messagebox, StringVar, OptionMenu, IntVar
from tkinter.ttk import Frame, Button, Label, Entry, Checkbutton, Radiobutton, Progressbar, Separator

class ImageConverter:
    SUPPORTED_FORMATS = [
        'jpg', 'jpeg', 'png', 'webp', 
        'bmp', 'gif', 'tiff', 'psd'
    ]
    
    def __init__(self):
        self.root = Tk()
        self.root.title("图片格式转换工具")
        
        # 设置窗口图标
        try:
            icon_path = os.path.join(os.path.dirname(__file__), 'icon.ico')
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
        except:
            pass
            
        self.task_queue = Queue()
        self.running = False
        self.status_var = StringVar()
        
        self.setup_ui()
        
    def setup_ui(self):
        # 主框架
        main_frame = Frame(self.root, padding="10")
        main_frame.pack(fill='both', expand=True)
        
        # 模式选择
        Label(main_frame, text="转换模式:").grid(row=0, column=0, sticky='w')
        self.mode_var = StringVar(value='single')
        Frame(main_frame).grid(row=0, column=1, sticky='w')  # 占位用
        
        # 单文件模式组件
        single_frame = Frame(main_frame)
        single_frame.grid(row=1, column=0, columnspan=3, sticky='ew')
        Label(single_frame, text="单文件:").grid(row=0, column=0, sticky='w')
        self.input_entry = Entry(single_frame, width=40)
        self.input_entry.grid(row=0, column=1)
        Button(single_frame, text="浏览...", command=self.select_input).grid(row=0, column=2)
        
        # 批量模式组件
        batch_frame = Frame(main_frame)
        batch_frame.grid(row=2, column=0, columnspan=3, sticky='ew')
        Label(batch_frame, text="批量目录:").grid(row=0, column=0, sticky='w')
        self.batch_entry = Entry(batch_frame, width=40)
        self.batch_entry.grid(row=0, column=1)
        Button(batch_frame, text="浏览...", command=self.select_batch).grid(row=0, column=2)
        
        # 输出格式选择
        Label(main_frame, text="输出格式:").grid(row=3, column=0, sticky='w')
        self.format_var = StringVar(value='png')
        OptionMenu(main_frame, self.format_var, *self.SUPPORTED_FORMATS).grid(row=3, column=1, sticky='w')
        
        # 质量设置
        Label(main_frame, text="输出质量 (1-100):").grid(row=4, column=0, sticky='w')
        self.quality_var = IntVar(value=100)
        quality_entry = Entry(main_frame, textvariable=self.quality_var, width=5)
        quality_entry.grid(row=4, column=1, sticky='w')
        
        # 分隔线
        Separator(main_frame, orient='horizontal').grid(row=5, column=0, columnspan=3, sticky='ew', pady=5)
        
        # 输出目录选择
        Label(main_frame, text="输出目录:").grid(row=6, column=0, sticky='w')
        self.output_entry = Entry(main_frame, width=40)
        self.output_entry.grid(row=6, column=1)
        Button(main_frame, text="浏览...", command=self.select_output).grid(row=6, column=2)
        
        # 进度条
        self.progress = Progressbar(main_frame, orient="horizontal", length=200, mode="determinate")
        self.progress.grid(row=7, column=0, columnspan=2, pady=10, sticky='ew')
        
        # 操作按钮框架
        button_frame = Frame(main_frame)
        button_frame.grid(row=7, column=0, columnspan=3, pady=10, sticky='ew')
        
        # 帮助按钮
        Button(button_frame, text="帮助", command=self.show_help).pack(side='left', padx=5)
        
        # 转换按钮
        Button(button_frame, text="转换", command=self.start_conversion).pack(side='right', padx=5)
        
        # 状态标签
        self.status_var = StringVar(value="就绪")
        Label(main_frame, textvariable=self.status_var).grid(row=8, column=0, columnspan=3, sticky='w')
        
        # 模式切换
        self.mode_var.trace('w', self.toggle_mode)
        Radiobutton(main_frame, text="单文件模式", variable=self.mode_var, value='single').grid(row=0, column=1, sticky='w')
        Radiobutton(main_frame, text="批量模式", variable=self.mode_var, value='batch').grid(row=0, column=2, sticky='w')
        
    def toggle_mode(self, *args):
        if self.mode_var.get() == 'single':
            self.input_entry.config(state='normal')
            self.batch_entry.config(state='disabled')
        else:
            self.input_entry.config(state='disabled')
            self.batch_entry.config(state='normal')
    
    def select_batch(self):
        dirpath = filedialog.askdirectory(title="选择图片目录")
        if dirpath:
            self.batch_entry.delete(0, 'end')
            self.batch_entry.insert(0, dirpath)
            
    def select_output(self):
        dirpath = filedialog.askdirectory(title="选择输出目录")
        if dirpath:
            self.output_entry.delete(0, 'end')
            self.output_entry.insert(0, dirpath)
        
    def select_input(self):
        filepath = filedialog.askopenfilename(
            title="选择图片文件",
            filetypes=[("图片文件", "*.jpg;*.jpeg;*.png;*.webp;*.bmp;*.gif;*.tiff;*.psd")]
        )
        if filepath:
            self.input_entry.delete(0, 'end')
            self.input_entry.insert(0, filepath)
    
    def start_conversion(self):
        """启动转换线程"""
        if self.running:
            return
            
        self.running = True
        self.progress['value'] = 0
        self.status_var.set("转换中...")
        threading.Thread(target=self.convert, daemon=True).start()
        
    def convert_single_image(self, input_path, output_path, output_format):
        """转换单个图片"""
        try:
            # 检查输出文件是否已存在
            if os.path.exists(output_path):
                if not messagebox.askyesno("确认", f"文件 {os.path.basename(output_path)} 已存在，是否覆盖？"):
                    return "用户取消操作"
            
            quality = max(1, min(100, self.quality_var.get()))
            img = Image.open(input_path)
            
            # 根据格式设置保存参数
            save_args = {'format': output_format.upper()}
            if output_format.lower() in ['jpg', 'jpeg', 'webp']:
                save_args['quality'] = quality
            elif output_format.lower() == 'png':
                save_args['compress_level'] = 9 - int(quality / 11.11)  # 将1-100映射到9-0
            
            img.save(output_path, **save_args)
            return True
            
        except IOError as e:
            error_msg = f"文件读写错误: {str(e)}"
            return error_msg
        except Image.DecompressionBombError:
            error_msg = "图片尺寸过大，可能造成内存溢出"
            return error_msg
        except Exception as e:
            error_msg = f"未知错误: {str(e)}"
            return error_msg
    
    def update_progress(self, value):
        """更新进度条"""
        self.progress['value'] = value
        self.root.update_idletasks()
        
    def show_help(self):
        """显示帮助信息"""
        help_text = """图片格式转换工具 使用说明

1. 选择转换模式:
   - 单文件模式: 转换单个图片文件
   - 批量模式: 转换整个目录中的图片

2. 设置输出格式和质量:
   - 从下拉列表中选择输出格式
   - 输入1-100的质量值(数值越大质量越好)

3. 设置输出目录:
   - 可以指定输出目录或单独选择每个文件的保存位置

4. 点击"转换"按钮开始转换
   - 批量转换时会显示进度条
   - 转换结果会显示在状态栏

注意:
- 支持格式: JPG, PNG, WEBP, BMP, GIF, TIFF, PSD
- 高质量设置会生成更大的文件 

提示:
- 作者:叁垣伍瑞肆凶廿捌宿宿
- 联系方式:https://space.bilibili.com/556216088
- 版权:Apache-2.0 License


"""
        messagebox.showinfo("帮助", help_text)
        
    def convert(self):
        """主转换逻辑"""
        output_format = self.format_var.get()
        output_dir = self.output_entry.get()
        
        if self.mode_var.get() == 'single':
            input_path = self.input_entry.get()
            if not input_path:
                messagebox.showerror("错误", "请先选择输入文件")
                self.running = False
                return
                
            if not output_dir:
                output_path = filedialog.asksaveasfilename(
                    title="保存为",
                    defaultextension=f".{output_format}",
                    filetypes=[(f"{output_format.upper()} 文件", f"*.{output_format}")]
                )
            else:
                filename = os.path.basename(input_path)
                name, ext = os.path.splitext(filename)
                output_path = os.path.join(output_dir, f"{name}.{output_format}")
                
            if output_path:
                result = self.convert_single_image(input_path, output_path, output_format)
                if result is True:
                    self.status_var.set("转换完成！")
                    messagebox.showinfo("成功", "图片转换完成！")
                else:
                    messagebox.showerror("错误", result)
        else:
            input_dir = self.batch_entry.get()
            if not input_dir:
                messagebox.showerror("错误", "请先选择输入目录")
                self.running = False
                return
                
            if not output_dir:
                messagebox.showerror("错误", "请先选择输出目录")
                self.running = False
                return
                
            try:
                # 收集所有图片文件
                image_files = [
                    f for f in os.listdir(input_dir) 
                    if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.bmp', '.gif', '.tiff', '.psd'))
                ]
                
                total = len(image_files)
                if total == 0:
                    messagebox.showwarning("警告", "指定目录中没有找到支持的图片文件")
                    self.running = False
                    return
                    
                self.progress['maximum'] = total
                
                # 处理每个文件
                success_count = 0
                for i, filename in enumerate(image_files):
                    input_path = os.path.join(input_dir, filename)
                    name, ext = os.path.splitext(filename)
                    output_path = os.path.join(output_dir, f"{name}.{output_format}")
                    
                    result = self.convert_single_image(input_path, output_path, output_format)
                    if result is True:
                        success_count += 1
                    
                    self.update_progress(i + 1)
                
                self.status_var.set(f"批量转换完成 - 成功: {success_count}, 失败: {total - success_count}")
                messagebox.showinfo("完成", 
                    f"批量转换完成！\n成功: {success_count}\n失败: {total - success_count}")
                    
            except Exception as e:
                messagebox.showerror("错误", f"批量转换失败: {str(e)}")
                
        self.running = False

if __name__ == "__main__":
    converter = ImageConverter()
    converter.root.mainloop()
