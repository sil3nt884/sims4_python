from google.protobuf import descriptor
class Vector2(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _VECTOR2

class Vector3(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _VECTOR3

class Quaternion(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _QUATERNION

class Transform(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _TRANSFORM

class LinearCurve(message.Message, metaclass=reflection.GeneratedProtocolMessageType):

    class CurvePoint(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
        DESCRIPTOR = _LINEARCURVE_CURVEPOINT

    DESCRIPTOR = _LINEARCURVE
