# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import uuid
from uuid import uuid4
from django.utils.encoding import force_bytes, force_text
import datetime
 
def create_key():
    """ ランダムな文字列を生成 """
  
    key = uuid.uuid4().hex
    return key
 
def create_expiration_date():
    """ 仮登録の有効期限を生成 """
 
    now = datetime.datetime.now()
 
    # 現日時に1時間 加算
    expiration_date = now + datetime.timedelta(hours=1)
 
    return expiration_date