import date_and_time
    sub_schema.add_field('household_id', label='Household ID', width=0.35)
    sub_schema.add_field('known_preferences', label='Known Preferences', width=0.4)
    sub_schema.add_field('general_cooldown', label='General Readiness', width=0.4)
    sub_schema.add_field('category_cooldown', label='Not Ready Categories', width=0.4)
@GsiHandler('animal_preferences', animal_preferences_schema)
def generate_animal_preferences_data():
    animal_preferences = []
    object_manager = services.object_manager()
    if object_manager is None:
        return animal_preferences
    for animal_obj in object_manager.get_all_objects_with_component_gen(ANIMAL_PREFERENCE_COMPONENT):
        preference_comp = animal_obj.animalpreference_component
        if preference_comp is None:
            pass
        else:
            entry = {'animal': str(animal_obj), 'like_preferences': trim_tags(*preference_comp.like_preferences), 'dislike_preferences': trim_tags(*preference_comp.dislike_preferences), 'favorite_preference': trim_tags(preference_comp.favorite_preference)}
            knowledge_info = []
            entry['knowledge'] = knowledge_info
            for (household_id, knowledge) in preference_comp.household_knowledge_dictionary.items():
                known_preferences = trim_tags(*knowledge.known_tags)
                is_general_ready = 'READY' if knowledge.check_general_gift_readiness() else 'NOT READY'
                not_ready_categories = []
                for (category, time) in knowledge.category_gift_timestamps.items():
                    if time > date_and_time.DATE_AND_TIME_ZERO:
                        not_ready_categories.append(category)
                knowledge_info.append({'household_id': str(household_id), 'known_preferences': known_preferences, 'general_cooldown': is_general_ready, 'category_cooldown': trim_tags(*not_ready_categories)})
            animal_preferences.append(entry)
    return animal_preferences

def trim_tags(*args):
    result = ''
    first = True
    for long_tag in args:
        if not first:
            result += ', '
        tag = str(long_tag)
        tag = tag.lstrip('Tag.Func')
        tag = tag.lstrip('_')
        first = False
        result += tag
    return result
