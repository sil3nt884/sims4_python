__author__ = 'petar@google.com (Petar Petrov)'
    _implementation_type = 'cpp'
    try:
        from google.protobuf.internal import cpp_message
        _implementation_type = 'cpp'
    except ImportError as e:
        _implementation_type = 'python'
    raise ValueError("unsupported PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION_VERSION: '" + _implementation_version_str + "' (supported versions: 1, 2)")
def Type():
    return _implementation_type

def Version():
    return _implementation_version
