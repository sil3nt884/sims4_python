from __future__ import annotationsfrom typing import TYPE_CHECKINGif TYPE_CHECKING:
    from typing import *
    from interactions.base.interaction import Interaction
    from sims4.tuning.tunable_hash import _Hashfrom event_testing.tests import TunableTestSetfrom interactions import ParticipantTypefrom element_utils import build_critical_section_with_finallyfrom sims4.tuning.tunable import TunableFactory, Tunable, TunableEnumFlags, TunableList, TunableTuplefrom uid import UniqueIdGeneratorimport distributor.opsimport sims4.logimport sims4.mathfrom sims4.tuning.tunable_hash import TunableStringHash32_normal_logger = sims4.log.Logger('Focus')logger = _normal_loggerid_gen = UniqueIdGenerator(1)active_focus = []
def get_next_focus_id():
    return id_gen()

def FocusPrintAll(_connection=None):
    console = sims4.log.CheatLogger(_normal_logger.group, _connection)
    for l in active_focus:
        focus_id = l[0]
        owner = l[1]
        console.info('focus: id=' + str(focus_id) + ' owner=' + str(owner))

def FocusDebug(out):
    logger.info(out)

def FocusAdd(owner_sim, focus_id, layer, score, source, target, bone, offset, blocking=True, distance_curve=None, facing_curve=None, flags=0):
    op = distributor.ops.FocusEventAdd(focus_id, layer, score, source, target, bone, offset, blocking, distance_curve, facing_curve, flags)
    distributor.ops.record(owner_sim, op)
    for l in active_focus:
        if l[0] == focus_id:
            logger.info('Focus DUPE Add: id=' + str(focus_id) + ' owner=' + str(owner_sim.id))
    active_focus.append((focus_id, owner_sim.id))
    logger.info('Focus Add: id=' + str(focus_id) + ' owner=' + str(owner_sim.id) + ' sim=' + str(source) + ' blocking=' + str(blocking) + ' score=' + str(score) + ' target=' + str(target))

def FocusDelete(owner_sim, source_id, focus_id, blocking=True):
    op = distributor.ops.FocusEventDelete(source_id, focus_id, blocking)
    distributor.ops.record(owner_sim, op)
    try:
        active_focus.remove((focus_id, owner_sim.id))
        logger.info('Focus Delete: id=' + str(focus_id) + ' owner=' + str(owner_sim.id) + ' sim=' + str(source_id) + ' blocking=' + str(blocking))
    except:
        logger.info('Focus Failed Delete: id=' + str(focus_id) + ' owner=' + str(owner_sim.id) + ' sim=' + str(source_id) + ' blocking=' + str(blocking))
        for l in active_focus:
            if l[0] == focus_id:
                active_focus.remove(l)
                return

def FocusClear(owner_sim, sim_id, blocking=True):
    op = distributor.ops.FocusEventClear(sim_id, blocking)
    distributor.ops.record(owner_sim, op)
    for l in active_focus:
        if l[1] == owner_sim.id:
            active_focus.remove(l)
    logger.info('Focus Clear: owner=' + str(sim_id))

def FocusModifyScore(owner_sim, sim_id, focus_id, score, blocking=True):
    op = distributor.ops.FocusEventModifyScore(sim_id, focus_id, score, blocking)
    distributor.ops.record(owner_sim, op)
    found = False
    for l in active_focus:
        if l[0] == focus_id:
            found = True
            if l[1] == owner_sim.id:
                logger.info('Focus Modify: id=' + str(focus_id) + ' owner=' + str(owner_sim.id) + ' sim=' + str(sim_id) + ' score=' + str(score))
            else:
                logger.info('Focus Modify WRONG OWNER: id=' + str(focus_id) + ' prev_owner=' + str(l[1]) + ' owner=' + str(owner_sim.id) + ' sim=' + str(sim_id) + ' score=' + str(score))
    if not found:
        logger.info('Focus Modify NOT FOUND: id=' + str(focus_id) + ' owner=' + str(owner_sim.id) + ' sim=' + str(sim_id) + ' score=' + str(score))

def FocusForceUpdate(owner_sim, sim_id, blocking=True):
    op = distributor.ops.FocusEventForceUpdate(sim_id, blocking)
    distributor.ops.record(owner_sim, op)
    logger.info('Focus Force Update: owner=' + str(sim_id))

def FocusDisable(owner_sim, sim_id, disable, blocking=True):
    op = distributor.ops.FocusEventDisable(sim_id, disable, blocking)
    distributor.ops.record(owner_sim, op)
    logger.info('Focus Force Disable: owner=' + str(owner_sim.id) + ' sim=' + str(sim_id))

def FocusPrint(sim, sim_id):
    op = distributor.ops.FocusEventPrint(sim_id)
    distributor.ops.record(sim, op)

class SimFocus:
    LAYER_AMBIENT = 0
    LAYER_SUPER_INTERACTION = 3
    LAYER_INTERACTION = 5
    LAYER_ALWAYSPICKFIRST = 4294967295

    def __init__(self, owner_sim, source, target, offset, record_id, bone=0, score=1.0, layer=LAYER_AMBIENT, flags=0, focus_bone_override=None):
        super().__init__()
        self._owner_sim = owner_sim
        self._record_id = record_id
        self._layer = layer
        self._score = score
        self._source_id = source.id
        self._target_id = target.id if target is not None else 0
        if focus_bone_override is not None:
            self._target_bone = focus_bone_override
        elif not hasattr(target, 'get_focus_bone'):
            logger.error('SimFocus target provided does not have get_focus_bone(): {}', target)
            self._target_bone = 0
        else:
            self._target_bone = target.get_focus_bone() if target is not None else 0
        self._offset = offset
        self._flags = flags

    def __str__(self):
        return 'Sim Focus Element'

    def begin(self, _):
        FocusAdd(self._owner_sim, self._record_id, self._layer, self._score, self._source_id, self._target_id, self._target_bone, self._offset, flags=self._flags)
        FocusForceUpdate(self._owner_sim, self._source_id)

    def end(self, _):
        FocusDelete(self._owner_sim, self._source_id, self._record_id)

def with_sim_focus(owner_sim, sim, target, layer, *args, score=1, flags=0, offset=sims4.math.Vector3.ZERO(), focus_bone_override=None):
    focus_element = SimFocus(owner_sim, sim, target, offset, get_next_focus_id(), layer=layer, score=score, flags=flags, focus_bone_override=focus_bone_override)
    return build_critical_section_with_finally(focus_element.begin, args, focus_element.end)

def without_sim_focus(owner_sim, sim, *args):
    sim_id = sim.id
    return build_critical_section_with_finally(lambda _: FocusDisable(owner_sim, sim_id, True), args, lambda _: FocusDisable(owner_sim, sim_id, False))

class TunableFocusElement(TunableFactory):

    @staticmethod
    def factory(interaction:'Interaction', subject:'ParticipantType', layer:'int', score:'int', focus_bone_override:'_Hash'=None, disable_focus:'bool'=False, focus_layer_override:'int'=None, sequence:'Sequence'=()) -> 'Sequence':
        sim = interaction.sim
        if disable_focus:
            sequence = without_sim_focus(sim, sim, sequence)
            return sequence
        if focus_layer_override is not None:
            layer = focus_layer_override
        elif layer is None:
            layer = SimFocus.LAYER_SUPER_INTERACTION if interaction.is_super else SimFocus.LAYER_INTERACTION
        for obj in interaction.get_participants(subject):
            sequence = with_sim_focus(sim, sim, obj, layer, sequence, focus_bone_override=focus_bone_override, score=score)
            sequence = with_sim_focus(sim, obj, sim, layer, sequence, focus_bone_override=focus_bone_override, score=score)
        return sequence

    FACTORY_TYPE = factory

    def __init__(self, description="Configure focus on one or more of an interaction's participants.", **kwargs) -> 'None':
        super().__init__(subject=TunableEnumFlags(ParticipantType, ParticipantType.Object, description='Who or what to focus on.'), layer=Tunable(int, None, description='Layer override: Ambient=0, SuperInteraction=3, Interaction=5.'), score=Tunable(int, 1, description='Focus score.  This orders focus elements in the same layer.'), focus_bone_override=TunableStringHash32(description='The bone Sims direct their attention towards when focusing on an object.'), disable_focus=Tunable(bool, False, description='If True, we disable the focus for the interaction participants.'), description=description, **kwargs)

class TestedTunableFocusElement(TunableFactory):

    @staticmethod
    def factory(interaction:'Interaction', tested_focus_list:'Tuple', sequence:'Sequence'=()) -> 'Sequence':
        resolver = interaction.get_resolver()
        for entry in tested_focus_list:
            if entry.tests.run_tests(resolver):
                sequence = entry.tunable_focus(interaction, sequence=sequence)
                break
        return sequence

    FACTORY_TYPE = factory

    def __init__(self, description='The first tunable focus whose tests pass will be applied.', **kwargs) -> 'None':
        super().__init__(tested_focus_list=TunableList(tunable=TunableTuple(tests=TunableTestSet(description='\n                        If tests pass, apply the tunable focus on the interaction participants.\n                        '), tunable_focus=TunableFocusElement(description="\n                        The tunable focus element to apply if this entry's tests pass.\n                        "))), description=description, **kwargs)
