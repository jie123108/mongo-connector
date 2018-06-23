# coding=utf8

import random
import datetime
import time 
from fix_by_schema import *
random.seed(time.time())

"""
bson types:
Double  1   “double”     
String  2   “string”     
Object  3   “object”     
Array   4   “array”  
Binary data 5   “binData”    
ObjectId    7   “objectId”   
Boolean 8   “bool”   
Date    9   “date”   
Null    10  “null”   
32-bit integer  16  “int”    
Timestamp   17  “timestamp”  
64-bit integer  18  “long”
"""

def new_obj_with_random_type(now):
    t = random.randint(1,9)
    if t == 1: #double
        return random.random() * 100
    elif t == 2: #string
        return u"random string-中文: %s" % (now)
    elif t == 3: #object
        return {"first": u"刘", "last": "xiaojie: %s" % (now), "full": {"cs": "100", "ds": 200}}
    elif t == 4: # array string
        return ["ONE{%s}" % (now), "TOW{%s}" % (now)]
    elif t == 5: # array int
        return [random.randint(1,100), random.randint(200,300)]
    elif t == 6: # bool
        return random.randint(0,5) < 3
    elif t == 7: # null
        return None
    elif t == 8: # int
        return random.randint(1, 10000)
    elif t == 9: # long
        return long(random.randint(10000, 10000*100))
    elif t == 10: # date
        return datetime.datetime.now()
    elif t == 11: #timestamp
        return time.time()
    else:
        assert("unknow t: %s" % (t))

def random_name(now):
    ## 有一半概率, 是错误类型的数据
    ok = random.randint(1,10) <= 5
    if ok:
        name = u"name-中文-%s" % (now)
    else:
        name = new_obj_with_random_type(now)
    return name 

def random_alias(now):
    ## 有一半概率, 是错误类型的数据
    ok = random.randint(1,10) <= 5
    if ok:
        alias = ["alias-%s-1" % (now), u"alias-中文-%s-2" % (now)]
    else:
        alias = new_obj_with_random_type(now)
    return alias

def random_films(now):
    ## 有一半概率, 是错误类型的数据
    x = random.randint(1,10)
    ok = x <= 5
    if ok:
        films = [now, now+1]
        if x == 2:
            films[0] = str(films[0])
            films[1] = unicode(films[1])
    else:
        films = new_obj_with_random_type(now)
    return films

def random_films_ex(now):
    ## 有一半概率, 是错误类型的数据
    ok = random.randint(1,10) <= 5
    if ok:
        fid1 = random.randint(1,10000*100)
        fid2 = random.randint(1,10000*100)
        films = [{"fid": fid1, "name": u"中文-%s" % (fid1)}, {"fid": fid2, "name": "name-%s" % (fid2)}]
    else:
        films = new_obj_with_random_type(now)
    return films

def random_pubdate(now):
    ## 有一半概率, 是错误类型的数据
    x = random.randint(1,10)
    ok = x <= 5
    if ok:        
        pubdate = random.randint(20000102, 21001100)
        if x == 5:
            pubdate = str(pubdate)
        elif x == 4:
            pubdate = unicode(pubdate)
    else:
        pubdate = new_obj_with_random_type(now)
    return pubdate

def random_douban(now):
    ## 有一半概率, 是错误类型的数据
    x = random.randint(1,10)
    ok = x <= 5
    if ok:        
        douban = round(random.random() * 10, 1)
        if x == 5:
            douban = str(douban)
        elif x == 4:
            douban = unicode(douban)
    else:
        douban = new_obj_with_random_type(now)
    return douban

def random_foreign_name(now):
    ## 有一半概率, 是错误类型的数据
    ok = random.randint(1,10) <= 5
    if ok:        
        foreign_name = {"CN": u"中文名-%s" % (now), "EN": "EN-%s" % (now), "FR": "FR Name-%s" % (now), "CNT": 100}
    else:
        foreign_name = new_obj_with_random_type(now)
    return foreign_name

def random_files(now):
    ## 有一半概率, 是错误类型的数据
    x = random.randint(1,10)
    ok = x <= 5
    if ok:        
        files = []
        for i in range(random.randint(1,2)):
            name = u"第%s集" % (i+1)
            images = {"3:4": "3x4.jpg", "16:9": "16x9.jpg"}
            detail = {}
            for spec in ["360p", "540p"]:
                fileid = "fileid-%s-%s" % (spec, now)
                url = "%s/%s.m3u8" % (spec, now)
                filesize = random.randint(1024*10, 1024*500)
                if x == 3:
                    filesize = filesize * 1.0
                elif x == 2:
                    url = 150
                detail[spec] = {"fileid": fileid, "url": url, "filesize": filesize}
            
            if x == 5:
                images = []
            elif x == 4:
                detail["360p"] = "error spec"

            info = {"name": name, "images": images, "detail": detail}
            files.append(info)
    else:
        files = new_obj_with_random_type(now)
    return files

def print_field_types(obj):
    keys = obj.keys()
    keys.sort()
    items = []
    for key in keys:
        value = obj[key]
        items.append("%s ---> %s" % (key, type(value)))
    print('|'.join(items))

mytest_data = {
    "name": "Westworld Season 1",
    "alias": ["西部世界", "西方极乐园"],
    "films": [100, 200],
    "filmsex": [{"fid":100, "name": "f100"}, {"fid":200, "name": "f200"}],
    "pubdate": 20180910,
    "douban": 8.9,
    "fgname": {"CN": "西部世界", "EN": "West World", "FR": "XXX"},
    "files": [
        {"name": "第一集", "images": {"3:4": "3x4.png", "16:9": "16x9.png"}, 
            "detail": {
                "360p": {"fileid": "fileid01", "url": "a.m3u8", "filesize": 100}, 
                "540p": {"fileid": "fileid02", "url": "b.m3u8", "filesize": 200}
            }
        }
    ]
}

import jsonschema as jschema


testschema = {
    "type" : "object",
    "properties": {
        "name": {"type": "string"},
        "alias": {"type": "array", "items": {"type": "string"}},
        "films": {"type": "array", "items": {"type": "integer"}},
        "filmsex": {
            "type": "array", "items": {
                "type": "object", 
                "properties": {
                    "fid": {"type": "integer"}, 
                    "name": {"type": "string"}
                }
            }
        },
        "pubdate": {"type": "integer"},
        "douban": {"type": "number"},
        "fgname": {"type": "object", "properties": {
                "CN": {"type": "string"}, 
                "EN": {"type": "string"}, 
                "FR": {"type": "string"}, 
                "CNT": {"type": "integer"}, 
            }
        },
        "files": {"type": "array", "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "images": {
                        "type": "object", "properties": {
                            "3:4": {"type": "string"},
                            "16:9": {"type": "string"}
                        }
                    },
                    "detail": {
                        "type": "object", "properties": {
                            "360p": {"type": "object", "properties": {
                                    "fileid": {"type": "string"},
                                    "url": {"type": "string"},
                                    "filesize": {"type": "integer"},
                                }
                            },
                            "540p": {"type": "object", "properties": {
                                    "fileid": {"type": "string"},
                                    "url": {"type": "string"},
                                    "filesize": {"type": "integer"}
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}

jschema.Draft4Validator.check_schema(testschema)
try:
    jschema.validate(mytest_data, testschema)
except jschema.exceptions.ValidationError, ex:
    print(u"data[%s] is invalid! err: %s" %(mytest_data, ex))

"""
#double
#string
#object
# array int
# array string
# bool
# null
# int
# long
# date
#timestamp
"""
# TODO: 缺失的原始类型字段添加.
def generate_one(now, id):
    info = {
        "id": id,
        "name": random_name(now),
        "alias": random_alias(now),
        "films": random_films(now),
        "filmsex": random_films_ex(now),
        "pubdate": random_pubdate(now),
        "douban": random_douban(now),
        "fgname": random_foreign_name(now),
        "files": random_files(now),
    }
    return info


def check_object(obj, schema):
    try:
        jschema.validate(obj, testschema)
    except jschema.exceptions.ValidationError, ex:
        return False, ex
    return True, None


def generate_data(n, id):
    now = int(time.time())
    datas = []
    for x in range(n):
        info = generate_one(now, id)
        datas.append(info)
        id += 1
    return datas

def generate_data_and_fix(n):
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')

    datas = generate_data(n, 1)
    for info in datas:
        print(u"----------- obj: %s ----------" % (info["name"]))
        # print_field_types(info)
        src = json.dumps(info)
        info = fix_object(info, testschema)
        dest = json.dumps(info)
        
        ok, ex = check_object(info, testschema)
        if ok:
            print("== OK")
        else:
            print("## FAIL err: %s" % (ex))
            print("## SRC  %s" % (src))
            print("## DST  %s" % (dest))

host = "127.0.0.1"
port = 27017
def generate_data_and_insert(n):
    from pymongo import MongoClient
    mongo = MongoClient(host, port)
    db = mongo.test
    id = int(time.time())
    datas = generate_data(n, id)
    for info in datas:
        db.myschema.save(info)

    datas_update = generate_data(n, id)
    for info in datas_update:
        db.myschema.update_one({"id": info["id"]}, {"$set": info})

# generate_data_and_fix(256)
# generate_data_and_insert(256)
# print(json.dumps(testschema))


