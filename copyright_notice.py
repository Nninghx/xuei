import tkinter as tk
from tkinter import messagebox, scrolledtext

class CopyrightNotice:
    def __init__(self, root):
        self.root = root
        self.root.title("版权声明")
        self.root.geometry("500x400")
        
        # 主框架
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 版权声明文本区域（带滚动条）
        self.text_area = scrolledtext.ScrolledText(
            self.main_frame,
            wrap=tk.WORD,
            font=("Arial", 11),
            padx=10,
            pady=10,
            height=15  # 限制文本区域高度
        )
        self.text_area.pack(fill=tk.BOTH, expand=True)
        
        # 设置文本内容
        notice_text = """版权声明与开源协议声明
版权所有：宁幻雪 © 2025
作者：宁幻雪（Bilibili账号：叁垣伍瑞肆凶廿捌宿）
开源协议：本软件及其相关文档采用 Apache License 2.0 开源协议
使用许可条款
版权与许可证声明
除非遵守 Apache-2.0 许可证条款，否则不得使用本文件。
您可通过下方链接获取许可证全文，或直接访问：
http://www.apache.org/licenses/LICENSE-2.0
免责声明
本软件按“原样”分发，不附带任何明示或暗示的保证或条件。
作者不对软件的功能、稳定性或兼容性提供任何形式的担保。
作者不对任何因使用本软件而导致的直接或间接损失负责。
作者保留对本软件进行修改、更新和维护的权利。
商业或个人使用建议
虽然 Apache-2.0允许商业用途，但作者不鼓励直接使用原版进行商业部署或使用。请先进行评估和测试，以确保您的使用符合您的需求。
由于本项目处于持续开发阶段，可能存在未发现的BUG或兼容性问题。
如果在使用中发现bug或其他问题，请及时反馈给作者。便于作者及时修复问题。
Bilibili主页：https://space.bilibili.com/556216088

"""
        self.text_area.insert(tk.END, notice_text)
        self.text_area.config(state=tk.DISABLED)  # 设置为只读
        
        # 按钮框架
        self.button_frame = tk.Frame(self.main_frame)
        self.button_frame.pack(fill=tk.X, pady=20)  # 增加按钮上下间距
        
        # 确认按钮
        self.button = tk.Button(
            self.button_frame,
            text="我已阅读并同意",
            command=self.on_agree,
            width=15,
            height=2
        )
        self.button.pack()
    
    def on_agree(self):
        messagebox.showinfo("确认", "您已同意")
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = CopyrightNotice(root)
    root.mainloop()
