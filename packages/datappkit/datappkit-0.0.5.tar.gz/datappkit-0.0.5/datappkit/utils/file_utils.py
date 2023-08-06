import os
import sys


def read_file(filename, mode='r'):
    """
    读取文件内容
    @filename 文件名
    return string(bin) 若文件不存在，则返回None
    """
    if not os.path.exists(filename):
        return False
    try:
        fp = open(filename, mode)
        content = fp.read()
        fp.close()
    except Exception as ex:
        if sys.version_info[0] != 2:
            try:
                fp = open(filename, mode, encoding="utf-8")
                content = fp.read()
                fp.close()
            except:
                fp = open(filename, mode, encoding="GBK")
                content = fp.read()
                fp.close()
        else:
            return False
    return content


def write_file(filename, content, mode='w+'):
    """
    写入文件内容
    @filename 文件名
    @content 写入的内容
    return bool 若文件不存在则尝试自动创建
    """
    try:
        fp = open(filename, mode)
        fp.write(content)
        fp.close()
        return True
    except:
        try:
            fp = open(filename, mode, encoding="utf-8")
            fp.write(content)
            fp.close()
            return True
        except:
            return False
