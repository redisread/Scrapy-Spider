import time
from multiprocessing import Pool
import os
import json

from win32file import CreateFile, SetFileTime, GetFileTime, CloseHandle
from win32file import GENERIC_READ, GENERIC_WRITE, OPEN_EXISTING
from pywintypes import Time  # 可以忽视这个 Time 报错（运行程序还是没问题的）
import time
from os.path import join

MARKDOWN_DIR = 'weixin_DM'

# 修改文件相关时间，便于之后排序
def modifyFileTime(filePath, createTime, modifyTime, accessTime, offset):
    """
    用来修改任意文件的相关时间属性，时间格式：YYYY-MM-DD HH:MM:SS 例如：2019-02-02 00:01:02
    :param filePath: 文件路径名
    :param createTime: 创建时间
    :param modifyTime: 修改时间
    :param accessTime: 访问时间
    :param offset: 时间偏移的秒数,tuple格式，顺序和参数时间对应
    """
    try:
        format = "%Y-%m-%d %H:%M:%S"  # 时间格式
        cTime_t = timeOffsetAndStruct(createTime, format, offset[0])
        mTime_t = timeOffsetAndStruct(modifyTime, format, offset[1])
        aTime_t = timeOffsetAndStruct(accessTime, format, offset[2])

        fh = CreateFile(filePath, GENERIC_READ | GENERIC_WRITE, 0, None, OPEN_EXISTING, 0, 0)
        createTimes, accessTimes, modifyTimes = GetFileTime(fh)

        createTimes = Time(time.mktime(cTime_t))
        accessTimes = Time(time.mktime(aTime_t))
        modifyTimes = Time(time.mktime(mTime_t))
        SetFileTime(fh, createTimes, accessTimes, modifyTimes)
        CloseHandle(fh)
        return 0
    except:
        return 1
# 偏移
def timeOffsetAndStruct(times, format, offset):
    return time.localtime(time.mktime(time.strptime(times, format)) + offset)

# 从文件每行生成数据 生成器
def from_file():
    with open('wxjc.json','r',encoding='utf-8') as f:
        while True:
            line = f.readline()
            if not line:
                break
            data = json.loads(line)
            yield data

def handle_md(item):
    title = item['title']
    fp = join(MARKDOWN_DIR,(title + ".md"))
    with open(fp,'w',encoding='utf-8') as f_md:
        f_md.write("# " + title + '\n')
        header_info = "作者:{}          发布时间:{}          Visitors:{}\n".format(item['author'],item['_time'],item['visitors'])
        f_md.write(header_info)
        f_md.write('> ' + item['pre_talk'] + '\n')
        f_md.write(item['article_content'] + '\n')
    # 修改时间
    _time = item['_time'] + ":00"
    cTime = _time  # 创建时间
    mTime = _time  # 修改时间
    aTime = _time  # 访问时间
    offset = (0, 1, 2)  # 偏移的秒数（不知道干啥的）

    # 调用函数修改文件创建时间，并判断是否修改成功
    r = modifyFileTime(fp, cTime, mTime, aTime, offset)
    if r == 0:
        print('修改完成')
    elif r == 1:
        print('修改失败')


if __name__=="__main__":
    # 获取生成器
    j_data =  from_file()
    p=Pool(4)
    for i in j_data:
        p.apply_async(handle_md,args=(i,))
    p.close()
    p.join()
    print("所有进程执行完毕")