from google.protobuf import descriptor
class SocialFriendMsg(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SOCIALFRIENDMSG

class SocialPersonaResponseMsg(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SOCIALPERSONARESPONSEMSG

class SocialGenericResponse(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SOCIALGENERICRESPONSE

class SocialPlayerInfoList(message.Message, metaclass=reflection.GeneratedProtocolMessageType):

    class PlayerInfo(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
        DESCRIPTOR = _SOCIALPLAYERINFOLIST_PLAYERINFO

    DESCRIPTOR = _SOCIALPLAYERINFOLIST

class SocialSearchMsg(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SOCIALSEARCHMSG

class OriginErrorMessage(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _ORIGINERRORMESSAGE

class SocialInviteResponseMessage(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SOCIALINVITERESPONSEMESSAGE

class SocialCassandraTest(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SOCIALCASSANDRATEST

class SocialFriendListRequestMessage(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SOCIALFRIENDLISTREQUESTMESSAGE

class SocialRequestNucleusIdFromPersona(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SOCIALREQUESTNUCLEUSIDFROMPERSONA

class SocialNucleusIdFromPersonaResponse(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SOCIALNUCLEUSIDFROMPERSONARESPONSE

class SocialExchangeMessage(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SOCIALEXCHANGEMESSAGE

class SocialFollowersMessage(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SOCIALFOLLOWERSMESSAGE

class SocialFeedItemMessage(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SOCIALFEEDITEMMESSAGE

class SocialFeedItemUnserializedMessage(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SOCIALFEEDITEMUNSERIALIZEDMESSAGE

class SocialWallCommentMessage(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SOCIALWALLCOMMENTMESSAGE

class SocialGetWallCommentsMessage(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SOCIALGETWALLCOMMENTSMESSAGE

class SocialPostWallCommentMessage(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SOCIALPOSTWALLCOMMENTMESSAGE

class SocialDeleteWallCommentMessage(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SOCIALDELETEWALLCOMMENTMESSAGE

class SocialRequestFeedWallMessage(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SOCIALREQUESTFEEDWALLMESSAGE

class SocialRequestFollowersMessage(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SOCIALREQUESTFOLLOWERSMESSAGE

class SocialRequestIgnoreListMessage(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SOCIALREQUESTIGNORELISTMESSAGE

class SocialGetPlayerInfoListMessage(message.Message, metaclass=reflection.GeneratedProtocolMessageType):

    class PlayerInfo(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
        DESCRIPTOR = _SOCIALGETPLAYERINFOLISTMESSAGE_PLAYERINFO

    DESCRIPTOR = _SOCIALGETPLAYERINFOLISTMESSAGE

class SocialCommentPetitionMessage(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SOCIALCOMMENTPETITIONMESSAGE

class SocialBioPetitionMessage(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SOCIALBIOPETITIONMESSAGE

class SocialFeedRemovalMessage(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SOCIALFEEDREMOVALMESSAGE

class SocialControlMessage(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SOCIALCONTROLMESSAGE

class SocialInvalidateMsg(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SOCIALINVALIDATEMSG

class SocialControlQueueBroadcastMessage(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SOCIALCONTROLQUEUEBROADCASTMESSAGE

class LifeEventMessage(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _LIFEEVENTMESSAGE

class SocialFacebookEventMessage(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SOCIALFACEBOOKEVENTMESSAGE

class SocialCandidateStatisticSubmessage(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SOCIALCANDIDATESTATISTICSUBMESSAGE

class SocialCandidatesMessage(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SOCIALCANDIDATESMESSAGE

class SocialEvaluationResultsMessage(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SOCIALEVALUATIONRESULTSMESSAGE

class SocialCGDigestMessage(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SOCIALCGDIGESTMESSAGE
