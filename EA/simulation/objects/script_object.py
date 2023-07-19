from _collections import defaultdictfrom _sims4_collections import frozendictimport itertoolsimport timefrom animation.animation_overrides_tuning import TunableParameterMappingfrom animation.animation_utils import AnimationOverridesfrom animation.focus.focus_component import FocusComponentfrom animation.tunable_animation_overrides import TunableAnimationOverrides, TunableAnimationObjectOverridesfrom autonomy.autonomy_component import AutonomyComponentfrom balloon.tunable_balloon import TunableBalloonfrom build_buy import get_object_placement_flags, PlacementFlags, WALL_OBJECT_POSITION_PADDINGfrom caches import cachedfrom carry.carry_postures import CarryingObjectfrom carry.carry_utils import get_carried_objects_genfrom crafting.crafting_tunable import CraftingTuningfrom curfew.curfew_component import CurfewComponentfrom curfew.curfew_service import CurfewServicefrom distributor.rollback import ProtocolBufferRollbackfrom interactions.aop import AffordanceObjectPairfrom interactions.base.basic import AFFORDANCE_LOADED_CALLBACK_STRfrom interactions.constraints import Constraintfrom interactions.utils.routing import RouteTargetTypefrom lunar_cycle.lunar_phase_aware_component import LunarPhaseAwareComponentfrom narrative.narrative_aware_component import NarrativeAwareComponentfrom objects import slotsfrom objects.base_object import BaseObject, ResetReasonfrom objects.collection_manager import CollectableComponentfrom objects.components import forward_to_components_gen, forward_to_components, get_component_priority_and_name_using_persist_id, component_definitionfrom objects.components.affordance_tuning import AffordanceTuningComponentfrom objects.components.animal_home_component import AnimalHomeComponentfrom objects.components.animal_object_component import AnimalObjectComponentfrom objects.components.animal_preference_component import AnimalPreferenceComponentfrom objects.components.autonomy_marker_component import AutonomyMarkerComponentfrom objects.components.camera_view_component import CameraViewComponentfrom objects.components.canvas_component import CanvasComponent, FamilyPortraitComponent, SimPortraitComponent, PhotoboothPortraitComponentfrom objects.components.carryable_component import CarryableComponentfrom objects.components.censor_grid_component import TunableCensorGridComponentfrom objects.components.consumable_component import ConsumableComponentfrom objects.components.crafting_station_component import CraftingStationComponentfrom objects.components.display_component import DisplayComponentfrom objects.components.fishing_location_component import FishingLocationComponentfrom objects.components.flowing_puddle_component import FlowingPuddleComponentfrom objects.components.footprint_component import HasFootprintComponentfrom objects.components.game_component import GameComponentfrom objects.components.idle_component import IdleComponentfrom objects.components.inventory_item import InventoryItemComponentfrom objects.components.lighting_component import LightingComponentfrom objects.components.line_of_sight_component import TunableLineOfSightComponentfrom objects.components.linked_object_component import LinkedObjectComponentfrom objects.components.live_drag_target_component import LiveDragTargetComponentfrom objects.components.locking_components import ObjectLockingComponentfrom objects.components.mannequin_component import MannequinComponentfrom objects.components.name_component import NameComponentfrom objects.components.object_age import TunableObjectAgeComponentfrom objects.components.object_inventory_component import ObjectInventoryComponentfrom objects.components.object_marketplace_component import ObjectMarketplaceComponentfrom objects.components.object_fashion_marketplace_component import ObjectFashionMarketplaceComponentfrom objects.components.object_relationship_component import ObjectRelationshipComponentfrom objects.components.object_teleportation_component import ObjectTeleportationComponentfrom objects.components.ownable_component import OwnableComponentfrom objects.components.owning_household_component import OwningHouseholdComponentfrom objects.components.privacy_component import PrivacyComponentfrom objects.components.procedural_animation_component import ProceduralAnimationComponentfrom objects.components.proximity_component import ProximityComponentfrom objects.components.routing_component import RoutingComponentfrom objects.components.situation_scheduler_component import SituationSchedulerComponentfrom objects.components.slot_component import SlotComponentfrom objects.components.spawner_component import SpawnerComponentfrom objects.components.state import TunableStateComponentfrom objects.components.state_references import TunableStateValueReferencefrom objects.components.statistic_component import HasStatisticComponentfrom objects.components.stereo_component import TunableStereoComponentSnippetfrom objects.components.stolen_component import StolenComponentfrom objects.components.stored_audio_component import StoredAudioComponentfrom objects.components.time_of_day_component import TimeOfDayComponentfrom objects.components.tooltip_component import TooltipComponentfrom objects.components.vehicle_component import VehicleComponentfrom objects.components.video import VideoComponentfrom objects.gallery_tuning import ContentSourcefrom objects.game_object_properties import GameObjectTuningfrom objects.gardening.gardening_component_variant import TunableGardeningComponentVariantfrom objects.object_enums import ItemLocation, PersistenceTypefrom objects.parts.part_data import TunablePartDataMappingfrom objects.persistence_groups import PersistenceGroupsfrom objects.slots import SlotTypefrom protocolbuffers import SimObjectAttributes_pb2 as protocolsfrom protocolbuffers.FileSerialization_pb2 import ObjectDatafrom retail.retail_component import TunableRetailComponentSnippetfrom routing import SurfaceType, SurfaceIdentifierfrom routing.portals.portal_component import PortalComponentfrom seasons.season_aware_component import SeasonAwareComponentfrom sims.household_utilities.utility_types import Utilitiesfrom sims.favorites.favorites_tunables import FavoritePropAnimationOverridesfrom sims.university.university_scholarship_letter_component import ScholarshipLetterComponentfrom sims4.localization import TunableLocalizedStringfrom sims4.math import MAX_FLOATfrom sims4.tuning.geometric import TunableVector2from sims4.tuning.instance_manager import GET_TUNING_SUGGESTIONSfrom sims4.tuning.instances import HashedTunedInstanceMetaclassfrom sims4.tuning.tunable import TunableList, TunableReference, TunableTuple, OptionalTunable, Tunable, TunableEnumEntry, TunableMapping, TunableSet, TunableEnumWithFilter, TunableRange, TunableVariantfrom sims4.tuning.tunable_base import GroupNames, FilterTagfrom sims4.utils import flexmethod, classpropertyfrom singletons import EMPTY_SETfrom statistics.mood import TunableEnvironmentScoreModifiersfrom tag import Tagfrom weather.weather_aware_component import WeatherAwareComponentfrom whims.whim_component import WhimComponentfrom world.spawn_point_component import SpawnPointComponentfrom zone_modifier.zone_modifier_component import ZoneModifierComponentimport build_buyimport cachesimport distributor.fieldsimport indexed_managerimport objects.components.typesimport objects.persistence_groupsimport posturesimport protocolbuffers.FileSerialization_pb2 as file_serializationimport routingimport servicesimport sims4.loglogger = sims4.log.Logger('Objects')COMMODITY_FLAGS_FROM_COMPONENTS_KEY = 'component_commodities'