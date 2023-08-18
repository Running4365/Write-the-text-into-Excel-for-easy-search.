
import re
import time
import os
import requests  

def gen_timestamp(file_name, suffix='txt'):
    """
        generate timestamp
    """
    return '{}_{}.{}'.format(file_name, time.strftime("%y%m%d%H%M%S", time.localtime()), suffix)


def find_all_file(base):
    """
    Traverse all files in a folder and output its absolute file path

    Usage:
        file_list = find_all_file('.')
        for i in file_list:
            print(i)
    """
    for root, ds, fs in os.walk(base):
        for f in fs:
            fullname = os.path.join(root, f)
            yield fullname


def remove_chinese(p1):
    #去除中文，防止CSV文件中有中文而乱码
    # p1='帮会建了徽信群 没在群里的加下徽信:[30109552300]，晚上群里有活动通知大家，(抢资源)，争地盘，谢谢配合。i love you '
    linee=re.sub('[\u4e00-\u9fa5]', '', p1)
    return linee


def get_webpage(url):
    """
        返回网页内容
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    response.encoding = response.apparent_encoding # 自动识别编码
    # print(response.text)
    return response.text


def get_file_name(file_path):
    """
        示例路径：D:\Py\22_write_text_into_excel_for_easy_search\19_dds\dds\dds.srcs\sources_1\new\key_control.v
        返回：key_control.v
    """
    return file_path.split('\\')[-1]


def get_filename(file_path):
    '''
    os.path.split('PATH')
    1.PATH指一个文件的全路径作为参数：
    2.如果给出的是一个目录和文件名，则输出路径和文件名
    3.如果给出的是一个目录名，则输出路径和为空文件名
    '''
    path,name = os.path.split(file_path)
    return name 