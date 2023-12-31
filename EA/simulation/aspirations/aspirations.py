import collectionsimport event_testing.event_data_tracker as data_trackerimport event_testing.test_events as test_eventsimport gsi_handlers.aspiration_handlersimport servicesimport sims4.logimport telemetry_helperimport weakreffrom aspirations.aspiration_types import AspriationTypefrom distributor.ops import GenericProtocolBufferOpfrom distributor.rollback import ProtocolBufferRollbackfrom distributor.shared_messages import IconInfoDatafrom distributor.system import Distributorfrom event_testing.resolver import SingleSimResolver, DataResolverfrom event_testing.test_events import TestEventfrom interactions import ParticipantTypefrom protocolbuffers import Sims_pb2from protocolbuffers.DistributorOps_pb2 import Operation, SetWhimBucksfrom sims.sim_info_lod import SimInfoLODLevelfrom sims.sim_info_tracker import SimInfoTrackerfrom sims4.localization import LocalizationHelperTuningfrom sims4.utils import classpropertylogger = sims4.log.Logger('Aspirations')TELEMETRY_GROUP_ASPIRATIONS = 'ASPR'TELEMETRY_HOOK_ADD_ASPIRATIONS = 'AADD'TELEMETRY_HOOK_COMPLETE_MILESTONE = 'MILE'TELEMETRY_OBJECTIVE_ID = 'obid'writer = sims4.telemetry.TelemetryWriter(TELEMETRY_GROUP_ASPIRATIONS)
class AspirationTracker(data_tracker.EventDataTracker, SimInfoTracker):

    class _AdditionalObjectiveData:

        def __init__(self, objectives, owner=None):
            self.objectives = objectives
            self.owner = owner

    def __init__(self, sim_info):
        super().__init__()
        self._owner_ref = weakref.ref(sim_info)
        self._selected_aspiration = 0
        self._whimsets_to_reset = set()
        self._active_aspiration = None
        self._timed_aspirations = {}
        self._additional_objectives = {}

    def _get_milestone_manager(self):
        return services.get_instance_manager(sims4.resources.Types.ASPIRATION)

    @property
    def active_track(self):
        return self.owner_sim_info.primary_aspiration

    def get_additional_objectives(self, aspiration):
        objective_data = self._additional_objectives.get(aspiration, None)
        if objective_data is None:
            return []
        return objective_data.objectives

    def validate_and_return_completed_status(self, aspiration, aspiration_track=None):
        aspiration_completed = aspiration in self._completed_milestones
        for objective in self.get_objectives(aspiration):
            if not self.objective_completed(objective):
                if aspiration_completed:
                    self.complete_objective(objective, aspiration)
                else:
                    return False
        if not aspiration_completed:
            self._completed_milestones.add(aspiration)
            if aspiration_track is not None:
                self._check_and_complete_aspiration_track(aspiration_track, aspiration.guid64, self.owner_sim_info)
        return True

    def register_additional_objectives(self, aspiration, objectives, replace_completed_objective=False, owner=None):
        if aspiration in self._additional_objectives:
            addtl_obj = self._additional_objectives[aspiration]
            if addtl_obj.owner is not None and owner is not None and addtl_obj.owner is not owner:
                logger.error('Trying to register additional objectives but getting an owner mismatch.\nAspiration: {}\nCurrent Owner: {}\nNew Owner: {}', aspiration, addtl_obj.owner, owner)
                return
            if owner is not None:
                addtl_obj.owner = owner
            new_objectives = [objective for objective in objectives if objective not in addtl_obj.objectives]
            current_additional_objectives = list(addtl_obj.objectives)
            if addtl_obj.owner is None and replace_completed_objective:
                self._replace_completed_objective(current_additional_objectives, new_objectives)
            else:
                current_additional_objectives.extend(new_objectives)
            addtl_obj.objectives = tuple(current_additional_objectives)
            return new_objectives
        else:
            self._additional_objectives[aspiration] = self._AdditionalObjectiveData(objectives, owner=owner)
            return objectives

    def _replace_completed_objective(self, current_objectives, new_objectives):
        remaining_objectives = list(new_objectives)
        for existing_objective in current_objectives:
            if len(remaining_objectives) == 0:
                break
            if not self.objective_completed(existing_objective):
                pass
            else:
                completed_objective_index = current_objectives.index(existing_objective)
                current_objectives[completed_objective_index] = remaining_objectives.pop()
        if len(remaining_objectives) > 0:
            current_objectives.append(remaining_objectives)

    def _activate_aspiration(self, aspiration, from_load=False):
        if from_load or self._active_aspiration is aspiration:
            return
        self._active_aspiration = aspiration
        aspiration.register_callbacks(additional_objectives=self.get_additional_objectives(aspiration))
        self.clear_objective_updates_cache(aspiration)
        self.process_test_events_for_aspiration(aspiration)
        self._send_objectives_update_to_client()
        self._send_tracker_to_client()

    def initialize_aspiration(self, from_load=False):
        if self.owner_sim_info is not None and not self.owner_sim_info.is_baby:
            track = self.active_track
            if track is not None:
                for (_, track_aspriation) in track.get_aspirations():
                    if not self.validate_and_return_completed_status(track_aspriation, track):
                        self._activate_aspiration(track_aspriation, from_load=from_load)
                        break
                services.get_event_manager().process_event(test_events.TestEvent.AspirationTrackSelected, sim_info=self.owner_sim_info)

    def process_test_events_for_aspiration(self, aspiration):
        event_manager = services.get_event_manager()
        event_manager.register_single_event(aspiration, TestEvent.UpdateObjectiveData)
        event_manager.process_test_events_for_objective_updates(self.owner_sim_info)
        event_manager.unregister_single_event(aspiration, TestEvent.UpdateObjectiveData)

    @property
    def owner_sim_info(self):
        return self._owner_ref()

    def aspiration_in_sequence(self, aspiration):
        return aspiration is self._active_aspiration

    def _should_handle_event(self, milestone, event, resolver:DataResolver):
        if not super()._should_handle_event(milestone, event, resolver):
            return False
        aspiration = milestone
        if aspiration.aspiration_type == AspriationType.FULL_ASPIRATION and aspiration.do_not_register_events_on_load:
            return self.aspiration_in_sequence(aspiration)
        if aspiration.aspiration_type == AspriationType.TIMED_ASPIRATION:
            return aspiration in self._timed_aspirations
        if aspiration.aspiration_type == AspriationType.CAREER:
            actor = resolver.get_participant(ParticipantType.Actor)
            if actor is None or not actor.is_sim:
                return False
            career_tracker = actor.sim_info.career_tracker
            if career_tracker is None:
                return False
            else:
                return milestone in career_tracker.get_all_career_aspirations()
        return True

    def _should_test_objective(self, aspiration, objective):
        objective_data = self._additional_objectives.get(aspiration, None)
        if objective_data is None or objective not in objective_data.objectives or objective_data.owner is None:
            return True
        return objective_data.owner.should_test_objective(objective)

    def gsi_event(self, event):
        return {'sim': self._owner_ref().full_name if self._owner_ref() is not None else 'None', 'event': str(event)}

    def post_to_gsi(self, message):
        gsi_handlers.aspiration_handlers.archive_aspiration_event_set(message)

    def unlock_hidden_aspiration_track(self, hidden_aspiration_track):
        self._unlocked_hidden_aspiration_tracks.add(hidden_aspiration_track)
        self._send_tracker_to_client()

    def is_aspiration_track_visible(self, aspriration_track):
        if not aspriration_track.is_hidden_unlockable:
            return True
        return aspriration_track.guid64 in self._unlocked_hidden_aspiration_tracks

    def _send_tracker_to_client(self, init=False):
        owner = self.owner_sim_info
        if owner is None or owner.is_npc or owner.manager is None:
            return
        msg_empty = True
        msg = Sims_pb2.AspirationTrackerUpdate()
        for aspiration in self._completed_milestones:
            if not self.milestone_sent(aspiration):
                self._sent_milestones.add(aspiration)
                msg.aspirations_completed.append(aspiration.guid64)
                msg_empty = False
        for objective in self._completed_objectives:
            if not self.objective_sent(objective):
                self._sent_objectives.add(objective)
                msg.objectives_completed.append(objective.guid64)
                msg_empty = False
        for objective in self._reset_objectives:
            if not self.objective_sent(objective):
                self._sent_objectives.add(objective)
                msg.objectives_reset.append(objective.guid64)
                msg_empty = False
        for unlocked_hidden_aspiration_track in self._unlocked_hidden_aspiration_tracks:
            if not self.unlocked_hidden_aspiration_track_sent(unlocked_hidden_aspiration_track):
                msg.unlocked_hidden_aspiration_tracks.append(unlocked_hidden_aspiration_track.guid64)
                msg_empty = False
        if not msg_empty:
            msg.sim_id = owner.id
            msg.init_message = init
            distributor = Distributor.instance()
            distributor.add_op(owner, GenericProtocolBufferOp(Operation.SIM_ASPIRATION_TRACKER_UPDATE, msg))

    def _send_objectives_update_to_client(self):
        owner = self.owner_sim_info
        if owner is None or owner.is_npc or owner.manager is None:
            return
        msg = Sims_pb2.GoalsStatusUpdate()
        if self._update_objectives_msg_for_client(msg):
            msg.sim_id = owner.id
            cheat_service = services.get_cheat_service()
            msg.cheats_used = cheat_service.cheats_ever_enabled
            distributor = Distributor.instance()
            distributor.add_op(owner, GenericProtocolBufferOp(Operation.SIM_GOALS_STATUS_UPDATE, msg, block_on_task_owner=False))

    def _check_and_complete_aspiration_track(self, aspiration_track, completed_aspiration_id, sim_info):
        if all(self.milestone_completed(track_aspiration) for track_aspiration in aspiration_track.aspirations.values()):
            if aspiration_track.reward is not None:
                reward_payout = aspiration_track.reward.give_reward(sim_info)
            else:
                reward_payout = ()
            reward_text = LocalizationHelperTuning.get_bulleted_list((None,), (reward.get_display_text(SingleSimResolver(sim_info)) for reward in reward_payout))
            dialog = aspiration_track.notification(sim_info, SingleSimResolver(sim_info))
            dialog.show_dialog(icon_override=IconInfoData(icon_resource=aspiration_track.icon), secondary_icon_override=IconInfoData(obj_instance=sim_info), additional_tokens=(reward_text,), event_id=completed_aspiration_id)

    def complete_milestone(self, aspiration, sim_info):
        aspiration_type = aspiration.aspiration_type
        if aspiration_type == AspriationType.FULL_ASPIRATION:
            if not aspiration.is_valid_for_sim(sim_info):
                return
            super().complete_milestone(aspiration, sim_info)
            if aspiration.reward is not None:
                aspiration.reward.give_reward(sim_info)
            track = self.active_track
            if track is None:
                if not sim_info.is_toddler:
                    logger.error('Active track is None when completing full aspiration {} for sim {}.', aspiration, sim_info)
                return
            if aspiration.screen_slam is not None:
                if aspiration in track.aspirations.values():
                    aspiration.screen_slam.send_screen_slam_message(sim_info, sim_info, aspiration.display_name, track.display_text)
                else:
                    aspiration.screen_slam.send_screen_slam_message(sim_info, sim_info, aspiration.display_name)
            if aspiration in track.aspirations.values():
                self._check_and_complete_aspiration_track(track, aspiration, sim_info)
                aspiration.apply_on_complete_loot_actions(sim_info)
                next_aspiration = track.get_next_aspriation(aspiration)
                if next_aspiration is not None:
                    for objective in self.get_objectives(next_aspiration):
                        if objective.set_starting_point(self.data_object):
                            self.update_objective(objective, 0, objective.goal_value(), objective.is_goal_value_money, objective.show_progress)
                    self._activate_aspiration(next_aspiration)
                else:
                    self._active_aspiration = None
                with telemetry_helper.begin_hook(writer, TELEMETRY_HOOK_COMPLETE_MILESTONE, sim=sim_info.get_sim_instance()) as hook:
                    hook.write_enum('type', aspiration.aspiration_type)
                    hook.write_guid('guid', aspiration.guid64)
            services.get_event_manager().process_event(test_events.TestEvent.UnlockEvent, sim_info=sim_info, unlocked=aspiration)
        elif aspiration_type == AspriationType.FAMILIAL:
            super().complete_milestone(aspiration, sim_info)
            for relationship in aspiration.target_family_relationships:
                family_member_sim_id = sim_info.get_relation(relationship)
                family_member_sim_info = services.sim_info_manager().get(family_member_sim_id)
                if family_member_sim_info is not None:
                    services.get_event_manager().process_event(test_events.TestEvent.FamilyTrigger, sim_info=family_member_sim_info, trigger=aspiration)
        elif aspiration_type == AspriationType.WHIM_SET:
            self._whimsets_to_reset.add(aspiration)
            super().complete_milestone(aspiration, sim_info)
            whim_tracker = sim_info.whim_tracker
            if whim_tracker is not None:
                whim_tracker.activate_whimset_from_objective_completion(aspiration)
        elif aspiration_type == AspriationType.NOTIFICATION:
            tutorial_service = services.get_tutorial_service()
            if tutorial_service is None or not tutorial_service.is_tutorial_running():
                dialog = aspiration.notification(sim_info, SingleSimResolver(sim_info))
                dialog.show_dialog(event_id=aspiration.guid64)
            super().complete_milestone(aspiration, sim_info)
        elif aspiration_type == AspriationType.ASSIGNMENT:
            super().complete_milestone(aspiration, sim_info)
            aspiration.satisfy_assignment(sim_info)
        elif aspiration_type == AspriationType.GIG:
            super().complete_milestone(aspiration, sim_info)
            aspiration.satisfy_assignment(sim_info)
        elif aspiration_type == AspriationType.ZONE_DIRECTOR:
            super().complete_milestone(aspiration, sim_info)
            zone_director = services.venue_service().get_zone_director()
            zone_director.on_zone_director_aspiration_completed(aspiration, sim_info)
        elif aspiration_type == AspriationType.TIMED_ASPIRATION:
            super().complete_milestone(aspiration, sim_info)
            self._timed_aspirations[aspiration].complete()
        elif aspiration_type == AspriationType.CAREER:
            super().complete_milestone(aspiration, sim_info)
            if aspiration.screen_slam is not None:
                aspiration.screen_slam.send_screen_slam_message(sim_info, sim_info)
        else:
            super().complete_milestone(aspiration, sim_info)
        services.get_event_manager().process_event(TestEvent.MilestoneCompleted, sim_info=sim_info)

    def post_completion_ui_update(self, aspiration, sim_info):
        super().post_completion_ui_update(aspiration, sim_info)
        if sim_info is not self._owner_ref():
            logger.error('Sim Info for this milestone is not the same provided for this tracker.', owner='nabaker')
            return
        if aspiration.aspiration_type == AspriationType.ASSIGNMENT:
            aspiration.send_assignment_update(sim_info)

    def update_objectives_after_ui_change(self, objective_instances):
        super().update_objectives_after_ui_change(objective_instances)
        owner = self._owner_ref()
        if owner is not None:
            for objective in objective_instances:
                objective.apply_loot_on_completion_ui_update(owner)

    def complete_objective(self, objective_instance, aspiration):
        result = super().complete_objective(objective_instance, aspiration)
        objective_data = self._additional_objectives.get(aspiration, None)
        if objective_data.owner is not None:
            result = objective_data.owner.complete_objective(objective_instance)
        owner = self._owner_ref()
        if objective_data is not None and owner is not None:
            objective_instance.apply_completion_loot(owner)
            if objective_instance.satisfaction_points > 0:
                owner.apply_satisfaction_points_delta(objective_instance.satisfaction_points, SetWhimBucks.ASPIRATION, source=objective_instance.guid64)
        return result

    def reset_milestone(self, completed_milestone, objectives=()):
        for objective in self.get_objectives(completed_milestone):
            self._try_reset_objective(objective)
        if completed_milestone in self._additional_objectives:
            for objective in self._additional_objectives[completed_milestone].objectives:
                self._try_reset_objective(objective)
            del self._additional_objectives[completed_milestone]
        for objective in objectives:
            self._try_reset_objective(objective)
        super().reset_milestone(completed_milestone)

    def _try_reset_objective(self, objective):
        if objective.resettable:
            objective.reset_objective(self.data_object)
            self.reset_objective(objective)
            self.update_objective(objective, 0, objective.goal_value(), objective.is_goal_value_money, objective.show_progress)
            self._send_objectives_update_to_client()

    def _update_timer_alarm(self, _):
        sim_info = self.owner_sim_info
        if sim_info is None:
            self.clear_update_alarm()
            logger.error('No Sim info in AspirationTracker._update_timer_alarm')
            return
        self.update_timers()
        if sim_info.is_selected:
            services.get_event_manager().process_event(test_events.TestEvent.TestTotalTime, sim_info=sim_info)

    def save(self, blob=None):
        for whim_set in self._whimsets_to_reset:
            self.reset_milestone(whim_set)
        blob.ClearField('unlocked_hidden_aspiration_tracks')
        unlocked_hidden_aspiration_tracks = set(blob.unlocked_hidden_aspiration_tracks) | {unlocked_hidden_aspiration_track.guid64 for unlocked_hidden_aspiration_track in self._unlocked_hidden_aspiration_tracks}
        blob.unlocked_hidden_aspiration_tracks.extend(unlocked_hidden_aspiration_tracks)
        blob.ClearField('timed_aspirations')
        for timed_aspiration_data in self._timed_aspirations.values():
            with ProtocolBufferRollback(blob.timed_aspirations) as msg:
                timed_aspiration_data.save(msg)
        blob.ClearField('additional_objectives')
        for (aspiration, data) in self._additional_objectives.items():
            with ProtocolBufferRollback(blob.additional_objectives) as add_obj_data:
                add_obj_data.milestone_guid = aspiration.guid64
                add_obj_data.objective_guids.extend([obj.guid64 for obj in data.objectives])
        super().save(blob)

    def load(self, blob=None):
        aspiration_track_manager = services.get_instance_manager(sims4.resources.Types.ASPIRATION_TRACK)
        if blob is not None:
            for unlocked_hidden_aspiration_track_id in blob.unlocked_hidden_aspiration_tracks:
                unlocked_hidden_aspiration_track = aspiration_track_manager.get(unlocked_hidden_aspiration_track_id)
                if unlocked_hidden_aspiration_track is not None and unlocked_hidden_aspiration_track.is_available():
                    self._unlocked_hidden_aspiration_tracks.add(unlocked_hidden_aspiration_track)
            aspiration_manager = services.get_instance_manager(sims4.resources.Types.ASPIRATION)
            for timed_aspiration_msg in blob.timed_aspirations:
                aspiration = aspiration_manager.get(timed_aspiration_msg.aspiration)
                if aspiration is None:
                    pass
                else:
                    timed_aspiration_data = aspiration.generate_aspiration_data(self, aspiration)
                    if timed_aspiration_data.load(timed_aspiration_msg):
                        self._timed_aspirations[aspiration] = timed_aspiration_data
            self._additional_objectives = {}
            objective_manager = services.get_instance_manager(sims4.resources.Types.OBJECTIVE)
            for additional_objective_data in blob.additional_objectives:
                aspiration = aspiration_manager.get(additional_objective_data.milestone_guid)
                if aspiration is None:
                    pass
                else:
                    objectives = []
                    for objective_guid in additional_objective_data.objective_guids:
                        objective = objective_manager.get(objective_guid)
                        if objective is None:
                            pass
                        else:
                            objectives.append(objective)
                    if not objectives:
                        pass
                    else:
                        self.register_additional_objectives(aspiration, objectives)
        super().load(blob=blob)

    def force_send_data_update(self):
        for aspiration in services.get_instance_manager(sims4.resources.Types.ASPIRATION).types.values():
            aspiration_type = aspiration.aspiration_type
            if aspiration_type != AspriationType.FULL_ASPIRATION and aspiration_type != AspriationType.SIM_INFO_PANEL:
                pass
            else:
                for objective in self.get_objectives(aspiration):
                    self.update_objective(objective, 0, objective.goal_value(), objective.is_goal_value_money, objective.show_progress, from_init=True)
                    self._tracker_dirty = True
        self.send_if_dirty()

    @classproperty
    def _tracker_lod_threshold(cls):
        return SimInfoLODLevel.ACTIVE

    def on_lod_update(self, old_lod, new_lod):
        if new_lod == SimInfoLODLevel.ACTIVE:
            sim_msg = services.get_persistence_service().get_sim_proto_buff(self.owner_sim_info.id)
            if sim_msg is not None:
                self.load(sim_msg.attributes.event_data_tracker)
        else:
            sim_msg = services.get_persistence_service().get_sim_proto_buff(self.owner_sim_info.id)
            sim_msg.attributes.event_data_tracker.Clear()
            self.save(sim_msg.attributes.event_data_tracker)
            self.clear_update_alarm()

    def clean_up(self):
        for timed_aspriation_data in self._timed_aspirations.values():
            timed_aspriation_data.clear()
        self.reset_data()
        self.clear_update_alarm()
        self._timed_aspirations.clear()

    def on_zone_load(self):
        self.clear_tracked_client_data()
        self.send_event_data_to_client()
        for timed_aspriation_data in self._timed_aspirations.values():
            timed_aspriation_data.send_timed_aspiration_to_client(Sims_pb2.TimedAspirationUpdate.ADD)

    def on_zone_unload(self):
        self.clear_tracked_client_data()

    def setup_timed_aspiration(self, aspiration, from_load=False):
        if not from_load:
            self.reset_milestone(aspiration)
        additional_objectives = () if aspiration not in self._additional_objectives else self._additional_objectives[aspiration].objectives
        aspiration.setup_aspiration(self, additional_objectives)
        self.clear_objective_updates_cache(aspiration)
        self.process_test_events_for_aspiration(aspiration)
        self._send_objectives_update_to_client()
        self._send_tracker_to_client()

    def deactivate_aspiration(self, aspiration):
        aspiration.cleanup_aspiration(self)

    def get_timed_aspiration_data(self, aspiration):
        return self._timed_aspirations.get(aspiration)

    def update_org_id_timed_aspiration(self, aspiration, org_id):
        if aspiration not in self._timed_aspirations:
            timed_aspiration_data = self._timed_aspirations.get(aspiration)
            timed_aspiration_data.set_org_id(org_id)

    def activate_timed_aspiration(self, aspiration, **kwargs):
        if aspiration.aspiration_type != AspriationType.TIMED_ASPIRATION:
            logger.error('Attempting to activate aspiration {} as a timed aspiration, which it is not.', aspiration)
            return
        if aspiration in self._timed_aspirations:
            logger.error('Attempting to activate aspiration {} when a timed aspiration of that type is already scheduled.', aspiration)
            return
        timed_aspiration_data = aspiration.generate_aspiration_data(self, aspiration, **kwargs)
        self._timed_aspirations[aspiration] = timed_aspiration_data
        timed_aspiration_data.schedule()

    def activate_timed_aspirations_from_load(self):
        for aspiration in self._timed_aspirations:
            self.setup_timed_aspiration(aspiration, from_load=True)

    def aspiration_in_timed_aspirations(self, aspiration):
        return aspiration in self._timed_aspirations

    def deactivate_timed_aspiration(self, aspiration, from_complete=False, **kwargs):
        if aspiration not in self._timed_aspirations:
            logger.error("Attempting to deactivate timed aspiration {} when it isn't active.")
            return
        self._timed_aspirations[aspiration].clear(from_complete=from_complete)
        del self._timed_aspirations[aspiration]

    def remove_invalid_aspirations(self):
        resolver = SingleSimResolver(self.owner_sim_info)
        for timed_aspiration in tuple(self._timed_aspirations.keys()):
            result = timed_aspiration.tests.run_tests(resolver)
            if result:
                pass
            else:
                self.deactivate_timed_aspiration(timed_aspiration)
                timed_aspiration.apply_on_cancel_loot_actions(self.owner_sim_info)
