import codecsimport binascii
def hex_encode(input, errors='strict'):
    return (binascii.b2a_hex(input), len(input))

def hex_decode(input, errors='strict'):
    return (binascii.a2b_hex(input), len(input))

class Codec(codecs.Codec):

    def encode(self, input, errors='strict'):
        return hex_encode(input, errors)

    def decode(self, input, errors='strict'):
        return hex_decode(input, errors)

class IncrementalEncoder(codecs.IncrementalEncoder):

    def encode(self, input, final=False):
        return binascii.b2a_hex(input)

class IncrementalDecoder(codecs.IncrementalDecoder):

    def decode(self, input, final=False):
        return binascii.a2b_hex(input)

class StreamWriter(Codec, codecs.StreamWriter):
    charbuffertype = bytes

class StreamReader(Codec, codecs.StreamReader):
    charbuffertype = bytes

def getregentry():
    return codecs.CodecInfo(name='hex', encode=hex_encode, decode=hex_decode, incrementalencoder=IncrementalEncoder, incrementaldecoder=IncrementalDecoder, streamwriter=StreamWriter, streamreader=StreamReader, _is_text_encoding=False)
