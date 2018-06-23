# 新添加的配置项
在namespaces正的表(collection)配置下面添加schema配置, schema使用[jsonschema](http://json-schema.org/latest/json-schema-validation.html)语法. 这里只使用了jsonschema中类型相关的定义.

```
namespaces {
    "included_db.collection": {
        "schema": {"type": "object", ... json schema definition }
    },
}
```

schema用于在数据同步时, 对数据进行校验. 当数据源类型与schema定义的目标数据类型不匹配时, 将按以下规则进行修正:

目标数据类型(schema定义的类型) | 源数据类型(mongodb中的类型) | 转换方法
--- | --- | ---
string | string | not changed
string | null | ""
string | list | json.dumps(obj)[1:-1]
string | dict | json.dumps(obj)
string | other | str(obj)
------------ | ------------ | ------------
integer | integer,long | not changed 
integer | bool | true => 1, false => 0
integer | float | int(obj)
integer | string | int(obj), remove it if failed.
integer | list | if obj[0]'s type is integer or long, use obj[0], else remove it.
integer | other | remove it 
------------ | ------------ | ------------
number(float) | float | not changed
number(float) | bool | true => 1.0, false => 0.0
number(float) | integer,long | float(obj), remove it if failed.
number(float) | string | float(obj), remove it if failed.
number(float) | list | if obj[0]'s type is float, use obj[0], else remove it.
number(float) | other | remove it
------------ | ------------ | ------------
boolean | boolean | not changed
boolean | integer,long | 0: false, other: true
boolean | float | 0.0: false, other: true
boolean | str | null, "": false, other: true
boolean | list | if obj[0]'s type is boolean, use obj[0], else remove it.
boolean | other | remove it
------------ | ------------ | ------------
object | object | convert each sub item.
object | other | remove it
------------ | ------------ | ------------
array | array | convert each sub item.
array | other | remove it


## schema示例

#### 示例数据

```
{
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
```

#### 示例Schema

```
"schema": {
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
```