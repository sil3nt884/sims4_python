from google.protobuf import descriptor
class CodeGeneratorRequest(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _CODEGENERATORREQUEST

class CodeGeneratorResponse(message.Message, metaclass=reflection.GeneratedProtocolMessageType):

    class File(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
        DESCRIPTOR = _CODEGENERATORRESPONSE_FILE

    DESCRIPTOR = _CODEGENERATORRESPONSE
