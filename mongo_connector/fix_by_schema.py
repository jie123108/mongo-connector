# coding=utf8

import logging
import jsonschema as jschema
import json 


logger = logging.getLogger(__name__)


# return fixed string obj
def fix_to_string(obj, obj_type):
    value = None
    if obj_type == str or obj_type == unicode:
        value = obj
    elif obj == None:
        value = ""
    elif obj_type == list:
        value = json.dumps(obj)[1:-1]
    elif obj_type == dict:
        value = json.dumps(obj)
    else: 
        value = str(obj)
    return value


def fix_to_integer(obj, obj_type):
    value = 0
    invalid = False
    if obj_type == int or obj_type == long:
        value = obj
    elif obj_type == bool:
        value = 1 if obj else 0
    elif obj_type == float:
        value = int(obj)
    elif obj_type == str or obj_type == unicode:
        try:
            value = int(obj)
        except:
            invalid = True
    elif obj_type == list:
        if len(obj) > 0 and (type(obj[0]) == int or type(obj[0]) == long):
            value = obj[0]
        else:
            invalid = True
    else:
        invalid = True

    return value, invalid

def fix_to_float(obj, obj_type):
    value = 0
    invalid = False
    if obj_type == float:
        value = obj
    elif obj_type == bool:
        value = 1.0 if obj else 0.0
    elif obj_type == int or obj_type == long:
        try:
            value = float(obj)
        except:
            invalid = True
    elif obj_type == str or obj_type == unicode:
        try:
            value = float(obj)
        except:
            invalid = True
    elif obj_type == list:
        if len(obj) > 0 and type(obj[0]) == float:
            value = obj[0]
        else:
            invalid = True
    else:
        invalid = True

    return value, invalid
    
def fix_to_bool(obj, obj_type):
    value = False
    invalid = False
    if obj_type == bool:
        value = obj
    elif obj_type == int or obj_type == long:
        value = obj != 0
    elif obj_type == float:
        value = not(obj < 0.000001 and obj > -0.000001)
    elif obj_type == str or obj_type == unicode:
        value = obj != ""
    elif obj_type == list:
        if len(obj) > 0 and type(obj[0]) == bool:
            value = obj[0]
        else:
            invalid = True
    else:
        invalid = True

    return value, invalid
"""
"filmsex": {"type": "array", "items": {
            "type": "object", 
            "properties": {"fid": {"type": "integer"}, "name": {"type": "string"} }
            }
        },
 """
def fix_object_internal(obj, schema):
    exp_type = schema.get("type")
    obj_type = type(obj)

    ok_obj = None 
    invalid = False
    if exp_type:
        if exp_type == "string":
            ok_obj = fix_to_string(obj, obj_type)
        elif exp_type == "integer":
            ok_obj, invalid = fix_to_integer(obj, obj_type)
        elif exp_type == "object":
            ok_obj = {}
            if obj_type == dict:
                properties = schema.get("properties")
                if properties:
                    for key, value in obj.iteritems():
                        # get sub item schema
                        value_schema = properties.get(key)
                        if value_schema: #if have a schema, fix by schema
                            ok_value, value_invalid = fix_object_internal(value, value_schema)
                            if value_invalid:
                                logger.error(u"fix_object_internal(%s, schema=%s) failed! ", unicode(value), value_schema)
                            else:
                                ok_obj[key] = ok_value
                        else: #no schema, copy it
                            ok_obj[key] = value
                else:
                    ok_obj = obj
            else:
                logger.error(u"fix_object '%s' failed! object type(%s) is invalid! exp type: %s", unicode(obj), obj_type, exp_type)
                invalid = True
        elif exp_type == "array":
            ok_obj = []
            if obj_type == list:
                # sub item schema
                value_schema = schema.get("items")
                if value_schema:
                    for value in obj:
                        ok_value, value_invalid = fix_object_internal(value, value_schema)
                        if value_invalid:
                            logger.error(u"fix_object(%s, schema=%s) failed! value is invalid!", unicode(value), value_schema)
                        else:
                            ok_obj.append(ok_value)
                else:
                    ok_obj = obj
            else:
                logger.error(u"fix_object '%s' failed! object type(%s) is invalid! exp type: %s", unicode(obj), obj_type, exp_type)
                invalid = True
        elif exp_type == "number":
            ok_obj, invalid = fix_to_float(obj, obj_type)
        elif exp_type == "boolean":
            ok_obj, invalid = fix_to_bool(obj, obj_type)
        else:
            logger.error(u"unknow type: %s, obj: %s", exp_type, unicode(obj))
            invalid = True

    else: # 如果未指定类型, 不进行修复.
        ok_obj = obj
    return ok_obj, invalid

def fix_object(obj, schema):
    ok_obj, invalid = fix_object_internal(obj, schema)
    if invalid:
        ok_obj = {}
    return ok_obj
