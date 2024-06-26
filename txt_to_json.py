
def txt_file_to_json(filename):
    txt_fo = open(filename, "r")

    #for line in txt_fo.readlines():
    #    line = line.strip()
    #    print('1:'+line)

    #for index, line in enumerate(txt_fo):
    #    line = line.strip()
    #    print(str(index)+': '+line)

    #print "读取的数据为: %s" % (line)

    while True:
        line1 = txt_fo.readline()
        line2 = txt_fo.readline()
        if not line2: break  # EOF

        print('line1: '+line1+'line2: '+line2)

    # 关闭文件
    txt_fo.close()

if __name__ == "__main__":
    import sys
    #fib(int(sys.argv[1]))

    try:
        filename = sys.argv[1]
        txt_file_to_json(filename)
        #print(sys.argv[1])
    except IndexError as e:
        txt_file_to_json("sample/つのじゅ - ___ (27116379).txt")

