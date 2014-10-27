# -*- coding: utf-8 -*-
import hashlib
import web
import lxml
import time
import os
import urllib2,json
import dbConnection as db
from lxml import etree
 
class WeixinInterface:
    
    def __init__(self):
        self.app_root = os.path.dirname(__file__)
        self.templates_root = os.path.join(self.app_root, 'templates')
        self.render = web.template.render(self.templates_root)
 
    def GET(self):
        #��ȡ�������
        data = web.input()
        signature=data.signature
        timestamp=data.timestamp
        nonce=data.nonce
        echostr=data.echostr
        #�Լ���token
        token="dsoul0621" #�����д����΢�Ź���ƽ̨�������token
        #�ֵ�������
        list=[token,timestamp,nonce]
        list.sort()
        sha1=hashlib.sha1()
        map(sha1.update,list)
        hashcode=sha1.hexdigest()
        #sha1�����㷨        
 
        #���������΢�ŵ�������ظ�echostr
        if hashcode == signature:
            return echostr
        
    def POST(self):        
        str_xml = web.data() #���post��������
        xml = etree.fromstring(str_xml)#����XML����
        msgType=xml.find("MsgType").text
        fromUser=xml.find("FromUserName").text
        toUser=xml.find("ToUserName").text
        if msgType == "event":
            mscontent = xml.find("Event").text
            if mscontent == "subscribe":
                reply = u'''����  -a[�ո�]�ؼ���  �������ؼ��֣�����  -d[�ո�]�ؼ���  ��ɾ��һ���Ѿ���ӵĹؼ��֣� ���� -s ���鿴��ǰ���ĵĹؼ��֣� ���� news ���鿴�����������š� '''
                return self.render.reply_text(fromUser,toUser,int(time.time()), reply)
            if mscontent == "unsubscribe":
                reply = u'''��֪����ǰ�Ĺ��ܼܺ򵥣������һ������Ľ�����ӭ�Ժ�������'''
                return self.render.reply_text(fromUser,toUser,int(time.time()), reply)
        elif msgType == "text":
            #return self.render.reply_text(fromUser,toUser,int(time.time()), "success")
            content=xml.find("Content").text#����û������������
            if content == "-h":
                reply = u'''����  -a[�ո�]�ؼ���  �������ؼ��֣�����  -d[�ո�]�ؼ���  ��ɾ��һ���Ѿ���ӵĹؼ��֣� ���� -s ���鿴��ǰ���ĵĹؼ��֣� ���� news ���鿴�����������š� '''
                return self.render.reply_text(fromUser,toUser,int(time.time()), reply)
            elif content == "-s":
                keyword = []
            	for user in db.get_all('User'):
                    if user.openID == fromUser:
                        keyword.append(user.keyword)
                keyword = db.unique(keyword)
                #return self.render.reply_text(fromUser,toUser,int(time.time()), "123")
                ret = ""
                for key in keyword:
                    ret += key + " "
                return self.render.reply_text(fromUser,toUser,int(time.time()), ret)
            elif content == "news":
                #ret = "no news yet!"
                keyword = []
            	for user in db.get_all('User'):
                    if user.openID == fromUser:
                        keyword.append(user.keyword)
                keyword = db.unique(keyword)
                #return self.render.reply_text(fromUser,toUser,int(time.time()), "123")
                
                #return self.render.reply_text(fromUser,toUser,int(time.time()), '#')
                #return self.render.reply_text(fromUser,toUser,int(time.time()), "123456")
                
                ret = ""
                cnt = 1
                for x in db.get_all('News'):
                    #cnt = cnt + 1
                    for key in keyword:
                        if x.title.find(key) != -1:
                            #cnt = cnt + 1
                            ret += x.title + "\n" + x.url + "\n"
                            break
                if ret == "":
                    return self.render.reply_text(fromUser,toUser,int(time.time()), "No news yet!") 
                return self.render.reply_text(fromUser,toUser,int(time.time()), ret)
            else:
                if content.find("-a") == 0:
                    tmp = content[3: len(content)]
                    #return self.render.reply_text(fromUser,toUser,int(time.time()), "tmp")
                    for user in db.get_all('User'):
                        #return self.render.reply_text(fromUser,toUser,int(time.time()), "already exists!")
                        if (user.keyword == tmp) and (user.openID == fromUser):
                            return self.render.reply_text(fromUser,toUser,int(time.time()), "already exists!")
                    
                    db.get_insert('User', fromUser, tmp)
                    return self.render.reply_text(fromUser,toUser,int(time.time()), "success.")
                elif content.find("-d") == 0:
                    #return self.render.reply_text(fromUser,toUser,int(time.time()), "123")
                    tmp = content[3: len(content)]
                    flag = 0
                    for user in db.get_all('User'):
                        if (user.keyword == tmp) and (user.openID == fromUser):
                            db.get_delete('User', "id=" + str(user.id))
                            flag = 1
                    
                    if flag == 1:
                        return self.render.reply_text(fromUser,toUser,int(time.time()), "success.")
                    else:
                        return self.render.reply_text(fromUser,toUser,int(time.time()), "no such keyword!")
                else:
                    return self.render.reply_text(fromUser,toUser,int(time.time()), "no such method!")

                    
            return self.render.reply_text(fromUser,toUser,int(time.time()), ret)
