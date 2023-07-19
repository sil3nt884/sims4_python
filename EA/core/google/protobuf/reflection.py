__author__ = 'robinson@google.com (Will Robinson)'
    if api_implementation.Version() == 2:
        from google.protobuf.internal.cpp import cpp_message
        _NewMessage = cpp_message.NewMessage
        _InitMessage = cpp_message.InitMessage
    else:
        from google.protobuf.internal import cpp_message
        _NewMessage = cpp_message.NewMessage
        _InitMessage = cpp_message.InitMessage
else:
    from google.protobuf.internal import python_message
    _NewMessage = python_message.NewMessage
    _InitMessage = python_message.InitMessage
class GeneratedProtocolMessageType(type):
    _DESCRIPTOR_KEY = 'DESCRIPTOR'

    def __new__(cls, name, bases, dictionary):
        descriptor = dictionary[GeneratedProtocolMessageType._DESCRIPTOR_KEY]
        bases = _NewMessage(bases, descriptor, dictionary)
        superclass = super(GeneratedProtocolMessageType, cls)
        new_class = superclass.__new__(cls, name, bases, dictionary)
        setattr(descriptor, '_concrete_class', new_class)
        return new_class

    def __init__(cls, name, bases, dictionary):
        descriptor = dictionary[GeneratedProtocolMessageType._DESCRIPTOR_KEY]
        _InitMessage(descriptor, cls)
        superclass = super(GeneratedProtocolMessageType, cls)
        superclass.__init__(name, bases, dictionary)
