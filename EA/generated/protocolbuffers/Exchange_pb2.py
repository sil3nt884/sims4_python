from google.protobuf import descriptor
class TrayBlueprintMetadata(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _TRAYBLUEPRINTMETADATA

class TrayRoomBlueprintMetadata(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _TRAYROOMBLUEPRINTMETADATA

class WebTraitTracker(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _WEBTRAITTRACKER

class WebAspirationInfo(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _WEBASPIRATIONINFO

class TraySimMetadata(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _TRAYSIMMETADATA

class TrayRankedStatMetadata(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _TRAYRANKEDSTATMETADATA

class TrayHouseholdMetadata(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _TRAYHOUSEHOLDMETADATA

class TrayMetadata(message.Message, metaclass=reflection.GeneratedProtocolMessageType):

    class ExtraThumbnailInfo(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
        DESCRIPTOR = _TRAYMETADATA_EXTRATHUMBNAILINFO

    class SpecificData(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
        DESCRIPTOR = _TRAYMETADATA_SPECIFICDATA

    DESCRIPTOR = _TRAYMETADATA

class ExchangeItemPrerequisites(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _EXCHANGEITEMPREREQUISITES

class ExchangeEnvelope(message.Message, metaclass=reflection.GeneratedProtocolMessageType):

    class ThumbnailMessage(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
        DESCRIPTOR = _EXCHANGEENVELOPE_THUMBNAILMESSAGE

    DESCRIPTOR = _EXCHANGEENVELOPE

class ExchangeSocialEnvelope(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _EXCHANGESOCIALENVELOPE

class ExchangeListResults(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _EXCHANGELISTRESULTS

class ExchangeWebserverUri(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _EXCHANGEWEBSERVERURI

class BaseUri(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _BASEURI

class ExchangeSearchRequest(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _EXCHANGESEARCHREQUEST

class ExchangeFetchByStatRequest(message.Message, metaclass=reflection.GeneratedProtocolMessageType):

    class ExchangeFetchFromValue(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
        DESCRIPTOR = _EXCHANGEFETCHBYSTATREQUEST_EXCHANGEFETCHFROMVALUE

    DESCRIPTOR = _EXCHANGEFETCHBYSTATREQUEST

class ExchangeFetchKeywordRequest(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _EXCHANGEFETCHKEYWORDREQUEST

class ExchangeFetchRecentRequest(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _EXCHANGEFETCHRECENTREQUEST

class ExchangeGetUpdatedStats(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _EXCHANGEGETUPDATEDSTATS

class ExchangeGetPrefixMatch(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _EXCHANGEGETPREFIXMATCH

class ExchangeCombinedSearch(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _EXCHANGECOMBINEDSEARCH

class ExchangeTestParameters(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _EXCHANGETESTPARAMETERS

class ExchangeSocialMessage(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _EXCHANGESOCIALMESSAGE

class ExchangeWWCEMessage(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _EXCHANGEWWCEMESSAGE

class ExchangeWWCEHideMessage(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _EXCHANGEWWCEHIDEMESSAGE

class ExchangeWWCEKickMessage(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _EXCHANGEWWCEKICKMESSAGE

class ExchangeWWCEResponse(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _EXCHANGEWWCERESPONSE

class ExchangeFetchPlayerInfoMessage(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _EXCHANGEFETCHPLAYERINFOMESSAGE

class SocialId(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SOCIALID

class SocialResponseFollowersMessage(message.Message, metaclass=reflection.GeneratedProtocolMessageType):

    class PlayerFollower(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
        DESCRIPTOR = _SOCIALRESPONSEFOLLOWERSMESSAGE_PLAYERFOLLOWER

    DESCRIPTOR = _SOCIALRESPONSEFOLLOWERSMESSAGE

class SocialFeedSubMessage(message.Message, metaclass=reflection.GeneratedProtocolMessageType):

    class SubscriptionFlags(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
        DESCRIPTOR = _SOCIALFEEDSUBMESSAGE_SUBSCRIPTIONFLAGS

    class SubscriptionObject(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
        DESCRIPTOR = _SOCIALFEEDSUBMESSAGE_SUBSCRIPTIONOBJECT

    DESCRIPTOR = _SOCIALFEEDSUBMESSAGE

class SocialCGVotePeriodMessage(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SOCIALCGVOTEPERIODMESSAGE

class SocialCandidateReportMessage(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SOCIALCANDIDATEREPORTMESSAGE

class SocialCandidatesBroadcast(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SOCIALCANDIDATESBROADCAST

class SocialCGUpdateMessage(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SOCIALCGUPDATEMESSAGE

class ServerPlayerIdentificationMessage(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SERVERPLAYERIDENTIFICATIONMESSAGE

class ServerCallbackInfoMessage(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SERVERCALLBACKINFOMESSAGE

class ServerPlayerIdentificationListMessage(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SERVERPLAYERIDENTIFICATIONLISTMESSAGE

class ExchangeFetchPlayerStatistics(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _EXCHANGEFETCHPLAYERSTATISTICS

class ExchangeFetchSubcriptionStats(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _EXCHANGEFETCHSUBCRIPTIONSTATS

class ExchangeHashtagTrendsMessage(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _EXCHANGEHASHTAGTRENDSMESSAGE

class ExchangeModerateMessage(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _EXCHANGEMODERATEMESSAGE

class ExchangeStatTicker(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _EXCHANGESTATTICKER

class ExchangeStatTickerMessage(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _EXCHANGESTATTICKERMESSAGE

class ExchangeGetSharedItemsByIdMessage(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _EXCHANGEGETSHAREDITEMSBYIDMESSAGE

class ExchangeItemWithStatus(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _EXCHANGEITEMWITHSTATUS

class ExchangeItemListWebMessage(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _EXCHANGEITEMLISTWEBMESSAGE

class ExchangeRecommendationEngineResult(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _EXCHANGERECOMMENDATIONENGINERESULT

class ExchangeControlMessage(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _EXCHANGECONTROLMESSAGE
