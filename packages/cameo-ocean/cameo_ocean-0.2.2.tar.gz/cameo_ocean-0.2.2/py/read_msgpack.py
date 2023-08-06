import msgpack

with open('output.msgpack', 'rb') as f:
    for i, d in enumerate(msgpack.Unpacker(f)):
        print(i, d)
