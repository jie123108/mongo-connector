import sys
import json
import getopt
from bson.timestamp import Timestamp
from mongo_connector import util


def usage():
    print("""    --help help 
    --ts_file mongo-connector-oplog-timestamp-file 
    --add second to add 
    --set timestamp to set 
    """)

def read_ts_file(ts_file):
    content = json.loads(open(ts_file).read())
    rs = content[0]
    ts = content[1]
    ts = util.long_to_bson_ts(ts)
    return rs, ts

def write_ts_file(ts_file, rs, ts):
    ts_long = util.bson_ts_to_long(ts)
    content = json.dumps([rs, ts_long])
    open(ts_file, "w").write(content)

if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')
    ts_file = None
    add = None
    set_ = None
    try:
        opts, args = getopt.getopt(sys.argv[1:], '',[
            'ts_file=',
            'add=',
            'set=',
        ])
        for name, value in opts:
            # print("name: %s, value: %s" % (name, value))
            if name in ('-h', '--help'):
                usage()
            elif name in ('--ts_file'):
                ts_file = value
            elif name in ('--add'):
                add = int(value)
            elif name in ('--set'):
                set_ = int(value)
            
    except getopt.GetoptError, ex:
        print("exception: %s" % ex)
        usage()
        sys.exit(0)
    if not ts_file:
        usage()
        sys.exit(0)
    
    rs, ts = read_ts_file(ts_file)
    print("raw ### %10s ==> %s" % (rs, ts))

    t = ts.time
    inc = ts.inc
    if add:
        t = t + add
        ts = Timestamp(t, 1)
        write_ts_file(ts_file, rs, ts)
    elif set_:
        ts = Timestamp(set_, 1)
        write_ts_file(ts_file, rs, ts)

    if add or set_:
        rs, ts = read_ts_file(ts_file)
        print("new ### %10s ==> %s" % (rs, ts))
