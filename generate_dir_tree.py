import os
from tkinter import *
from tkinter import filedialog, messagebox
import os

def generate_dir_tree(path='.', ignore=None, prefix=''):
    if ignore is None:
        ignore = []
    try:
        items = sorted(os.listdir(path))
    except PermissionError:
        return f"无法访问 {path}：权限不足\n"
    result = ""
    for i, item in enumerate(items):
        if item in ignore:
            continue
        full_path = os.path.join(path, item)
        is_last = i == len(items) - 1
        # 添加当前项到结果
        result += prefix + ('└── ' if is_last else '├── ') + item + '\n'
        # 如果是目录，递归处理
        if os.path.isdir(full_path):
            new_prefix = prefix + ('    ' if is_last else '│   ')
            result += generate_dir_tree(full_path, ignore, new_prefix)
    return result
class DirTreeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("目录树生成器Alpha1.0.0")
        # 设置窗口大小并居中显示
        window_width = 800
        window_height = 600
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.create_widgets()
    def create_widgets(self):
        # 目录选择框架
        dir_frame = Frame(self.root)
        dir_frame.pack(pady=10, padx=10, fill=X)
        self.dir_entry = Entry(dir_frame, font=('Arial', 12))
        self.dir_entry.pack(side=LEFT, expand=True, fill=X)
        browse_btn = Button(dir_frame, text="浏览", command=self.browse_directory, width=8)
        browse_btn.pack(side=LEFT, padx=5)
        # 按钮框架
        btn_frame = Frame(self.root)
        btn_frame.pack(pady=10)
        generate_btn = Button(btn_frame, text="生成目录树", command=self.generate_tree, width=15, font=('Arial', 12))
        generate_btn.pack(side=LEFT, padx=5)
        save_btn = Button(btn_frame, text="保存结果", command=self.save_result, width=10, font=('Arial', 12))
        save_btn.pack(side=LEFT, padx=5)
        clear_btn = Button(btn_frame, text="清空", command=self.clear_output, width=10, font=('Arial', 12))
        clear_btn.pack(side=LEFT, padx=5)
        help_btn = Button(btn_frame, text="帮助", command=self.show_help, width=8, font=('Arial', 12))
        help_btn.pack(side=LEFT, padx=5)
        # 输出框架
        output_frame = Frame(self.root)
        output_frame.pack(pady=10, padx=10, fill=BOTH, expand=True)
        # 创建带滚动条的文本框
        output_scrollbar = Scrollbar(output_frame)
        output_scrollbar.pack(side=RIGHT, fill=Y)
        self.output_text = Text(output_frame, wrap=NONE, yscrollcommand=output_scrollbar.set, font=('Courier New', 10))
        self.output_text.pack(side=LEFT, fill=BOTH, expand=True)
        output_scrollbar.config(command=self.output_text.yview)
    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.dir_entry.delete(0, END)
            self.dir_entry.insert(0, directory)
    def generate_tree(self):
        directory = self.dir_entry.get()
        if not os.path.isdir(directory):
            self.output_text.delete('1.0', END)
            self.output_text.insert(END, "请输入有效的目录路径")
            return
        self.output_text.delete('1.0', END)
        ignore_list = ['.git', '__pycache__', '.DS_Store']
        result = generate_dir_tree(directory, ignore=ignore_list)
        self.output_text.insert(END, f"目录结构（忽略: {', '.join(ignore_list)}）:\n\n")
        self.output_text.insert(END, result)
    def save_result(self):
        result = self.output_text.get('1.0', END)
        if not result.strip():
            messagebox.showwarning("警告", "没有可保存的内容")
            return
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("文本文件", ".txt"), ("所有文件", ".*")]
        )
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(result)
                messagebox.showinfo("成功", "结果已保存")
            except Exception as e:
                messagebox.showerror("错误", f"保存文件时出错: {str(e)}")
    def clear_output(self):
        self.output_text.delete('1.0', END)
        self.dir_entry.delete(0, END)
    def show_help(self):
        help_text = """
        ==== 使用说明 ====
1. 浏览按钮：点击后可以选择要分析的目录
2. 生成目录树按钮：根据所选目录生成文件结构图
3. 保存结果按钮：将当前显示的目录结构保存到文件
4. 清空按钮：清除输入框和输出区域的内容
5. 默认忽略文件：.git、__pycache__、.DS_Store 等常见开发文件/目录
        ==== 注意事项 ====   
1. 大型目录可能需要较长时间生成结构图
2. 保存文件使用.txt扩展名
          ==== 提示 ====      
- 作者:叁垣伍瑞肆凶廿捌宿宿
- 联系方式:https://space.bilibili.com/556216088
- 版权:Apache-2.0 License
        """
        messagebox.showinfo("帮助文档", help_text.strip())
if __name__ == '__main__':
    root = Tk()
    app = DirTreeGUI(root)
    root.mainloop()
