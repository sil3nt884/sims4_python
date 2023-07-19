from live_events.live_event_service import LiveEventName
class LiveFestivalEventState(enum.Int):
    ACTIVE = 0
    DISABLED = 1

class LiveFestivalTuning:

    @staticmethod
    def _verify_tunable_callback(instance_class, tunable_name, source, value, **kwargs):
        for (festival_key, festival_data) in value.items():
            if festival_data.live_event_name != festival_key.name:
                logger.error('Live festival {} has field Live Event Name set different to its key name.', festival_key.name, owner='asantos')

    LIVE_FESTIVAL_EVENT_DATA = TunableMapping(description='\n        Defines event data for live events.\n        ', key_type=TunableEnumEntry(description='\n            Festival event key.\n            ', tunable_type=LiveEventName, default=LiveEventName.DEFAULT, invalid_enums=(LiveEventName.DEFAULT,)), value_type=TunableTuple(description='\n            Defines a live festival event\n            ', name=TunableLocalizedString(description='\n                User-facing name for festival to be displayed in UI.\n                '), street=TunableWorldDescription(description='\n                Reference to the street associated with this festival.\n                ', pack_safe=True), lot=TunableLotDescription(description='\n                Reference to the lot associated with this festival.\n                ', pack_safe=True), start_date=TunableTuple(description='\n                Date and time (UTC) for when the event is expected to start.\n                ', display_name='Start Date (UTC)', export_class_name='TunableChallengeDateTuple', year=TunableRange(description='\n                    Year\n                    ', tunable_type=int, default=2021, minimum=2014), month=TunableRange(description='\n                    Month\n                    ', tunable_type=int, default=1, minimum=1, maximum=12), day=TunableRange(description='\n                    Day\n                    ', tunable_type=int, default=1, minimum=1, maximum=31), hour=TunableRange(description='\n                    Hour (24-hour)\n                    ', tunable_type=int, default=0, minimum=0, maximum=23), minute=TunableRange(description='\n                    Minute\n                    ', tunable_type=int, default=0, minimum=0, maximum=59)), end_date=TunableTuple(description='\n                Date and time (UTC) for when the event is expected to end.\n                ', display_name='End Date (UTC)', export_class_name='TunableChallengeDateTuple', year=TunableRange(description='\n                    Year\n                    ', tunable_type=int, default=2021, minimum=2014), month=TunableRange(description='\n                    Month\n                    ', tunable_type=int, default=1, minimum=1, maximum=12), day=TunableRange(description='\n                    Day\n                    ', tunable_type=int, default=1, minimum=1, maximum=31), hour=TunableRange(description='\n                    Hour (24-hour)\n                    ', tunable_type=int, default=0, minimum=0, maximum=23), minute=TunableRange(description='\n                    Minute\n                    ', tunable_type=int, default=0, minimum=0, maximum=59)), festival_time=TunableTuple(description='\n                In-game time of festival.\n                ', day=TunableRange(description='\n                    Day of week, 0 = sunday, 6 = saturday.\n                    ', tunable_type=int, default=0, minimum=0, maximum=6), hour=TunableRange(description='\n                    Hour (24-hour)\n                    ', tunable_type=int, default=0, minimum=0, maximum=23), duration=Tunable(description='\n                    Duration of festival (estimated) in minutes.\n                    ', tunable_type=int, default=0), export_class_name='LiveFestivalEventDate'), street_description_image=TunableResourceKey(description='\n                An image which is shown on the map street description tooltip\n                ', resource_types=sims4.resources.CompoundTypes.IMAGE), live_event_name=Tunable(description='\n                The name of this live festival, as defined by the PMs in the UM message that triggers it.\n                This is needed so client can map festivals to their names from the UM messages.\n                This should be the same as the name picked as the key for this festival.\n                ', tunable_type=str, default='', allow_empty=False), state=TunableEnumEntry(description='\n                The active state of the event\n                ', tunable_type=LiveFestivalEventState, default=LiveFestivalEventState.ACTIVE), export_class_name='LiveFestivalEvent'), verify_tunable_callback=_verify_tunable_callback, export_modes=ExportModes.ClientBinary, tuple_name='LiveFestivalEventMap')
