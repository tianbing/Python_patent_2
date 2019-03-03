#作者：泊头子 微信公众号：专利方舟

#专利复审委复审决定提取源代码

from lxml import etree
import requests
import os
import time
import random
import socket
import logging
import pymysql
def add_to_database(anjuanid,inventor):
    try:
        conn = pymysql.connect(--------------)
        cursor = conn.cursor()
        # sql = "select * from test_table"
        # reCount = cursor.execute(sql)  # 返回受影响的行数
        # print(reCount)
        sql = "insert into test_table values(\"" + anjuanid + "\",\"" + inventor + "\")"
        print(sql)
        reCount = cursor.execute(sql)  # 返回受影响的行数
        conn.commit()
        sql = "select * from test_table"
        reCount = cursor.execute(sql)  # 返回受影响的行数
        print("number of lines involved: " + str(reCount))
        data = cursor.fetchall()  # 返回数据,返回的是tuple类型
        print(data)
        cursor.close()
        conn.close()
    except Exception as e4:
        print("exception database occur!" + str(e4))
def add_reexamination_decision(anjuanid_t,
                               patent_name,
                               design_name,
                               internal_sequence,
                               decision_date,
                               priority_date,
                               application_number,
                               application_date,
                               grant_date,
                               plantiff,
                               assignee,
                               primary_examiner,
                               leading_examiner,
                               attending_examiner,
                               IPC_classification,Locarno_calssification,
                               legitimate,
                               decision_summary,
                               filename_t,
                               full_text
                               ):

    try:
        conn = pymysql.connect(-----------)
        cursor = conn.cursor()
        sql = "INSERT INTO patent_reexamination_decision (juedinghao,patent_name, design_name,internal_sequence," \
              "decision_date,priority_date, application_number,application_date,grant_date, plantiff," \
              "assignee, primary_examiner,leading_examiner,attending_examiner,IPC_classification, " \
              "Locarno_calssification,legitimate,decision_summary,filename,full_text) " \
              "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        #logging.info(juedinghao)
        #print("decision_date: " + decision_date)
        #print("priority_date: " + priority_date)
        if len(str(decision_date)) < 5:
            decision_date = "1900-01-01"
        if len(str(grant_date)) < 5:
            grant_date = "1900-01-01"
        if len(str(priority_date)) < 5:
            priority_date = "1900-01-01"
        if len(str(application_date)) < 5:
            application_date = "1900-01-01"
            #print("IPC: " + IPC_classification)
            #print("Locarno: " + Locarno_calssification)
        if len(str(IPC_classification)) > 90:
            IPC_classification = str(IPC_classification)[0:89]
        if len(str(decision_summary)) > 1000:
            decision_summary = str(decision_summary)[0:999]
        if len(str(full_text)) > 2^24 - 1:
            full_text = str(full_text)[0:2^24-2]
        data = [anjuanid_t, patent_name, design_name,internal_sequence,decision_date,priority_date,
                application_number,application_date,grant_date, plantiff, assignee, primary_examiner,
                leading_examiner,attending_examiner,IPC_classification,Locarno_calssification,
                legitimate,decision_summary,filename_t,full_text];
        cursor.execute(sql, data)
        # 提交，不然无法保存新建或者修改的数据
        conn.commit()
        #sql = "select * from patent_reexamination_decision"
        #reCount = cursor.execute(sql)  # 返回受影响的行数
        #print("number of lines involved: " + str(reCount))
        #data = cursor.fetchall()  # 返回数据,返回的是tuple类型
        #print(data)
        cursor.close()
        conn.close()
        logging.info("Insert Into datebase succees!")
    except Exception as e4:
        try :
            cursor.close()
            conn.close()
        except Exception as econnection:
            logging.error("database close exception: " + str(econnection))
        print("exception database occur!" + str(e4))
        logging.error("exception database occur!" + str(e4))

def add_file_to_database(filename_t, filedata_t):

    try:
        # 将数据存储到数据库
        conn = pymysql.connect(-----------)
        # 创建游标
        cursor = conn.cursor()

        sql = "INSERT INTO file_test (filename,data) VALUES (%s,%s)"
        data = [filename_t,filedata_t];
        print(sql)
        cursor.execute(sql, data)
        # 提交，不然无法保存新建或者修改的数据
        conn.commit()

        # 关闭游标
        cursor.close()
        # 关闭连接
        conn.close()
    except Exception as e5:
        print("exception database occur!" + str(e5))

logging.basicConfig(level=logging.WARNING,#控制台打印的日志级别
                    filename='a.log',
                    filemode='a',##模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
                    #a是追加模式，默认如果不写的话，就是追加模式
                    format=
                    '%(asctime)s - %(levelname)s: %(message)s'
                    #日志格式
                    )

#add_to_database("123460","tianbing")
#add_reexamination_decision('1','2','3','4','2002-01-01','2002-01-01','7','2002-01-01','2002-01-01','10','11','12','13','14','15','16','17','18','19')
socket.setdefaulttimeout(20)      #设置默认超时时间
head={'User-Agent': 'Mozilla/5.0'}# 设置User-Agent浏览器信息
i1=range(126900,126999) #示例性提取复审决定号为170000—170100的100个复审决定
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
            #print (str(document_nodes_titles[nodes_counter])+':' + str(doc_node_text))
            logging.info(str(document_nodes_titles[nodes_counter])+':' + str(doc_node_text))
            if nodes_counter == 0: #专利名称
                patent_name = str(doc_node_text).strip()
                #print("patent_name: " + patent_name)
            if nodes_counter == 1: #决定号
                juedinghao_t = str(doc_node_text).strip()
            if nodes_counter == 2: #委内编号
                internal_sequence = str(doc_node_text).strip()
            if nodes_counter == 3: #专利申请号
                application_number = str(doc_node_text).strip()
            if nodes_counter == 4: #复审请求人
                assignee = str(doc_node_text).strip()
            if nodes_counter == 5: #授权公告日
                grant_date = str(doc_node_text).strip()[0:10]
            if nodes_counter == 6: #专利权人
                assignee = str(doc_node_text).strip()
            if nodes_counter == 7: #合议组组长
                leading_examiner = str(doc_node_text).strip()
            if nodes_counter == 8: #国际分类号
                IPC_classification = str(doc_node_text).strip()
            nodes_counter = nodes_counter + 1

        document_nodes_titles = root.xpath('//div[@class="one4 marginL noborder bg"]//span/text()')
        document_nodes_texts = root.xpath('//div[@class="one4 marginL noborder bg"]/text()')
        nodes_counter = 0;
        for doc_node_text in document_nodes_texts:
            #print(str(document_nodes_titles[nodes_counter]) + ':' + str(doc_node_text))
            logging.info(str(document_nodes_titles[nodes_counter]) + ':' + str(doc_node_text));
            if nodes_counter == 0: #外观设计名称
                design_name = str(doc_node_text).strip()
            if nodes_counter == 1: #决定日
                decision_date = str(doc_node_text).strip()[0:10]
                #print("决定日：" + decision_date + ":Origin:" + str(doc_node_text).strip())
            if nodes_counter == 2: #优先权日
                priority_date = str(doc_node_text).strip()[0:10]
            if nodes_counter == 3: #申请日 0000-00-00 格式
                application_date = str(doc_node_text).strip()[0:10]
            if nodes_counter == 4: #无效请求人
                plantiff = str(doc_node_text).strip()
            #if nodes_counter == 5: #审定公告日
                #decision_date = str(doc_node_text).strip()[0:10]
            if nodes_counter == 6: #主审员
                primary_examiner = str(doc_node_text).strip()
            if nodes_counter == 7: #参审员
                attending_examiner = str(doc_node_text).strip()
            if nodes_counter == 8: #外观设计分类号
                Locarno_calssification = str(doc_node_text).strip()
            nodes_counter = nodes_counter + 1

        document_nodes_titles = root.xpath('//div[@class="two2 marginL noborder bg"]//span/text()')
        document_nodes_texts = root.xpath('//div[@class="two2 marginL noborder bg"]/text()')
        #print(str(document_nodes_titles[0]) + ':' + str(document_nodes_texts[0]))
        logging.info(str(document_nodes_titles[0]) + ":" + str(document_nodes_texts[0]))
        legitimate = str(document_nodes_texts[0]).strip()
        document_nodes_titles = root.xpath('//div[@class="three2 noborder bg"]//span/text()')
        document_nodes_texts = root.xpath('//div[@class="pad5"]/text()')
        #print(str(document_nodes_titles[0]) + ':' + str(document_nodes_texts[0]))
        logging.info(str(document_nodes_titles[0]) + ':' + str(document_nodes_texts[0]))
        decision_summary = str(document_nodes_texts[0]).strip()
        document_nodes_titles = root.xpath('//div[@class="fore1"]/text()')
        #document_nodes_texts = root.xpath('//div[@class="pad5"]/text()')
        #print(str(document_nodes_titles[0]))
        #logging.info(str(document_nodes_titles[0]))
        nodes_counter = 0;
        document_text_t = "";
        for itext in document_nodes_texts:
            if nodes_counter == 0:
                nodes_counter = nodes_counter + 1
                continue
            #print(str(itext))
            document_text_t = document_text_t + str(itext).strip()
        logging.info(str(document_text_t))
        full_text = str(document_text_t).strip()
    except Exception as e:
        print("except0 occur!" + str(e))
        continue #异常后进入下一个循环
    try:
        r = requests.get(dizhi,headers=head,timeout=10) #获取响应状态码，返回WORD文件内容
        filename = os.path.basename(dizhi)              #从复审决定WORD文档网址中抽取文件名
        filename_t = filename
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
    start_time = time.time()
    add_reexamination_decision(str(juedinghao_t), patent_name, design_name, internal_sequence, decision_date,
                               priority_date, application_number, application_date, grant_date,
                               plantiff, assignee, primary_examiner, leading_examiner, attending_examiner,
                               IPC_classification, Locarno_calssification, legitimate, decision_summary, filename_t, str(document_text_t))
    #logging.info()
    end_time = time.time()
    print("database response time_delay = " + str(end_time - start_time))
    logging.info("------------这里是分隔符-------------")
