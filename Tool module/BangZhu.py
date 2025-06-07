# 禁止生成 .pyc 文件
import sys
sys.dont_write_bytecode = True

import tkinter as tk
from tkinter import messagebox

class HelpSystem:
    """
    统一的帮助系统类，用于管理和显示所有模块的帮助内容。
    
    该类实现了以下功能：
    1. 集中管理所有模块的帮助文档
    2. 提供统一的帮助内容显示界面
    3. 自动附加统一的作者和版权信息
    4. 错误处理和默认帮助内容
    
    使用示例：
    help_system = HelpSystem()
    help_system.show_help("pdf_splitter")
    """
    # 统一的作者信息、联系方式和版权声明
    AUTHOR_INFO = """
提示：
如果发现发现Bug或需要新的功能，请联系作者：
- 作者:宁幻雪(叁垣伍瑞肆凶廿捌宿宿)
- 联系方式:https://space.bilibili.com/556216088
- 版权:Apache-2.0 License
"""
    def __init__(self):
        self.help_contents = {
# PDF工具帮助内容合集
    # PDF拆分帮助内容
    "PDF拆分": 
"""
PDF拆分工具使用帮助
功能说明：
- 支持PDF文件拆分功能
- 可以选择拆分的页面范围
使用步骤：
1. 点击"选择文件"选择要拆分的PDF文件
2. 在拆分选项框中选择按页拆分还是按范围拆分
3. 点击"开始拆分"按钮进行处理
""",
# PDF合并帮助内容
                        "PDF合并":
"""
PDF合并工具使用帮助
功能说明：
- 支持多个PDF文件合并
使用步骤：
1. 点击"添加文件"按钮选择要合并的PDF文件
2. 选择那些哪些页面需要合并
3. 点击"开始合并"按钮进行处理
""",
# PDF转图片帮助内容
                        "PDF转图片":
"""
PDF转图片工具使用帮助
功能说明：
- 支持将PDF文件转换为多种图片格式
- 支持PNG/JPEG/TIFF/BMP输出格式
- 可调整DPI和质量设置
- 支持页面预览和选择
使用步骤：
1. 点击"选择PDF文件"按钮或直接将PDF文件拖放到窗口
2. 选择输出目录
3. 设置转换选项:
   - 输出格式: PNG/JPEG/TIFF/BMP
   - DPI: 控制输出图片的分辨率(72-600)
   - JPEG质量: 仅对JPEG格式有效(1-100)
4. 选择要转换的页面 - 默认转换所有页面
5. 点击"开始转换"按钮开始转换
""",

# 图片转PDF帮助内容
                        "图片转PDF":
"""
1. 添加图片 - 点击"添加图片"按钮选择一张或多张图片
2. 选择输出PDF - 点击"选择输出PDF"按钮指定保存位置
3. 管理图片列表:
   - 右键点击图片可移除选中项
   - 点击"清空列表"可移除所有图片
4. 点击"开始转换"按钮开始转换
5. 转换完成后会自动打开输出文件夹
""",

# PDF转Word帮助内容
                        "PDF转Word":
"""
1. 点击"选择PDF"按钮选择要转换的PDF文件
2. 点击"转换为Word"按钮开始转换
3. 选择保存位置和文件名
        
注意: 
- 转换时间取决于PDF文件大小
- 转换过程中请勿关闭程序
""",

# PDF加水印帮助内容
                        "PDF加水印":
"""
PDF加水印工具使用帮助
功能说明：
- 支持为PDF文件添加文字水印
- 可自定义水印文字、大小、透明度和位置
使用步骤：
1. 点击"选择PDF"按钮选择要加水印的PDF文件
2. 设置水印选项:
   - 水印文字: 输入要显示的文字
   - 字体大小: 调整水印文字大小
   - 透明度: 调整水印透明度
   - 位置: 选择水印在页面中的位置
3. 点击"添加水印"按钮开始处理
4. 选择保存位置和文件名
""",








            # 其他工具帮助内容可以继续添加...
        }

    def show_help(self, module_id: str) -> None:
        """
        显示指定模块的帮助内容。
        
        该方法会：
        1. 通过get_help_content获取帮助文本
        2. 在独立的消息框中显示帮助内容
        3. 自动处理异常情况

        Args:
            module_id (str): 模块的唯一标识符，应与help_contents中的键匹配

        Returns:
            None

        Raises:
            捕获所有异常并通过消息框显示错误信息
        """
        try:
            # 获取格式化后的帮助内容
            help_content = self.get_help_content(module_id)
            # 显示在独立的消息框中，标题自动转换为友好格式
            messagebox.showinfo(
                f"{module_id.replace('_', ' ').title()} 帮助", 
                help_content
            )
        except Exception as e:
            # 异常处理，显示错误详情
            messagebox.showerror("错误", f"显示帮助内容时出错：{str(e)}")

    def get_help_content(self, module_id: str) -> str:
        """
        获取指定模块的帮助内容。
        
        该方法会：
        1. 检查模块ID是否存在
        2. 返回对应帮助内容并自动附加作者信息
        3. 模块不存在时返回默认帮助

        Args:
            module_id (str): 模块的唯一标识符，必须与help_contents字典键匹配

        Returns:
            str: 完整的帮助内容文本(模块帮助+作者信息)

        Raises:
            KeyError: 当指定的模块ID不存在时(内部处理，不向外抛出)
        """
        if module_id in self.help_contents:
            # 返回模块特定帮助内容并附加统一作者信息
            return self.help_contents[module_id] + self.AUTHOR_INFO
        # 模块ID不存在时返回默认帮助
        return self._get_default_help()

    def _get_default_help(self) -> str:
        """
        获取默认的帮助内容。
        
        当请求的模块帮助不存在时，返回默认帮助内容。

        Returns:
            str: 仅包含作者信息的默认帮助内容
        """
        return self.AUTHOR_INFO

# 创建全局帮助系统实例
help_system = HelpSystem()

def get_help_system() -> HelpSystem:
    """
    获取全局帮助系统实例。
    
    通过单例模式提供全局唯一的帮助系统实例，
    确保整个应用程序使用同一套帮助内容。

    Returns:
        HelpSystem: 全局唯一的帮助系统实例
    """
    return help_system

# 使用示例：
if __name__ == "__main__":
    # 创建测试窗口
    root = tk.Tk()
    root.title("帮助系统测试")
    
    # 获取帮助系统实例
    help_sys = get_help_system()
    
    # 创建测试按钮
    def show_pdf_help():
        help_sys.show_help("pdf_splitter")
    
    def show_image_help():
        help_sys.show_help("image_converter")
    
    def show_audio_help():
        help_sys.show_help("audio_extractor")
    
    def show_invalid_help():
        help_sys.show_help("invalid_module")
    
    # 添加测试按钮
    tk.Button(root, text="显示PDF拆分帮助", command=show_pdf_help).pack(pady=5)
    tk.Button(root, text="显示图片转换帮助", command=show_image_help).pack(pady=5)
    tk.Button(root, text="显示音频提取帮助", command=show_audio_help).pack(pady=5)
    tk.Button(root, text="测试无效模块", command=show_invalid_help).pack(pady=5)
    
    # 运行测试窗口
    root.mainloop()