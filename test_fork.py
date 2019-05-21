import time
import os
import sys

# print('start++++++++')
# source = 10
# try:
#     pid = os.fork()
#     print('pid=', pid)
#     if pid == 0:
#         print("这是子进程")
#         source = source -1
#     else:
#         # 父进程
#         print("这是父进程")
#     print(source)
# except OSError as e:
#     pass
#
# print('End=======')

def main():
    print('helloworld')

def createDaemon():

    try:
        if os.fork() > 0:
            sys.exit(0)
    except OSError as error:
        print('(fork第一个子进程失败）fork #1 failed: %d (%s)' % (error.errno, error.strerror))
        sys.exit(1)

    os.chdir('/')
    os.setsid()
    os.umask(0)

    try:
        pid = os.fork()
        if pid > 0:
            print('Daemon PID %d' % pid)
            sys.exit(0)
    except OSError as error:
        print('（fork第二个子进程失败）fork #2 failed: %d (%s)' % (error.errno, error.strerror))

    main()

if __name__ == '__main__':
    createDaemon()
