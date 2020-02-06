#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 04/02/2020

@author: zhouxuan

"""

import itchat
from itchat.content import *
import time


def msg_handler(msg):

    global emo
#    print(msg)    
    wx_typ = {'Text':'txt','Sharing':'shr','Picture': 'img', 'Video': 'vid', 'Attachment':'fil'}.get(msg['Type']) #, 'fil'
    if msg['Type'] == 'Text':
        wx_text = msg['Text']  
    elif msg['Type'] == 'Sharing':
        wx_text = msg['FileName']+': '+ msg['Url']
    else:
        msg['Text']('temp\\'+msg['FileName'])
        wx_text = 'temp\\'+msg['FileName']
        
    wx_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(int(msg['CreateTime'])))
    
    try:
        wx_name = msg['ActualNickName']
        wx_group = itchat.search_chatrooms(userName=msg['FromUserName'])['NickName'] 
    except:
        wx_name = itchat.search_friends(userName=msg['FromUserName'])['NickName']
        wx_group = ''
        
    wx_trans = u'%s(%s): \n%s' % (emo[hash(wx_name)%len(emo)]+'·'+wx_name,wx_group,wx_text)

#    print("(msg_handler) msg received: %s"%wx_trans)
    
    return [wx_time, wx_name, wx_group, wx_text, wx_typ, wx_trans]
    
def txt_transfer(usr,msg):
    print('(txt_transfer): ... transfering txt msg')
    itchat.send_msg(msg, itchat.search_chatrooms(name=usr)[0]['UserName']) 
                        
def mm_transfer(usr,typ,file):
    print('(mm_transfer): ... transfering multimedia msg')
    itchat.send('@%s@%s' %(typ,file),toUserName=itchat.search_chatrooms(name=usr)[0]['UserName'])

#@itchat.msg_register([itchat.content.TEXT, itchat.content.PICTURE, itchat.content.RECORDING, itchat.content.ATTACHMENT, itchat.content.VIDEO], isGroupChat=True, isFriendChat=True)
@itchat.msg_register([TEXT, SHARING, PICTURE, RECORDING, ATTACHMENT, VIDEO],isFriendChat=True, isGroupChat=True)
def chat_handle(msg):
    global dax_grps
    global old_msg
    msg_cpl = msg_handler(msg)
      
    if msg_cpl[2][:3] == u'DAX' and old_msg!=msg_cpl[3]:
        print(msg_cpl[0] + ': ' + msg_cpl[-1])
        if msg_cpl[4]=='txt' or msg_cpl[4]=='shr':
            old_msg = msg_cpl[-1]
            for grp in dax_grps:
                if grp != msg_cpl[2]:
                    txt_transfer(grp, msg_cpl[-1])
        else:
            old_msg = msg_cpl[3]
            for grp in dax_grps:
                if grp != msg_cpl[2]:
                    mm_transfer(grp, msg_cpl[4], msg_cpl[3])
                
# emoji set
emo = ['[微笑]','[撇嘴]','[色]','[发呆]','[得意]','[害羞]','[闭嘴]','[睡]','[调皮]','[呲牙]','[偷笑]','[愉快]','[憨笑]','[悠闲]','[奋斗]','[疑问]','[嘘]','[鼓掌]','[坏笑]','[左哼哼]','[右哼哼]','[哈欠]','[阴险]','[西瓜]','[啤酒]','[咖啡]','[玫瑰]','[蛋糕]','[月亮]','[太阳]','[拥抱]','[强]','[握手]','[胜利]','[抱拳]','[勾引]','[拳头]','[OK]','[跳跳]','[发抖]','[转圈]','😄','😷','😝','😒','[嘿哈]','[捂脸]','[奸笑]','[机智]','[耶]','[吃瓜]','[加油]','[Emm]','[社会社会]','[旺柴]','[好的]','[哇]','🙃','🤔','👻','🙈','🙏','💪','👊','🙌','💯','💃','🍻','🎉','📦','[红包]','[蜡烛]']	#length = 72
dax_grps = [u'DAX全德学生群', u'DAX信息1群', u'DAX信息2群', u'DAX群', u'DAX爱国群']
old_msg = ''

itchat.auto_login(enableCmdQR=True,hotReload = True)
itchat.get_chatrooms(update=True)
itchat.run()
