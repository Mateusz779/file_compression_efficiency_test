#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: Mateusz779
"""

import os
import time
import argparse
import time
from typing_extensions import Required

to_compress="."
filename=int(time.time())
algo_type=[]
algo_time={}
algo_size={}
file_count=0

def get_size(start_path):
    global file_count
    file_count = 0
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        file_count=file_count+1
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)

    return total_size

def main():

    parser = argparse.ArgumentParser(description='File compression efficiency test')
    parser.add_argument('--files', required=True,
                    help='location of the test files folder')
    parser.add_argument('--name',default="",
                    help='name of output files')

    parser.add_argument('--lzip',dest="lzip",action='store_false', default=True,
                    help='lzip exclude')
    parser.add_argument('--xz',dest="xz",action='store_false',default=True,
                    help='xz exclude')
    parser.add_argument('--lzop',dest="lzop",action='store_false',default=True,
                    help='lzop exclude')
    parser.add_argument('--lz4',dest="lz4",action='store_false',default=True,
                    help='lz4 exclude')
    parser.add_argument('--tar',dest="tar",action='store_false',default=True,
                    help='tar exclude')
    parser.add_argument('--zip',dest="zip",action='store_false',default=True,
                    help='zip exclude')
    parser.add_argument('--7z',dest="sz",action='store_false',default=True,
                    help='7z exclude')
    parser.add_argument('--pixz',dest="pixz",action='store_false',default=True,
                    help='pixz exclude')
    parser.add_argument('--pigz',dest="pigz",action='store_false',default=True,
                    help='pigz exclude')
    parser.add_argument('--gz',dest="gz",action='store_false',default=True,
                    help='gz exclude')

    args = parser.parse_args()
    if args.files !=".":
        to_compress=args.files

    if args.name !="":
        filename=args.name
    else:
         filename=int(time.time())

    if args.lzip==True:
        algo_type.append("lzip")
    if args.xz==True:
        algo_type.append("xz")
    if args.lzop==True:
        algo_type.append("lzop")
    if args.lz4==True:
        algo_type.append("lz4")

    for i in algo_type:
        start = time.time()
        os.system(("tar cvf {}/../{}.tar.{} --use-compress-program='{} -9' {}".format(to_compress, filename, i, i, to_compress)))
        end = time.time()
        algo_time[i] = end - start
        algo_size[i] = os.path.getsize("{}/../{}.tar.{}".format(to_compress, filename, i));

    if args.tar==True:
        algo_type.append("tar")
        start = time.time()
        os.system(("tar cvf {}/../{}.tar {}".format(to_compress, filename, to_compress)))
        end = time.time()
        algo_time["tar"] = end - start
        algo_size["tar"] = os.path.getsize(("{}/../{}.tar".format(to_compress,filename)));

    if args.zip==True:
        algo_type.append("zip")
        start = time.time()
        os.system("zip -9 -r {}/../{}.zip {}".format(to_compress,filename,to_compress))
        end = time.time()
        algo_time["zip"] = end - start
        algo_size["zip"] = os.path.getsize("{}/../{}.zip".format(to_compress,filename));

    if args.pixz==True:
        algo_type.append("pixz")
        start = time.time()
        os.system("tar cvf {}/../{}.pxz --use-compress-program='pixz -9 -p 8' {}".format(to_compress,filename,to_compress))
        end = time.time()
        algo_time["pixz"] = end - start
        algo_size["pixz"] = os.path.getsize("{}/../{}.pxz".format(to_compress,filename));

    if args.pigz==True:
        algo_type.append("pigz")
        start = time.time()
        os.system("tar cvf {}/../{}.pigz.tar.gz --use-compress-program='pigz -9 -p 8' {}".format(to_compress,filename,to_compress))
        end = time.time()
        algo_time["pigz"] = end - start
        algo_size["pigz"] = os.path.getsize("{}/../{}.pigz.tar.gz".format(to_compress,filename));

    if args.sz==True:
        algo_type.append("7z")
        start = time.time()
        os.system("7z a {}/../{}.7z {}".format(to_compress,filename,to_compress))
        end = time.time()
        algo_time["7z"] = end - start
        algo_size["7z"] = os.path.getsize("{}/../{}.7z".format(to_compress,filename));

    if args.gz==True:
        algo_type.append("gz")
        start = time.time()
        os.system("tar czvf  {}/../{}.tar.gz {}".format(to_compress,filename,to_compress))
        end = time.time()
        algo_time["gz"] = end - start
        algo_size["gz"] = os.path.getsize("{}/../{}.tar.gz".format(to_compress,filename));

    with open(to_compress+'/../stats_{}.txt'.format(filename), 'a') as file:
        file.write("\n{}\n".format(int(time.time())))
        file.write(os.popen("uname -s -r -o").read()+"\n")
        file.write(os.popen("lscpu | egrep 'Model name|Socket|Thread|NUMA|CPU\(s\)'").read()+"\n")
        file.write("size of {}: {} b \n".format(to_compress,get_size(to_compress)))
        file.write("file count: {}\n".format(file_count))
    print("\n{}\n".format(int(time.time())))
    print(os.popen("uname -s -r -o").read())
    print(os.popen("lscpu | egrep 'Model name|Socket|Thread|NUMA|CPU\(s\)'").read())
    print("size of {}: {} b \n".format(to_compress,get_size(to_compress)))
    print("file count: {}\n".format(file_count))

    for i in range(0,len(algo_type)):
        with open(to_compress+'/../stats.txt', 'a') as file:
            file.write("{}:\n {} sek\n {} b \n compress ratio: {} \n\n".format(algo_type[i], algo_time[algo_type[i]], algo_size[algo_type[i]],(algo_size[algo_type[i]]/get_size(to_compress))))
        print("{}:\n {} sek\n {} b \n compress ratio: {} \n\n".format(algo_type[i], algo_time[algo_type[i]], algo_size[algo_type[i]],(algo_size[algo_type[i]]/get_size(to_compress))))

if __name__ == "__main__":
   main()