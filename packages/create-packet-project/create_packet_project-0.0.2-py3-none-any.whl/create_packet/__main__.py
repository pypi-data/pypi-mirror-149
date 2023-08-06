# _*_ coding:utf-8 _*_
# ------------------------
# @Author   :    Jack    -
# @Time     : 2022-05-05 -
#  敲的是字母, 码的是人生    -
# ------------------------
import click
from create_packet.create_setup.create_file import create_project


@click.command()
@click.option('--path', help="项目路径", required=True)
@click.option("--name", help="项目名称", required=True)
@click.option("--default", default=True, help="是否使用默认证书")
def create(path, name, default=True):
    create_project(path, name, use_default_license=default)
    click.echo("文件生成成功")


if __name__ == '__main__':
    create()
