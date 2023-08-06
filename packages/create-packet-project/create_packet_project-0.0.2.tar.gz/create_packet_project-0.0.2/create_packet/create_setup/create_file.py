"""
自动创建资源包文件
"""
import os
from datetime import datetime


class CreateProject(object):
    """
    创建一个资源包项目
    """

    def __init__(self, project_path: str, project_folder_name: str):
        self.project_path = project_path  # 项目的父级路径
        self.project_folder_name = project_folder_name  # 项目名称
        self.project_folder_path = os.path.join(
            self.project_path, self.project_folder_name
        )  # 项目根目录

    def _create_project_folder(self):
        """创建项目文件夹
        要求这个文件夹必须是空的
        """
        # 如果目标文件夹下有文件存在，会抛出错误
        if not os.path.exists(self.project_folder_path):
            os.mkdir(self.project_folder_path)
        else:
            if os.listdir(self.project_folder_path):
                raise Exception("项目文件夹必须为空")

    def _create_license_file(self, *, default: bool = True):
        """创建许可证文件
        支持自动生成， 也可以自己去获取
        Args:
            default: 是否使用默认许可证
        """
        license_path = os.path.join(self.project_folder_path, "LICENSE")
        if not default:
            with open(license_path, "w", encoding="utf-8") as fh:
                license_url = "许可证获取地址: https://choosealicense.com/"
                fh.write(license_url)
        else:
            content = self.__license_content()
            with open(license_path, "w", encoding="utf-8") as fh:
                fh.write(content)

    def __license_content(self):
        """证书内容
        只需要替换里面的内容即可
        """
        year = datetime.now().year
        content = f"""MIT License

Copyright (c) {year} {self.project_folder_name}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
        """
        return content

    def _create_readme_file(self):
        """创建README.md文件

        创建资源包的描述文件，在这个文件中存放对资源包的描述，以及使用方法
        """
        with open(f"{self.project_folder_path}/README.md", "w", encoding="utf-8") as fh:
            fh.write("这里写对文件的描述和资源包的详细用法")

    def _create_setup_file(self):
        """创建setup.py模板文件
        创建文件，生成一些必要的字段，只需要填写对应的字段值，无需关心
        """
        with open(f"{self.project_folder_path}/setup.py", "w", encoding="utf-8") as fp, \
                open('create_packet/create_setup/setup_template.py', "r", encoding="utf-8") as fh:
            fp.write(fh.read())

    def _create_packet_folder(self):
        """创建python包文件夹
        """
        packet_path = os.path.join(self.project_folder_path, self.project_folder_name)
        os.mkdir(packet_path)
        with open(f"{packet_path}/__init__.py", "w", encoding="utf-8") as fp:
            fp.write("")

    def main_func(self, use_default_license: bool = True):
        """主函数

        Args:
            use_default_license: 是否使用默认证书
        """
        # 创建项目路径
        self._create_project_folder()
        # 包的证书
        self._create_license_file(default=use_default_license)
        # 创建readme.md文件
        self._create_readme_file()
        # 创建setup.py文件
        self._create_setup_file()
        # 创建包文件夹
        self._create_packet_folder()


def create_project(project_path: str, project_folder_name: str, *, use_default_license: bool = True):
    """提供给外部使用，用来创建资源包项目框架

    Args:
        project_path: 项目的父级路径
        project_folder_name: 项目的文件夹名称
        use_default_license: 是否使用默认的证书，必须使用关键字传参

    Returns:

    """
    func_obj = CreateProject(project_path, project_folder_name)
    func_obj.main_func(use_default_license)


if __name__ == "__main__":
    create_project(r"D:\Desktop\packet", "add_num")
