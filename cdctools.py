#! *-* coding:utf-8 *-*
#python-version: python34
import os,sys
from unicodetest import _smartcode
import configparser 
# CDROM = r'F:\test'

def cdWalker(cdrom,cdcfile):
    '''光盘扫描主函式
    @param cdrom: 光盘访问路径
    @param cdcfile: 输出的光盘信息记录文件(包含路径，绝对，相对都可以)
    @return: 无，直接输出成*.cdc文件
    @attention: 从v0.7 开始不使用此扫描函式，使用iniCDinfo()
    '''

    export = ""

    for root,dirs,files in os.walk(cdrom):
        print(formatCDinfo(root,dirs,files))
        export += formatCDinfo(root,dirs,files)
        with open(cdcfile,'a') as f:
            f.write(export)

##cdWalker(r'F:\test',r'F:\temp\text3.out')
##cdWalker(r'F:\test',r'F:\temp\text4.out')
# if "-e" == sys.argv[1]:
#     cdWalker(CDROM,sys.argv[2])
#     print("记录路径信息到{}".format(sys.argv[2]))
# else:
#     print('''PyCDC使用方式:
#     python pycdc.py -e mycd1-1.cdc
#     #将路径信息记录为mycdc1-1.cdc
#     ''')

def cdcGrep(cdcpath,keyword):
    '''目录信息查询函式
    @param cdcpath: 查询的目录
    @param keyword: 查询关键词
    @return: 无,直接显示相关文字行
    '''
    filelist = os.listdir(cdcpath)
    for cdc in filelist:
        if ".cdc" in cdc:
            with open(cdcpath+cdc) as f:
                for line in f.readlines():
                    if keyword in line:
                        print(line)

def formatCDinfo(root,dirs,files):
    '''光盘信息记录格式化函式
    @note: 直接利用os.walk()函式的输出信息进行重组
    @param root: 当前根
    @param dirs： 当前根中的所有目录
    @param files: 当前根中的所有文件
    @return: 字串，组织好的当前目录信息

    '''
    export = "\n{}\n".format(root)
    for d in dirs:
        export += "-d {}{}\n".format(root,_smartcode(d))
    for f in files:
        export += "-f {} {}\n".format(root,_smartcode(f))
    export += "="*70
    return export

def iniCDinfo(cdrom,cdcfile):
    '''光盘信息.ini 格式化函式
    @note: 直接利用 os.walk() 函式的输出信息由ConfigParser
    进行重组处理成.ini 格式文本输出记录
    @param cdrom: 光盘访问路径
    @param cdcfile: 输出的光盘信息记录文件(包含路径，绝对、相对都可以)
    @return: 无,直接输出成组织好的类.ini 的*.cdc文件
    '''

    walker = {}
    for root,dirs,files in os.walk(cdrom):
        walker[root] = (dirs,files)
    config = configparser.ConfigParser()
    config['Info'] = {'ImagePath':cdrom,
                      'Volume':cdcfile}
    config.add_section('Comment')
    dirs = walker.keys()
    i = 0
    for d in dirs:
        i += 1
        config.set("Comment",str(i),d)
    for p in walker:
        config[p] = {}
        for f in walker[p][1]:
            config.set(p,f,str(os.stat("{}/{}".format(p,f)).st_size))
    with open(cdcfile,"w") as configfile:
        config.write(configfile)
