from google.protobuf import descriptor
class Operation(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _OPERATION

class OperationList(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _OPERATIONLIST

class ObjectCreate(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _OBJECTCREATE

class ObjectReplace(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _OBJECTREPLACE

class ObjectDelete(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _OBJECTDELETE

class ObjectReset(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _OBJECTRESET

class SocialGroupCreate(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SOCIALGROUPCREATE

class SocialGroupUpdate(message.Message, metaclass=reflection.GeneratedProtocolMessageType):

    class SocialGroupMember(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
        DESCRIPTOR = _SOCIALGROUPUPDATE_SOCIALGROUPMEMBER

    DESCRIPTOR = _SOCIALGROUPUPDATE

class SocialGroupTargetUpdate(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SOCIALGROUPTARGETUPDATE

class StartClubGathering(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _STARTCLUBGATHERING

class UpdateClubGathering(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _UPDATECLUBGATHERING

class EndClubGathering(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _ENDCLUBGATHERING

class ClubInfo(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _CLUBINFO

class ClubMembershipCriteriaValidation(message.Message, metaclass=reflection.GeneratedProtocolMessageType):

    class FailureInfo(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
        DESCRIPTOR = _CLUBMEMBERSHIPCRITERIAVALIDATION_FAILUREINFO

    DESCRIPTOR = _CLUBMEMBERSHIPCRITERIAVALIDATION

class ClubValidation(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _CLUBVALIDATION

class AskAboutClubsDialog(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _ASKABOUTCLUBSDIALOG

class PartyMember(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _PARTYMEMBER

class PartyCreate(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _PARTYCREATE

class PartyUpdate(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _PARTYUPDATE

class PartyTurnUpdate(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _PARTYTURNUPDATE

class PartyKickout(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _PARTYKICKOUT

class SimInfoCreate(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SIMINFOCREATE

class ClientCreate(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _CLIENTCREATE

class SetOwnerID(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETOWNERID

class SetLocation(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETLOCATION

class SetModel(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETMODEL

class SetRig(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETRIG

class SetVoicePitch(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETVOICEPITCH

class SetSkinTone(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETSKINTONE

class SetSkinToneValShift(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETSKINTONEVALSHIFT

class SetSimAttachment(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETSIMATTACHMENT

class SetPeltLayers(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETPELTLAYERS

class SetCustomTexture(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETCUSTOMTEXTURE

class SetVoiceActor(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETVOICEACTOR

class SetVoiceSuffixOverrides(message.Message, metaclass=reflection.GeneratedProtocolMessageType):

    class SuffixOverride(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
        DESCRIPTOR = _SETVOICESUFFIXOVERRIDES_SUFFIXOVERRIDE

    DESCRIPTOR = _SETVOICESUFFIXOVERRIDES

class SetVoiceEffect(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETVOICEEFFECT

class SetPhysique(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETPHYSIQUE

class SetFirstName(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETFIRSTNAME

class SetLastName(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETLASTNAME

class SetBreedName(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETBREEDNAME

class SetFullNameKey(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETFULLNAMEKEY

class SetFirstNameKey(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETFIRSTNAMEKEY

class SetLastNameKey(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETLASTNAMEKEY

class SetBreedNameKey(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETBREEDNAMEKEY

class RouteCancel(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _ROUTECANCEL

class SetFootprint(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETFOOTPRINT

class UpdateFootprintStatus(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _UPDATEFOOTPRINTSTATUS

class SetSlot(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETSLOT

class SetDisabledSlots(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETDISABLEDSLOTS

class SetScale(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETSCALE

class SetTint(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETTINT

class SetOpacity(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETOPACITY

class SetFadeablePartOpacity(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETFADEABLEPARTOPACITY

class SetPregnancyProgress(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETPREGNANCYPROGRESS

class SetSinged(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETSINGED

class SetGrubby(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETGRUBBY

class SetDyed(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETDYED

class SetMessy(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETMESSY

class SetTanLevel(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETTANLEVEL

class SetGhost(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETGHOST

class SetGeometryState(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETGEOMETRYSTATE

class SetVisibility(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETVISIBILITY

class SetVisibilityFlags(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETVISIBILITYFLAGS

class SetMaterialState(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETMATERIALSTATE

class SetPinWheelSpinSpeed(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETPINWHEELSPINSPEED

class SetSortOrder(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETSORTORDER

class SetInteractable(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETINTERACTABLE

class SetParentType(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETPARENTTYPE

class SetAudioEffects(message.Message, metaclass=reflection.GeneratedProtocolMessageType):

    class AudioEffect(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
        DESCRIPTOR = _SETAUDIOEFFECTS_AUDIOEFFECT

    DESCRIPTOR = _SETAUDIOEFFECTS

class SetActorType(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETACTORTYPE

class SetActorData(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETACTORDATA

class SetActorStateMachineParams(message.Message, metaclass=reflection.GeneratedProtocolMessageType):

    class ActorStateMachineParam(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
        DESCRIPTOR = _SETACTORSTATEMACHINEPARAMS_ACTORSTATEMACHINEPARAM

    DESCRIPTOR = _SETACTORSTATEMACHINEPARAMS

class SetFocusScore(message.Message, metaclass=reflection.GeneratedProtocolMessageType):

    class FocusScoreEntry(message.Message, metaclass=reflection.GeneratedProtocolMessageType):

        class FocusScoreEntryMultiplier(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
            DESCRIPTOR = _SETFOCUSSCORE_FOCUSSCOREENTRY_FOCUSSCOREENTRYMULTIPLIER

        DESCRIPTOR = _SETFOCUSSCORE_FOCUSSCOREENTRY

    class SpecificFocusScoreEntry(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
        DESCRIPTOR = _SETFOCUSSCORE_SPECIFICFOCUSSCOREENTRY

    DESCRIPTOR = _SETFOCUSSCORE

class SetSimActive(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETSIMACTIVE

class SetSimOutfits(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETSIMOUTFITS

class PartData(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _PARTDATA

class PartDataListMessage(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _PARTDATALISTMESSAGE

class SetGeneticData(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETGENETICDATA

class SetThumbnail(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETTHUMBNAIL

class VideoSetPlaylist(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _VIDEOSETPLAYLIST

class SetLightDimmer(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETLIGHTDIMMER

class SetLightMaterialStates(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETLIGHTMATERIALSTATES

class SetLightColor(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETLIGHTCOLOR

class SetHauntedLight(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETHAUNTEDLIGHT

class SetCensorState(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETCENSORSTATE

class FadeOpacity(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _FADEOPACITY

class SetStandInModel(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETSTANDINMODEL

class FadeFadeablePartOpacity(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _FADEFADEABLEPARTOPACITY

class SetObjectDefStateIndex(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETOBJECTDEFSTATEINDEX

class SetMoney(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETMONEY

class InitializeCollection(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _INITIALIZECOLLECTION

class SetPainting(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETPAINTING

class SetPuzzle(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETPUZZLE

class SimPhotoInfo(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SIMPHOTOINFO

class TakePhoto(message.Message, metaclass=reflection.GeneratedProtocolMessageType):

    class MoodCategory(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
        DESCRIPTOR = _TAKEPHOTO_MOODCATEGORY

    DESCRIPTOR = _TAKEPHOTO

class CompositeParams(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _COMPOSITEPARAMS

class CompositeThumbnail(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _COMPOSITETHUMBNAIL

class CompositeImages(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _COMPOSITEIMAGES

class HouseholdCreate(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _HOUSEHOLDCREATE

class TravelGroupCreate(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _TRAVELGROUPCREATE

class SetValue(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETVALUE

class SetId(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETID

class SetBuildBuyUseFlags(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETBUILDBUYUSEFLAGS

class SetSimAge(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETSIMAGE

class SetSimAgeProgress(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETSIMAGEPROGRESS

class SetGender(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETGENDER

class SetSpecies(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETSPECIES

class SetDeathType(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETDEATHTYPE

class SetCurrentSkillId(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETCURRENTSKILLID

class ChangeSimOutfit(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _CHANGESIMOUTFIT

class GigInfo(message.Message, metaclass=reflection.GeneratedProtocolMessageType):

    class ObjectiveChain(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
        DESCRIPTOR = _GIGINFO_OBJECTIVECHAIN

    DESCRIPTOR = _GIGINFO

class AuditionUpdate(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _AUDITIONUPDATE

class PreferencesUpdate(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _PREFERENCESUPDATE

class SetCareer(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETCAREER

class SetCareers(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETCAREERS

class SetAtWorkInfo(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETATWORKINFO

class DisplayCareerTooltip(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _DISPLAYCAREERTOOLTIP

class NotifyNotebookEntryDiscovered(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _NOTIFYNOTEBOOKENTRYDISCOVERED

class SetAtWorkInfos(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETATWORKINFOS

class UpdateFindCareerInteractionAvailability(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _UPDATEFINDCAREERINTERACTIONAVAILABILITY

class EndOfWorkdayPromotion(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _ENDOFWORKDAYPROMOTION

class EndOfWorkday(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _ENDOFWORKDAY

class SetSimSleep(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETSIMSLEEP

class TravelSwitchToZone(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _TRAVELSWITCHTOZONE

class TravelBringToZone(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _TRAVELBRINGTOZONE

class TravelLiveToNhdToLive(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _TRAVELLIVETONHDTOLIVE

class SetPrimaryAspiration(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETPRIMARYASPIRATION

class SetSimGameplayFilterFx(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETSIMGAMEPLAYFILTERFX

class WhimGoal(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _WHIMGOAL

class SetCurrentWhims(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETCURRENTWHIMS

class SetWhimComplete(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETWHIMCOMPLETE

class SetWhimBucks(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETWHIMBUCKS

class SetTraits(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETTRAITS

class ChangeSimAge(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _CHANGESIMAGE

class SetAccountId(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETACCOUNTID

class SetIsNpc(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETISNPC

class SetPlayerProtectedStatus(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETPLAYERPROTECTEDSTATUS

class SetPlayedStatus(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETPLAYEDSTATUS

class SetHouseholdName(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETHOUSEHOLDNAME

class SetHouseholdDescription(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETHOUSEHOLDDESCRIPTION

class SetHouseholdHidden(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETHOUSEHOLDHIDDEN

class SetHouseholdHomeZoneId(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETHOUSEHOLDHOMEZONEID

class SetHouseholdSims(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETHOUSEHOLDSIMS

class SetRelatedObjects(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETRELATEDOBJECTS

class PreloadSimOutfit(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _PRELOADSIMOUTFIT

class OutfitTypeAndIndex(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _OUTFITTYPEANDINDEX

class SetWallsUpOrDown(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETWALLSUPORDOWN

class OverrideWallsUp(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _OVERRIDEWALLSUP

class SetCanLiveDrag(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETCANLIVEDRAG

class LiveDragStart(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _LIVEDRAGSTART

class LiveDragEnd(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _LIVEDRAGEND

class LiveDragCancel(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _LIVEDRAGCANCEL

class SetPhoneSilence(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETPHONESILENCE

class SetBabySkinTone(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETBABYSKINTONE

class SetAwayAction(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETAWAYACTION

class SetObjectDefinitionId(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETOBJECTDEFINITIONID

class FocusCamera(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _FOCUSCAMERA

class CancelFocusCamera(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _CANCELFOCUSCAMERA

class FocusCameraOnLot(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _FOCUSCAMERAONLOT

class SetSimAgeProgressTooltipData(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETSIMAGEPROGRESSTOOLTIPDATA

class MoveHouseholdIntoLotFromGallery(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _MOVEHOUSEHOLDINTOLOTFROMGALLERY

class SetOccultTypes(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETOCCULTTYPES

class SetCurrentOccultTypes(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETCURRENTOCCULTTYPES

class SetMannequinData(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETMANNEQUINDATA

class SetMannequinPose(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETMANNEQUINPOSE

class ShowFamilyTree(message.Message, metaclass=reflection.GeneratedProtocolMessageType):

    class FamilyTreeNode(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
        DESCRIPTOR = _SHOWFAMILYTREE_FAMILYTREENODE

    DESCRIPTOR = _SHOWFAMILYTREE

class CustomizableObjectData(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _CUSTOMIZABLEOBJECTDATA

class CustomizableObjectDataList(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _CUSTOMIZABLEOBJECTDATALIST

class MakeMemoryFromPhoto(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _MAKEMEMORYFROMPHOTO

class SetBuckFunds(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETBUCKFUNDS

class SetRetailFunds(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETRETAILFUNDS

class SetRetailDailyItemsSold(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETRETAILDAILYITEMSSOLD

class SetRetailDailyOutgoingCosts(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETRETAILDAILYOUTGOINGCOSTS

class SetRetailDailyNetProfit(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETRETAILDAILYNETPROFIT

class SetRetailStoreOpen(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETRETAILSTOREOPEN

class SetAura(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETAURA

class SetSimHeadline(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETSIMHEADLINE

class SetLinkedSims(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETLINKEDSIMS

class SetMulticolor(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETMULTICOLOR

class SetVFXMask(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETVFXMASK

class SetExcludeVFXMask(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETEXCLUDEVFXMASK

class StartEnsemble(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _STARTENSEMBLE

class UpdateEnsemble(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _UPDATEENSEMBLE

class EndEnsemble(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _ENDENSEMBLE

class SetDisplayNumber(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETDISPLAYNUMBER

class UpdateFlipBook(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _UPDATEFLIPBOOK

class SetOverrideDialogPitch(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETOVERRIDEDIALOGPITCH

class InitCameraShake(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _INITCAMERASHAKE

class SetCallToAction(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETCALLTOACTION

class SetScratchedOverlay(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETSCRATCHEDOVERLAY

class SendHolidayInfo(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SENDHOLIDAYINFO

class SendActiveHolidayInfo(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SENDACTIVEHOLIDAYINFO

class SetLotDecorations(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETLOTDECORATIONS

class SetAllowFame(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETALLOWFAME

class SetAllowReputation(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETALLOWREPUTATION

class DisplayHeadline(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _DISPLAYHEADLINE

class OwnedUniversityHousingLoad(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _OWNEDUNIVERSITYHOUSINGLOAD

class SplitHouseholdDialog(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SPLITHOUSEHOLDDIALOG

class OrganizationUpdate(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _ORGANIZATIONUPDATE

class OrganizationEventInfo(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _ORGANIZATIONEVENTINFO

class OrganizationEventUpdate(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _ORGANIZATIONEVENTUPDATE

class CivicPolicyPanelData(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _CIVICPOLICYPANELDATA

class SendUIMessage(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SENDUIMESSAGE

class SetTraitAtRiskState(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _SETTRAITATRISKSTATE

class ToggleCustomCamera(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _TOGGLECUSTOMCAMERA

class OpenTutorial(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _OPENTUTORIAL

class ClanMembershipUpdate(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _CLANMEMBERSHIPUPDATE

class ClanUpdate(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _CLANUPDATE

class TogglePhoneBadge(message.Message, metaclass=reflection.GeneratedProtocolMessageType):
    DESCRIPTOR = _TOGGLEPHONEBADGE
