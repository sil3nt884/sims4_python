import services
class NotebookEntryCountryItem(NotebookEntry):
    INSTANCE_TUNABLES = {'entry_text_value': TunableLocalizedStringFactory(description="\n            The text used to display the item's value. First (only) token is price of object.\n            "), 'entry_text_flavor': TunableLocalizedString(description='\n            The text to display the flavor text for the item.\n            '), 'entry_text_description': TunableLocalizedString(description="\n            The text to display the item's description.\n            ")}
    REMOVE_INSTANCE_TUNABLES = ('entry_text', 'entry_icon', 'entry_sublist')

    def is_definition_based(self):
        return True

    def get_definition_notebook_data(self, ingredient_cache=()):
        definition_manager = services.definition_manager()
        country_item_definition = definition_manager.get(self.entry_object_definition_id)
        concatenated_text = LocalizationHelperTuning.get_new_line_separated_strings(self.entry_text_value(country_item_definition.price), self.entry_text_flavor, self.entry_text_description)
        sub_list_data = []
        sub_list_data.append(SubListData(None, 0, 0, True, False, concatenated_text, None, None))
        entry_data = EntryData(LocalizationHelperTuning.get_object_name(country_item_definition), IconInfoData(obj_def_id=country_item_definition.id), None, sub_list_data, None)
        return entry_data

    def has_identical_entries(self, entries):
        for entry in entries:
            if entry.entry_object_definition_id == self.entry_object_definition_id:
                return True
        return False

class NotebookEntryCountryItemSansDefinition(NotebookEntry):
    INSTANCE_TUNABLES = {'entry_text_value': TunableLocalizedString(description="\n            The text used to display the item's value.\n            "), 'entry_text_flavor': TunableLocalizedString(description='\n            The text to display the flavor text for the item.\n            '), 'entry_text_description': TunableLocalizedString(description="\n            The text to display the item's description.\n            "), 'entry_icon_definition': TunableReference(description='\n            The definition that will be used to create the icon for\n            this entry.\n            ', manager=services.definition_manager())}
    REMOVE_INSTANCE_TUNABLES = ('entry_icon', 'entry_sublist')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.entry_object_definition_id = self.entry_icon_definition.id

    def is_definition_based(self):
        return True

    def get_definition_notebook_data(self, ingredient_cache=()):
        concatenated_text = LocalizationHelperTuning.get_new_line_separated_strings(self.entry_text_value, self.entry_text_flavor, self.entry_text_description)
        sub_list_data = []
        sub_list_data.append(SubListData(None, 0, 0, True, False, concatenated_text, None, None))
        entry_data = EntryData(self.entry_text, IconInfoData(obj_def_id=self.entry_icon_definition.id), None, sub_list_data, None)
        return entry_data

class NotebookEntryAnimalFeed(NotebookEntryRecipe):
    INSTANCE_TUNABLES = {'entry_text_flavor': TunableLocalizedString(description='\n            The text to display the flavor text for the item.\n            '), 'entry_text_description': TunableLocalizedString(description="\n            The text to display the item's description.\n            "), 'entry_text_rarity': TunableLocalizedString(description='\n            The text to display for rarity.\n            ')}

    def _get_entry_tooltip(self, entry_def):
        return EntryTooltip(HovertipStyle.HOVER_TIP_DEFAULT, {TooltipFieldsComplete.simoleon_value: entry_def.price, TooltipFields.subtext: self.entry_text_flavor, TooltipFields.rarity_text: self.entry_text_rarity, TooltipFields.recipe_description: self.entry_text_description, TooltipFields.recipe_name: LocalizationHelperTuning.get_object_name(entry_def)})
