import objects
class SetSituationSpecialObjectLootOp(BaseLootOperation):
    FACTORY_TUNABLES = {'situation': TunableReference(description='\n            The Situation to which the target object is added. If the subject Sim is not in this situation,\n            nothing will happen.\n            ', manager=services.get_instance_manager(sims4.resources.Types.SITUATION))}

    def __init__(self, situation, **kwargs):
        super().__init__(target_participant_type=ParticipantType.Object, **kwargs)
        self._situation = situation

    def _apply_to_subject_and_target(self, subject, target, resolver):
        drama_scheduler = services.drama_scheduler_service()
        for drama_node in drama_scheduler.get_scheduled_nodes_by_drama_node_type(DramaNodeType.PLAYER_PLANNED):
            situation_seed = drama_node.get_situation_seed()
            if situation_seed.situation_type.guid64 == self._situation.guid64 and situation_seed.host_sim_id == subject.id:
                situation_seed.special_object_definition_id = target.definition.id
                crafting_component = target.get_component(objects.components.types.CRAFTING_COMPONENT)
                if crafting_component is not None:
                    recipe_name = crafting_component.get_recipe().get_recipe_name()
                    situation_seed.special_object_name = recipe_name
                return
