import codecs
class Codec(codecs.Codec):

    def encode(self, input, errors='strict'):
        return (str.translate(input, rot13_map), len(input))

    def decode(self, input, errors='strict'):
        return (str.translate(input, rot13_map), len(input))

class IncrementalEncoder(codecs.IncrementalEncoder):

    def encode(self, input, final=False):
        return str.translate(input, rot13_map)

class IncrementalDecoder(codecs.IncrementalDecoder):

    def decode(self, input, final=False):
        return str.translate(input, rot13_map)

class StreamWriter(Codec, codecs.StreamWriter):
    pass

class StreamReader(Codec, codecs.StreamReader):
    pass

def getregentry():
    return codecs.CodecInfo(name='rot-13', encode=Codec().encode, decode=Codec().decode, incrementalencoder=IncrementalEncoder, incrementaldecoder=IncrementalDecoder, streamwriter=StreamWriter, streamreader=StreamReader, _is_text_encoding=False)

def rot13(infile, outfile):
    outfile.write(codecs.encode(infile.read(), 'rot-13'))

    import sys
    rot13(sys.stdin, sys.stdout)