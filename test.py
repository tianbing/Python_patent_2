#作者：泊头子 微信公众号：专利方舟

#专利复审委复审决定提取源代码

from lxml import etree
import requests
import os
import time
import random
import socket
import logging

socket.setdefaulttimeout(20)      #设置默认超时时间
head={'User-Agent': 'Mozilla/5.0'}# 设置User-Agent浏览器信息
i1=range(132000,132999) #示例性提取复审决定号为170000—170100的100个复审决定
for juedinghao in i1:
    try:              #异常处理,url为某个复审决定网址
        url = "http://app.sipo-reexam.gov.cn/reexam_out1110/searchdoc/decidedetail.jsp?jdh="+str(juedinghao)+"&lx=fs"
        response = requests.get(url=url,headers=head) #获取响应状态码，返回某个复审决定网页源代码
        if response.status_code != 200:
                continue;
        #t2 = timeit.Timer('x=range(1000)')
        start_time = time.time()
        response = requests.get(url=url,headers=head)

        end_time = time.time();
        print ("web response time_delay = " + str(end_time - start_time))
    except Exception as e2:
        print("except2 occur!" + str(e2))
        continue #异常后进入下一个循环
    response.encoding = response.apparent_encoding #获得真实编码,解决乱码
    root = etree.HTML(response.content)  #利用lxml.html的xpath对html进行分析，获取抓取信息
    response.close()                     #断开连接
    try:
        dizhi=root.xpath('//a/@href')[0] #a标签下选取名为href的所有属性，网页中只存在一个，实际获得复审决定WORD文件网址
        document_nodes_titles = root.xpath('//div[@class="one2 marginL bg"]//span/text()')
        document_nodes_texts = root.xpath('//div[@class="one2 marginL bg"]/text()')
        nodes_counter = 0
        logging.info(juedinghao)
        for doc_node_text in document_nodes_texts:
            print (str(document_nodes_titles[nodes_counter])+':' + str(doc_node_text))
            logging.info(str(document_nodes_titles[nodes_counter])+':' + str(doc_node_text))
            nodes_counter = nodes_counter + 1
        document_nodes_titles = root.xpath('//div[@class="one4 marginL noborder bg"]//span/text()')
        document_nodes_texts = root.xpath('//div[@class="one4 marginL noborder bg"]/text()')
        nodes_counter = 0;
        for doc_node_text in document_nodes_texts:
            print(str(document_nodes_titles[nodes_counter]) + ':' + str(doc_node_text))
            logging.info(str(document_nodes_titles[nodes_counter]) + ':' + str(doc_node_text));
            nodes_counter = nodes_counter + 1

        document_nodes_titles = root.xpath('//div[@class="two2 marginL noborder bg"]//span/text()')
        document_nodes_texts = root.xpath('//div[@class="two2 marginL noborder bg"]/text()')
        print(str(document_nodes_titles[0]) + ':' + str(document_nodes_texts[0]))
        logging.info(str(document_nodes_titles[0]) + ":" + str(document_nodes_texts[0]))
        document_nodes_titles = root.xpath('//div[@class="three2 noborder bg"]//span/text()')
        document_nodes_texts = root.xpath('//div[@class="pad5"]/text()')
        print(str(document_nodes_titles[0]) + ':' + str(document_nodes_texts[0]))
        logging.info(str(document_nodes_titles[0]) + ':' + str(document_nodes_texts[0]))
        document_nodes_titles = root.xpath('//div[@class="fore1"]/text()')
        #document_nodes_texts = root.xpath('//div[@class="pad5"]/text()')
        print(str(document_nodes_titles[0]))
        logging.info(str(document_nodes_titles[0]))
        nodes_counter = 0;
        document_text_t = "";
        for itext in document_nodes_texts:
            if nodes_counter == 0:
                nodes_counter = nodes_counter + 1
                continue
            print(str(itext))
            document_text_t = document_text_t + str(itext)
        logging.info(str(document_text_t))

    except Exception as e:
        print("except0 occur!" + str(e))
        continue #异常后进入下一个循环
    try:
        r = requests.get(dizhi,headers=head,timeout=10) #获取响应状态码，返回WORD文件内容
        filename = os.path.basename(dizhi)              #从复审决定WORD文档网址中抽取文件名
        filename = "/Users/tianbing/documents/python/" + str(juedinghao) + "-" + filename
        if os.path.exists(filename):
            print(filename + " exist")
            continue
        print("ADD: " + filename)
        logging.info("ADD: " + filename)
        with open(filename, "wb") as code:              #打开文件
            code.write(r.content) # 写入内容
            #add_file_to_database(filename,r.content)  #向数据库插入文件
        r.close()                 #断开连接
        code.close()              #关闭文件,可以没有
        time.sleep(random.uniform(1,4)) #按给定的秒数暂停执行，时间自己定，本代码在3-7随机暂停，可以删除
    except Exception as e1:
        print("except1 occur!" + str(e1))
        continue
    print(dizhi,time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),juedinghao) #屏幕输出复审决定网址、当前时间及决定号
    #logging.info()
    logging.info("------------这里是分隔符-------------")
