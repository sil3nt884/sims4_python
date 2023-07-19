from audio.primitive import TunablePlayAudioAllPacksfrom bucks.bucks_enums import BucksTypefrom buffs.buff import Bufffrom business.advertising_configuration import AdvertisingConfigurationfrom business.business_employee_tuning import TunableBusinessEmployeeDataSnippetfrom business.business_enums import BusinessEmployeeType, BusinessCustomerStarRatingBuffBuckets, BusinessAdvertisingType, BusinessQualityTypefrom business.business_funds import BusinessFundsCategoryfrom business.business_tuning import TunableStarRatingVfxMappingfrom interactions.utils.tunable_icon import TunableIconAllPacks, TunableIconfrom objects.lighting.lighting_utils import LightingHelperfrom sims4 import mathfrom sims4.localization import TunableLocalizedString, TunableLocalizedStringFactoryVariant, TunableLocalizedStringFactoryfrom sims4.resources import Typesfrom sims4.tuning.geometric import TunableCurvefrom sims4.tuning.instances import HashedTunedInstanceMetaclassfrom sims4.tuning.tunable import HasTunableReference, TunableMapping, TunableEnumEntry, TunableRange, TunableList, TunableTuple, OptionalTunable, TunableReference, TunableSet, Tunable, TunablePackSafeReference, TunableInterval, TunableEnumWithFilterfrom sims4.tuning.tunable_base import GroupNames, ExportModes, EnumBinaryExportTypefrom ui.ui_dialog import UiDialogOkCancelfrom ui.ui_dialog_notification import TunableUiDialogNotificationSnippetfrom vfx import PlayEffectimport servicesimport sims4.resourcesimport tagimport uilogger = sims4.log.Logger('Business', default_owner='trevor')
class Business(HasTunableReference, metaclass=HashedTunedInstanceMetaclass, manager=services.get_instance_manager(sims4.resources.Types.BUSINESS)):
    INSTANCE_TUNABLES = {'employee_data_map': TunableMapping(description='\n            The mapping between Business Employee Type and the Employee Data for\n            that type.\n            ', key_type=TunableEnumEntry(description='\n                The Business Employee Type that should get the specified Career.\n                ', tunable_type=BusinessEmployeeType, default=BusinessEmployeeType.INVALID, invalid_enums=(BusinessEmployeeType.INVALID,)), value_type=TunableBusinessEmployeeDataSnippet(description='\n                The Employee Data for the given Business Employee Type.\n                '), tuning_group=GroupNames.EMPLOYEES), 'npc_starting_funds': TunableRange(description='\n            The amount of money an npc-owned store will start with in their\n            funds. Typically should be set to the same cost as the interaction\n            to buy the business.\n            ', tunable_type=int, default=0, minimum=0, tuning_group=GroupNames.CURRENCY), 'funds_category_data': TunableMapping(description='\n            Data associated with specific business funds categories.\n            ', key_type=TunableEnumEntry(description='\n                The funds category.\n                ', tunable_type=BusinessFundsCategory, default=BusinessFundsCategory.NONE, invalid_enums=(BusinessFundsCategory.NONE,)), value_type=TunableTuple(description='\n                The data associated with this retail funds category.\n                ', summary_dialog_entry=OptionalTunable(description="\n                    If enabled, an entry for this category is displayed in the\n                    business' summary dialog.\n                    ", tunable=TunableLocalizedString(description='\n                        The dialog entry for this retail funds category. This\n                        string takes no tokens.\n                        '))), tuning_group=GroupNames.CURRENCY), 'default_markup_multiplier': TunableRange(description='\n            The default markup multiplier for a new business. This must match a\n            multiplier that\'s in the Markup Multiplier Data tunable. It\'s also\n            possible for this to be less than 1, meaning the default "markup"\n            will actually cause prices to be lower than normal.\n            ', tunable_type=float, default=1.25, minimum=math.EPSILON, tuning_group=GroupNames.CURRENCY), 'advertising_name_map': TunableMapping(description='\n            The mapping between advertising enum and the name used in the UI for\n            that type.\n            ', key_name='advertising_enum', key_type=TunableEnumEntry(description='\n                The Advertising Type.\n                ', tunable_type=BusinessAdvertisingType, default=BusinessAdvertisingType.INVALID, invalid_enums=(BusinessAdvertisingType.INVALID,), binary_type=EnumBinaryExportType.EnumUint32), value_name='advertising_name', value_type=TunableLocalizedString(description='\n                The name of the advertising type used in the UI.\n                '), tuple_name='AdvertisingEnumDataMappingTuple', tuning_group=GroupNames.UI, export_modes=ExportModes.All), 'advertising_type_sort_order': TunableList(description='\n            Sort order for the advertising types in the UI\n            ', tunable=TunableEnumEntry(description='\n                The Advertising Type.\n                ', tunable_type=BusinessAdvertisingType, default=BusinessAdvertisingType.INVALID, invalid_enums=(BusinessAdvertisingType.INVALID,), binary_type=EnumBinaryExportType.EnumUint32), unique_entries=True, tuning_group=GroupNames.UI, export_modes=ExportModes.All), 'quality_settings': TunableList(description='\n            Tunable Business quality settings.  \n            \n            Quality type can be interpreted in different ways \n            by specific businesses, and can be used for tests.\n            \n            These are quality settings that are exported to the client.\n            \n            The order in this list should be the order we want them displayed\n            in the UI.\n            ', tunable=TunableTuple(quality_type=TunableEnumEntry(description='\n                    The quality Type.\n                    ', tunable_type=BusinessQualityType, default=BusinessQualityType.INVALID, invalid_enums=(BusinessQualityType.INVALID,), binary_type=EnumBinaryExportType.EnumUint32), quality_name=TunableLocalizedString(description='\n                    The name of the quality type used in the UI.\n                    '), export_class_name='QualitySettingsData'), tuning_group=GroupNames.UI, export_modes=ExportModes.All), 'show_settings_button': OptionalTunable(description="\n            If enabled, this business type will show the settings button with \n            the tuned tooltip text. If disabled, this business type won't show\n            the settings button.\n            ", tunable=TunableLocalizedString(description='\n                The tooltip to show on the settings button when it is shown\n                for this business type.\n                '), tuning_group=GroupNames.UI, export_modes=ExportModes.ClientBinary), 'business_summary_tooltip': OptionalTunable(description='\n            If enabled, allows tuning a business summary tooltip. If disabled, no\n            tooltip will be used or displayed by the UI.\n            ', tunable=TunableLocalizedString(description='\n                The tooltip to show on the business panel.\n                '), tuning_group=GroupNames.UI, export_modes=ExportModes.ClientBinary), 'show_sell_button': Tunable(description="\n            If checked, the sell button will be shown in the business panel if\n            the business is on the active lot. If left unchecked, the sell button\n            won't be shown on the business panel at all.\n            ", tunable_type=bool, default=False, tuning_group=GroupNames.UI, export_modes=ExportModes.ClientBinary), 'show_employee_button': Tunable(description='\n            ', tunable_type=bool, default=False, tuning_group=GroupNames.UI, export_modes=ExportModes.ClientBinary), 'default_quality': OptionalTunable(description='\n            The default quality type for the business.', tunable=TunableEnumEntry(tunable_type=BusinessQualityType, default=BusinessQualityType.INVALID, invalid_enums=(BusinessQualityType.INVALID,), binary_type=EnumBinaryExportType.EnumUint32), disabled_value=BusinessQualityType.INVALID, tuning_group=GroupNames.BUSINESS), 'quality_unlock_perk': OptionalTunable(description='\n            Reference to a perk that, if unlocked, allow the player to adjust\n            the quality type specific to this business.\n            ', tunable=TunablePackSafeReference(manager=services.get_instance_manager(sims4.resources.Types.BUCKS_PERK)), tuning_group=GroupNames.BUSINESS), 'advertising_configuration': AdvertisingConfiguration.TunableFactory(description='\n            Tunable Business advertising configuration.\n            ', tuning_group=GroupNames.BUSINESS), 'markup_multiplier_data': TunableList(description='\n            A list of markup multiplier display names and the actual multiplier\n            associated with that name. This is used for sending the markup\n            information to the UI.\n            ', tunable=TunableTuple(description='\n               A tuple of the markup multiplier display name and the actual\n               multiplier associated with that display name.\n               ', name=TunableLocalizedString(description='\n                   The display name for this markup multiplier. e.g. a\n                   multiplier of 1.2 will have "20 %" tuned here.\n                   '), markup_multiplier=TunableRange(description='\n                    The multiplier associated with this display name.\n                    ', tunable_type=float, default=1, minimum=math.EPSILON), export_class_name='MarkupMultiplierData'), tuning_group=GroupNames.CURRENCY, export_modes=ExportModes.All), 'star_rating_to_screen_slam_map': TunableMapping(description='\n            A mapping of star ratings to screen slams.\n            Screen slams will be triggered when the rating increases to a new\n            whole value.\n            ', key_type=int, value_type=ui.screen_slam.TunableScreenSlamSnippet(), key_name='star_rating', value_name='screen_slam', tuning_group=GroupNames.BUSINESS), 'show_empolyee_skill_level_up_notification': Tunable(description='\n            If true, skill level up notifications will be shown for employees.\n            ', tunable_type=bool, default=True, tuning_group=GroupNames.EMPLOYEES), 'bucks': TunableEnumEntry(description='\n            The Bucks Type this business will use for Perk unlocks.\n            ', tunable_type=BucksType, default=BucksType.INVALID, invalid_enums=(BucksType.INVALID,), tuning_group=GroupNames.CURRENCY, export_modes=ExportModes.All), 'off_lot_star_rating_decay_multiplier_perk': OptionalTunable(description='\n            If enabled, allows the tuning of a perk which can adjust the off-lot star rating decay.\n            ', tunable=TunableTuple(description='\n                The off lot star rating decay multiplier tuning.\n                ', perk=TunableReference(description='\n                    The perk that will cause the multiplier to be applied to the\n                    star rating decay during off-lot simulations.\n                    ', manager=services.get_instance_manager(sims4.resources.Types.BUCKS_PERK)), decay_multiplier=TunableRange(description='\n                    If the household has the specified perk, the off-lot star\n                    rating decay rate will be multiplied by this value.\n                    ', tunable_type=float, default=1.1, minimum=0)), tuning_group=GroupNames.OFF_LOT), 'manage_outfit_affordances': TunableSet(description='\n            A list of affordances that are shown when the player clicks on the\n            Manage Outfits button.\n            ', tunable=TunableReference(description='\n                An affordance shown when the player clicks on the Manage Outfits\n                button.\n                ', manager=services.get_instance_manager(sims4.resources.Types.INTERACTION), pack_safe=True), tuning_group=GroupNames.EMPLOYEES), 'employee_training_buff_tag': TunableEnumWithFilter(description='\n            A tag to indicate a buff is used for employee training.\n            ', tunable_type=tag.Tag, default=tag.Tag.INVALID, invalid_enums=(tag.Tag.INVALID,), filter_prefixes=('buff',), pack_safe=True, tuning_group=GroupNames.EMPLOYEES), 'customer_buffs_to_save_tag': TunableEnumWithFilter(description='\n            All buffs with this tag will be saved and reapplied to customer sims\n            on load.\n            ', tunable_type=tag.Tag, default=tag.Tag.INVALID, invalid_enums=(tag.Tag.INVALID,), filter_prefixes=('buff',), pack_safe=True, tuning_group=GroupNames.CUSTOMER), 'customer_buffs_to_remove_tags': TunableSet(description='\n            Tags that indicate which buffs should be removed from customers when\n            they leave the business.\n            ', tunable=TunableEnumWithFilter(description='\n                A tag that indicates a buff should be removed from the customer\n                when they leave the business.\n                ', tunable_type=tag.Tag, default=tag.Tag.INVALID, invalid_enums=(tag.Tag.INVALID,), filter_prefixes=('buff',), pack_safe=True), tuning_group=GroupNames.CUSTOMER), 'current_business_lot_transfer_dialog_entry': TunableLocalizedString(description='\n            This is the text that will show in the funds transfer dialog drop\n            down for the current lot if it\'s a business lot. Typically, the lot\n            name would show but if the active lot is a business lot it makes\n            more sense to say something along the lines of\n            "Current Retail Lot" or "Current Restaurant" instead of the name of the lot.\n            ', tuning_group=GroupNames.UI), 'open_business_notification': TunableUiDialogNotificationSnippet(description='\n            The notification that shows up when the player opens the business.\n            We need to trigger this from code because we need the notification\n            to show up when we open the store through the UI or through an\n            Interaction.\n            ', tuning_group=GroupNames.UI), 'no_way_to_make_money_notification': TunableUiDialogNotificationSnippet(description='\n            The notification that shows up when the player opens a store that has no\n            way of currently making money (e.g. retail store having no items set for\n            sale or restaurants having nothing on the menu). It will replace the\n            Open Business Notification.\n            ', tuning_group=GroupNames.UI), 'audio_sting_open': TunablePlayAudioAllPacks(description='\n            The audio sting to play when the store opens.\n            ', tuning_group=GroupNames.UI), 'audio_sting_close': TunablePlayAudioAllPacks(description='\n            The audio sting to play when the store closes.\n            ', tuning_group=GroupNames.UI), 'sell_store_dialog': UiDialogOkCancel.TunableFactory(description='\n            This dialog is to confirm the sale of the business.\n            ', tuning_group=GroupNames.UI), 'lighting_helper_open': LightingHelper.TunableFactory(description='\n            The lighting helper to execute when the store opens.\n            e.g. Turn on all neon signs.\n            ', tuning_group=GroupNames.TRIGGERS), 'lighting_helper_close': LightingHelper.TunableFactory(description='\n            The lighting helper to execute when the store closes.\n            e.g. Turn off all neon signs.\n            ', tuning_group=GroupNames.TRIGGERS), 'min_and_max_star_rating': TunableInterval(description='\n            The lower and upper bounds for a star rating. This affects both the\n            customer star rating and the overall business star rating.\n            ', tunable_type=float, default_lower=1, default_upper=5, tuning_group=GroupNames.BUSINESS), 'min_and_max_star_rating_value': TunableInterval(description='\n            The minimum and maximum star rating value for this business.\n            ', tunable_type=float, default_lower=0, default_upper=100, tuning_group=GroupNames.BUSINESS), 'star_rating_value_to_user_facing_rating_curve': TunableCurve(description='\n           Curve that maps star rating values to the user-facing star rating.\n           ', x_axis_name='Star Rating Value', y_axis_name='User-Facing Star Rating', tuning_group=GroupNames.BUSINESS), 'default_business_star_rating_value': TunableRange(description='\n            The star rating value a newly opened business will begin with. Keep in mind, this is not the actual star rating. This is the value which maps to a rating using \n            ', tunable_type=float, default=1, minimum=0, tuning_group=GroupNames.BUSINESS), 'customer_rating_delta_to_business_star_rating_value_change_curve': TunableCurve(description='\n            When a customer is done with their meal, we will take the delta\n            between their rating and the business rating and map that to an\n            amount it should change the star rating value for the restaurant.\n            \n            For instance, the business has a current rating of 3 stars and the\n            customer is giving a rating of 4.5 stars. 4.5 - 3 = a delta of 1.5.\n            That 1.5 will map, on this curve, to the amount we should adjust the\n            star rating value for the business.\n            ', x_axis_name='Customer Rating to Business Rating Delta (restaurant rating - customer rating)', y_axis_name='Business Star Rating Value Change', tuning_group=GroupNames.BUSINESS), 'default_customer_star_rating': TunableRange(description='\n            The star rating a new customer starts with.\n            ', tunable_type=float, default=3, minimum=0, tuning_group=GroupNames.CUSTOMER), 'customer_star_rating_buff_bucket_data': TunableMapping(description="\n            A mapping from Business Customer Star Rating Buff Bucket to the data\n            associated with the buff bucker for this business.\n            \n            Each buff bucket has a minimum, median, and maximum value. For every\n            buff a customer has that falls within a buff bucket, that buff's\n            Buff Bucket Delta is added to that bucket's totals. The totals are\n            clamped between -1 and 1 and interpolated against the\n            minimum/medium/maximum value for their associated buckets. All of\n            the final values of the buckets are added together and that value is\n            used in the Customer Star Buff Bucket To Rating Curve to determine\n            the customer's final star rating of this business.\n            \n            For instance, assume a buff bucket has a minimum value of -200, median of 0,\n            and maximum of 100, and the buff bucket's clamped total is 0.5, the actual\n            value of that bucket will be 50 (half way, or 0.5, between 0 and\n            100). If, however, the bucket's total is -0.5, we'd interpolate\n            between the bucket's minimum value, -200, and median value, 0, to arrive at a\n            bucket value of -100.\n            ", key_name='Star_Rating_Buff_Bucket', key_type=TunableEnumEntry(description='\n                The Business Customer Star Rating Buff Bucket enum.\n                ', tunable_type=BusinessCustomerStarRatingBuffBuckets, default=BusinessCustomerStarRatingBuffBuckets.INVALID, invalid_enums=(BusinessCustomerStarRatingBuffBuckets.INVALID,)), value_name='Star_Rating_Buff_Bucket_Data', value_type=TunableTuple(description='\n                All of the data associated with a specific customer star rating\n                buff bucket.\n                ', bucket_value_minimum=Tunable(description="\n                    The minimum value for this bucket's values.\n                    ", tunable_type=float, default=-100), positive_bucket_vfx=PlayEffect.TunableFactory(description='\n                    The vfx to play when positive change star value occurs. \n                    '), negative_bucket_vfx=PlayEffect.TunableFactory(description='\n                    The vfx to play when negative change star value occurs.\n                    '), bucket_value_median=Tunable(description="\n                    The median/middle value for this bucket's values.\n                    ", tunable_type=float, default=0), bucket_value_maximum=Tunable(description="\n                    The maximum value for this bucket's values.\n                    ", tunable_type=float, default=100), bucket_icon=TunableIconAllPacks(description='\n                    The icon that represents this buff bucket.\n                    '), bucket_positive_text=TunableLocalizedStringFactoryVariant(description='\n                    The possible text strings to show up when this bucket\n                    results in a positive star rating.\n                    '), bucket_negative_text=TunableLocalizedStringFactoryVariant(description='\n                    The possible text strings to show up when this bucket\n                    results in a bad star rating.\n                    '), bucket_excellence_text=TunableLocalizedStringFactoryVariant(description="\n                    The description text to use in the business summary panel if\n                    this buff bucket is in the 'Excellence' section.\n                    "), bucket_growth_opportunity_text=TunableLocalizedStringFactoryVariant(description="\n                    The description text to use in the business summary panel if\n                    this buff bucket is in the 'Growth Opportunity' section.\n                    "), bucket_growth_opportunity_threshold=TunableRange(description='\n                    The amount of score this bucket must be from the maximum to be\n                    considered a growth opportunity. \n                    ', tunable_type=float, minimum=0, default=10), bucket_excellence_threshold=TunableRange(description='\n                    The amount of score this bucket must be before it is \n                    considered an excellent bucket\n                    ', tunable_type=float, minimum=0, default=1), bucket_title=TunableLocalizedString(description='\n                    The name for this bucket.\n                    ')), tuning_group=GroupNames.CUSTOMER), 'customer_star_rating_buff_data': TunableMapping(description='\n            A mapping of Buff to the buff data associated with that buff.\n            \n            Refer to the description on Customer Star Rating Buff Bucket Data\n            for a detailed explanation of how this tuning works.\n            ', key_name='Buff', key_type=Buff.TunableReference(description="\n                A buff meant to drive a customer's star rating for a business.\n                ", pack_safe=True), value_name='Buff Data', value_type=TunableTuple(description='\n                The customer star rating for this buff.\n                ', buff_bucket=TunableEnumEntry(description='\n                    The customer star rating buff bucket associated with this buff.\n                    ', tunable_type=BusinessCustomerStarRatingBuffBuckets, default=BusinessCustomerStarRatingBuffBuckets.INVALID, invalid_enums=(BusinessCustomerStarRatingBuffBuckets.INVALID,)), buff_bucket_delta=Tunable(description='\n                    The amount of change this buff should contribute to its bucket.\n                    ', tunable_type=float, default=0), update_star_rating_on_add=Tunable(description="\n                    If enabled, the customer's star rating will be re-\n                    calculated when this buff is added.\n                    ", tunable_type=bool, default=True), update_star_rating_on_remove=Tunable(description="\n                    If enabled, the customer's star rating will be re-\n                    calculated when this buff is removed.\n                    ", tunable_type=bool, default=False)), tuning_group=GroupNames.CUSTOMER), 'customer_star_buff_bucket_to_rating_curve': TunableCurve(description='\n            A mapping of the sum of all buff buckets for a single customer to\n            the star rating for that customer.\n            \n            Refer to the description on Customer Star Rating Buff Bucket Data\n            for a detailed explanation of how this tuning works.\n            ', x_axis_name='Buff Bucket Total', y_axis_name='Star Rating', tuning_group=GroupNames.CUSTOMER), 'customer_star_rating_vfx_increase_arrow': OptionalTunable(description='\n            The "up arrow" VFX to play when a customer\'s star rating goes up.\n            These will play even if the customer\'s rating doesn\'t go up enough\n            to trigger a star change.\n            ', tunable=PlayEffect.TunableFactory(), tuning_group=GroupNames.CUSTOMER), 'customer_star_rating_vfx_decrease_arrow': OptionalTunable(description='\n            The "down arrow" VFX to play when a customer\'s star rating goes\n            down. These will play even if the customer\'s rating doesn\'t go down\n            enough to trigger a star change.\n            ', tunable=PlayEffect.TunableFactory(), tuning_group=GroupNames.CUSTOMER), 'customer_star_rating_vfx_mapping': TunableStarRatingVfxMapping(description='\n            Maps the star rating for the customer to the persistent star effect\n            that shows over their head.\n            ', tuning_group=GroupNames.CUSTOMER), 'customer_final_star_rating_vfx': OptionalTunable(description='\n            The VFX to play when the customer is done and is submitting their\n            final star rating to the business.\n            ', tunable=PlayEffect.TunableFactory(), tuning_group=GroupNames.CUSTOMER), 'customer_max_star_rating_vfx': OptionalTunable(description='\n            The VFX to play when the customer hits the maximum star rating.\n            ', tunable=PlayEffect.TunableFactory(), tuning_group=GroupNames.CUSTOMER), 'customer_star_rating_statistic': TunablePackSafeReference(description='\n            The statistic on a customer Sim that represents their current star\n            rating.\n            ', manager=services.get_instance_manager(Types.STATISTIC), allow_none=True, tuning_group=GroupNames.CUSTOMER), 'buy_business_lot_affordance': TunableReference(description='\n            The affordance to buy a lot for this type of business.\n            ', manager=services.get_instance_manager(Types.INTERACTION), tuning_group=GroupNames.UI), 'initial_funds_transfer_amount': TunableRange(description='\n            The amount to default the funds transfer dialog when a player\n            initially buys this business.\n            ', tunable_type=int, minimum=0, default=2500, tuning_group=GroupNames.CURRENCY), 'summary_dialog_icon': TunableIcon(description='\n            The Icon to show in the header of the dialog.\n            ', tuning_group=GroupNames.UI), 'summary_dialog_subtitle': TunableLocalizedString(description="\n            The subtitle for the dialog. The main title will be the store's name.\n            ", tuning_group=GroupNames.UI), 'summary_dialog_transactions_header': TunableLocalizedString(description="\n            The header for the 'Items Sold' line item. By design, this should say\n            something along the lines of 'Items Sold:' or 'Transactions:'\n            ", tuning_group=GroupNames.UI), 'summary_dialog_transactions_text': TunableLocalizedStringFactory(description="\n            The text in the 'Items Sold' line item. By design, this should say\n            the number of items sold.\n            {0.Number} = number of items sold since the store was open\n            i.e. {0.Number}\n            ", tuning_group=GroupNames.UI), 'summary_dialog_cost_of_ingredients_header': TunableLocalizedString(description="\n            The header for the 'Cost of Ingredients' line item. By design, this\n            should say something along the lines of 'Cost of Ingredients:'\n            ", tuning_group=GroupNames.UI), 'summary_dialog_cost_of_ingredients_text': TunableLocalizedStringFactory(description="\n            The text in the 'Cost of Ingredients' line item. {0.Number} = the\n            amount of money spent on ingredients.\n            ", tuning_group=GroupNames.UI), 'summary_dialog_food_profit_header': TunableLocalizedString(description="\n            The header for the 'Food Profits' line item. This line item is the\n            total revenue minus the cost of ingredients. By design, this should\n            say something along the lines of 'Food Profits:'\n            ", tuning_group=GroupNames.UI), 'summary_dialog_food_profit_text': TunableLocalizedStringFactory(description="\n            The text in the 'Food Profits' line item. {0.Number} = the amount of\n            money made on food.\n            ", tuning_group=GroupNames.UI), 'summary_dialog_wages_owed_header': TunableLocalizedString(description="\n            The header text for the 'Wages Owned' line item. By design, this\n            should say 'Wages Owed:'\n            ", tuning_group=GroupNames.UI), 'summary_dialog_wages_owed_text': TunableLocalizedStringFactory(description="\n            The text in the 'Wages Owed' line item. By design, this should say the\n            number of hours worked and the price per hour.\n            {0.Number} = number of hours worked by all employees\n            {1.Money} = amount employees get paid per hour\n            i.e. {0.Number} hours worked x {1.Money}/hr\n            ", tuning_group=GroupNames.UI), 'summary_dialog_payroll_header': TunableLocalizedStringFactory(description='\n            The header text for each unique Sim on payroll. This is provided one\n            token, the Sim.\n            ', tuning_group=GroupNames.UI), 'summary_dialog_payroll_text': TunableLocalizedStringFactory(description='\n            The text for each job that the Sim on payroll has held today. This is\n            provided three tokens: the career level name, the career level salary,\n            and the total hours worked.\n            \n            e.g.\n             {0.String} ({1.Money}/hr) * {2.Number} {S2.hour}{P2.hours}\n            ', tuning_group=GroupNames.UI), 'summary_dialog_wages_advertising_header': TunableLocalizedString(description="\n            The header text for the 'Advertising' line item. By design, this\n            should say 'Advertising Spent:'\n            ", tuning_group=GroupNames.UI), 'summary_dialog_wages_advertising_text': TunableLocalizedStringFactory(description="\n            The text in the 'Advertising' line item. By design, this should say the\n            amount spent on advertising\n            ", tuning_group=GroupNames.UI), 'summary_dialog_wages_net_profit_header': TunableLocalizedString(description="\n            The header text for the 'Net Profit' line item. By design, this\n            should say 'Net Profit:'\n            ", tuning_group=GroupNames.UI), 'summary_dialog_wages_net_profit_text': TunableLocalizedStringFactory(description="\n            The text in the 'Net Profit' line item. By design, this should say the\n            total amount earnt so far in this shift\n            ", tuning_group=GroupNames.UI), 'grand_opening_notification': OptionalTunable(description='\n            If enabled, allows a notification to be tuned that will show only\n            the first time you arrive on your business lot.\n            ', tunable=TunableUiDialogNotificationSnippet(), tuning_group=GroupNames.UI), 'business_icon': TunableIcon(description='\n            The Icon to show in the header of the dialog.\n            ', tuning_group=GroupNames.UI), 'star_rating_to_customer_count_curve': TunableCurve(description='\n            A curve mapping of current star rating of the restaurant to the base\n            number of customers that should come per interval.\n            ', x_axis_name='Star Rating', y_axis_name='Base Customer Count', tuning_group=GroupNames.CUSTOMER), 'time_of_day_to_customer_count_multiplier_curve': TunableCurve(description='\n            A curve that lets you tune a specific customer multiplier based on the \n            time of day. \n            \n            Time of day should range between 0 and 23, 0 being midnight.\n            ', tuning_group=GroupNames.CUSTOMER, x_axis_name='time_of_day', y_axis_name='customer_multiplier'), 'off_lot_customer_count_multiplier': TunableRange(description='\n            This value will be multiplied by the Base Customer Count (derived\n            from the Star Rating To Customer Count Curve) to determine the base\n            number of customers per hour during off-lot simulation.\n            ', tunable_type=float, minimum=0, default=0.5, tuning_group=GroupNames.OFF_LOT), 'off_lot_customer_count_penalty_multiplier': TunableRange(description='\n            A penalty multiplier applied to the off-lot customer count. This is\n            applied after the Off Lot Customer Count Multiplier is applied.\n            ', tunable_type=float, default=0.2, minimum=0, tuning_group=GroupNames.OFF_LOT), 'off_lot_chance_of_star_rating_increase': TunableRange(description="\n            Every time we run offlot simulations, we'll use this as the chance\n            to increase in star rating instead of decrease.\n            ", tunable_type=float, default=0.1, minimum=0, tuning_group=GroupNames.OFF_LOT), 'off_lot_star_rating_decay_per_hour_curve': TunableCurve(description='\n            Maps the current star rating of the business to the decay per hour\n            of star rating value. This value will be added to the current star\n            rating value so use negative numbers to make the rating decay.\n            ', x_axis_name='Business Star Rating', y_axis_name='Off-Lot Star Rating Value Decay Per Hour', tuning_group=GroupNames.OFF_LOT), 'off_lot_star_rating_increase_per_hour_curve': TunableCurve(description='\n            Maps the current star rating of the business to the increase per\n            hour of the star rating value, assuming the Off Lot Chance Of Star\n            Rating Increase passes.\n            ', x_axis_name='Business Star Rating', y_axis_name='Off-Lot Star Rating Value Increase Per Hour', tuning_group=GroupNames.OFF_LOT), 'off_lot_profit_per_item_multiplier': TunableRange(description='\n            This is multiplied by the average cost of the business specific\n            service that is the main source of profit, to determine how much \n            money the business makes per customer during off-lot simulation.\n            ', tunable_type=float, default=0.3, minimum=0, tuning_group=GroupNames.OFF_LOT), 'off_lot_net_loss_notification': OptionalTunable(description='\n            If enabled, the notification that will show if a business turns a \n            negative net profit during off-lot simulation.\n            ', tunable=TunableUiDialogNotificationSnippet(), tuning_group=GroupNames.OFF_LOT), 'critic': OptionalTunable(description='\n            If enabled, allows tuning a critic for this business type.\n            ', tunable=TunableTuple(description='\n                Critic tuning for this business.\n                ', critic_trait=TunableReference(description='\n                    The trait used to identify a critic of this business.\n                    ', manager=services.get_instance_manager(sims4.resources.Types.TRAIT)), critic_star_rating_application_count=TunableRange(description='\n                    The number of times a critics star rating should count towards the\n                    business star rating.\n                    ', tunable_type=int, default=10, minimum=1), critic_star_rating_vfx_mapping=TunableStarRatingVfxMapping(description='\n                    Maps the star rating for the critic to the persistent star effect\n                    that shows over their head.\n                    '), critic_banner_vfx=PlayEffect.TunableFactory(description='\n                    A persistent banner VFX that is started when the critic\n                    arrives and stopped when they leave.\n                    ')), tuning_group=GroupNames.CUSTOMER)}

    @classmethod
    def _verify_tuning_callback(cls):
        advertising_data_types = frozenset(cls.advertising_configuration.advertising_data_map.keys())
        advertising_types_with_mapped_names = frozenset(cls.advertising_name_map.keys())
        advertising_sort_ordered_types = frozenset(cls.advertising_name_map.keys())
        if advertising_data_types:
            if advertising_data_types != advertising_types_with_mapped_names:
                logger.error('Advertising type list {} does not match list of mapped names: {}', advertising_data_types, advertising_types_with_mapped_names)
            if advertising_data_types != advertising_sort_ordered_types:
                logger.error('Advertising type list {} does not sorted UI list types: {}', advertising_data_types, advertising_sort_ordered_types)
        if cls.advertising_configuration.default_advertising_type is not None and cls.advertising_configuration.default_advertising_type not in advertising_types_with_mapped_names:
            logger.error('Default advertising type {} is not in advertising name map', cls.default_advertising_type)
