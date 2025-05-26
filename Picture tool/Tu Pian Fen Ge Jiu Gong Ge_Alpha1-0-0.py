from PIL import Image
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

class ImageSplitterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("图片九宫格分割工具Alpha1.0.0")
        
        # 输入图片
        tk.Label(root, text="输入图片:").grid(row=0, column=0, padx=5, pady=5)
        self.input_entry = tk.Entry(root, width=40)
        self.input_entry.grid(row=0, column=1, padx=5, pady=5)
        tk.Button(root, text="浏览...", command=self.browse_input).grid(row=0, column=2, padx=5, pady=5)
        
        # 输出目录
        tk.Label(root, text="输出目录:").grid(row=1, column=0, padx=5, pady=5)
        self.output_entry = tk.Entry(root, width=40)
        self.output_entry.grid(row=1, column=1, padx=5, pady=5)
        tk.Button(root, text="浏览...", command=self.browse_output).grid(row=1, column=2, padx=5, pady=5)
        
        # 进度条
        self.progress = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
        self.progress.grid(row=2, column=0, columnspan=3, padx=5, pady=10)
        
        # 分割按钮和帮助按钮
        tk.Button(root, text="开始分割", command=self.start_split).grid(row=3, column=1, pady=10)
        tk.Button(root, text="帮助", command=self.show_help).grid(row=3, column=0, pady=10, padx=5)
    
    def show_help(self):
        help_text = """图片九宫格分割工具使用说明
        
1. 点击"浏览..."按钮选择要分割的图片
2. 点击"浏览..."按钮选择输出目录
3. 点击"开始分割"按钮进行分割
4. 分割完成后，将在输出目录下创建一个以图片名命名的文件夹

提示:
- 作者:叁垣伍瑞肆凶廿捌宿宿
- 联系方式:https://space.bilibili.com/556216088
- 版权:Apache-2.0 License
"""
        messagebox.showinfo("帮助", help_text)
    
    def browse_input(self):
        filepath = filedialog.askopenfilename(
            filetypes=[("图片文件", "*.jpg *.jpeg *.png *.bmp *.gif")]
        )
        if filepath:
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, filepath)
    
    def browse_output(self):
        dirpath = filedialog.askdirectory()
        if dirpath:
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, dirpath)
    
    def start_split(self):
        input_path = self.input_entry.get()
        output_dir = self.output_entry.get()
        
        if not input_path or not output_dir:
            messagebox.showerror("错误", "请选择输入图片和输出目录")
            return
        
        try:
            self.progress["value"] = 0
            self.root.update()
            
            # 获取输入文件名(不带扩展名)
            base_name = os.path.splitext(os.path.basename(input_path))[0]
            # 创建子文件夹路径
            save_dir = os.path.join(output_dir, base_name + "_split")
            
            # 确保输出目录存在
            os.makedirs(save_dir, exist_ok=True)
            
            # 打开图片
            with Image.open(input_path) as img:
                width, height = img.size
                
                # 计算每个小块的尺寸
                tile_width = width // 3
                tile_height = height // 3
                
                # 分割图片
                total = 9
                for i in range(3):
                    for j in range(3):
                        left = j * tile_width
                        upper = i * tile_height
                        right = left + tile_width
                        lower = upper + tile_height
                        
                        # 裁剪图片
                        tile = img.crop((left, upper, right, lower))
                        
                        # 保存小块
                        tile.save(os.path.join(save_dir, f'{base_name}_tile_{i}_{j}.png'))
                        
                        # 更新进度
                        self.progress["value"] = ((i * 3) + j + 1) / total * 100
                        self.root.update()
            
            messagebox.showinfo("完成", f"图片已成功分割为9份，保存在 {save_dir}")
            self.progress["value"] = 0
        
        except Exception as e:
            messagebox.showerror("错误", f"处理图片时出错: {e}")
            self.progress["value"] = 0

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageSplitterApp(root)
    root.mainloop()
