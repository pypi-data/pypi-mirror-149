import os
from enum import Enum, unique

from jinja2 import Environment, FileSystemLoader, select_autoescape

from .. import Generator


# Keil5 版本定义
@unique
class Keil5VersionType(Enum):
    V5 = 1      # Keil V5.x   （低于 V5.27）
    V5_27 = 2   # Keil V5.27+ （包括 V5.27）


class Keil5Generator(Generator):
    # Jinja2环境
    __env = Environment(
        loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')),
        autoescape=select_autoescape(),
        trim_blocks=True,
        lstrip_blocks=True,
    )

    # 生成工程接口
    def project_generator(self, prj_info, target_info, prj_path, version: Keil5VersionType):
        # --------------------- 路径处理 -----------------------
        # 项目文件路径
        prj_file_path = os.path.join(prj_path, 'MDK-ARM')

        # 检查路径是否存在
        if not os.path.exists(prj_file_path):
            os.mkdir(prj_file_path)

        # ----------- 检查工程文件是否需要修改target配置 -----------
        # 检查工程是否需要添加额外的烧写配置文件
        if prj_info['advanced_options']['keil_flasher_cfg'] is not None:
            target_info['keil_5_flash_algorithms'].extend(prj_info['advanced_options']['keil_flasher_cfg'])

        # -------------------- 生成工程文件 ---------------------
        # KEIL 5
        if version == Keil5VersionType.V5:
            # KEIL 5 工程文件(*.uvprojx)
            tpl = self.__env.get_template('keil_5_uvprojx.xml')
            uvprojx_name = prj_info['name'] + ".uvprojx"
            f = open(os.path.join(prj_file_path, uvprojx_name), mode='w')
            f.write(tpl.render(project=prj_info, target=target_info))
            f.close()

            # KEIL 5 工程选项文件(*.uvoptx)
            tpl = self.__env.get_template('keil_5_uvoptx.xml')
            uvoptx_name = prj_info['name'] + ".uvoptx"
            f = open(os.path.join(prj_file_path, uvoptx_name), mode='w')
            f.write(tpl.render(project=prj_info, target=target_info))
            f.close()

            # KEIL 5 JLink 配置文件(JLinkSettings.ini)
            if str.lower(prj_info['debug']['tool']) == 'jlink':
                tpl = self.__env.get_template('keil_5_jlink_setting.ini')
                f = open(os.path.join(prj_file_path, 'JLinkSettings.ini'), mode='w')
                f.write(tpl.render(target=target_info))
                f.close()

        # KEIL 5.27
        elif version == Keil5VersionType.V5_27:
            # KEIL 5.27 工程文件(*.uvprojx)
            tpl = self.__env.get_template('keil_5_27_uvprojx.xml')
            uvprojx_name = prj_info['name'] + ".uvprojx"
            f = open(os.path.join(prj_file_path, uvprojx_name), mode='w')
            f.write(tpl.render(project=prj_info, target=target_info))
            f.close()

            # KEIL 5.27 工程选项文件(*.uvoptx)
            tpl = self.__env.get_template('keil_5_27_uvoptx.xml')
            uvoptx_name = prj_info['name'] + ".uvoptx"
            f = open(os.path.join(prj_file_path, uvoptx_name), mode='w')
            f.write(tpl.render(project=prj_info, target=target_info))
            f.close()

            # KEIL 5.27 JLink 配置文件(JLinkSettings.ini)
            if str.lower(prj_info['debug']['tool']) == 'jlink':
                tpl = self.__env.get_template('keil_5_27_jlink_setting.ini')
                f = open(os.path.join(prj_file_path, 'JLinkSettings.ini'), mode='w')
                f.write(tpl.render(target=target_info))
                f.close()
