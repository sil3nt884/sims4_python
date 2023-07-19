from gsi_handlers.gameplay_archiver import GameplayArchiver
    sub_schema.add_field('walkstyle', label='Walkstyle', width=1)
    sub_schema.add_field('priority', label='Priority', width=1)
    sub_schema.add_field('can_replace_with_short_walkstyle', label='Can Replace With Short Walkstyle', width=1)
class WalkstyleGSIArchiver:

    def __init__(self, actor):
        self.sim = actor
        self.default_walkstyle = None
        self.combo_replacement_walkstyle_found = None
        self.default_walkstyle_replaced_by_short_walkstyle = None
        self.default_walkstyle_replaced_by_swimming_walkstyle = None
        self.default_walkstyle_replaced_by_posture_walkstyle = None
        self.walkstyle_requests = None

    def gsi_archive_entry(self):
        entry = {'default_walkstyle': str(self.default_walkstyle), 'combo_replacement_walkstyle_found': str(self.combo_replacement_walkstyle_found), 'default_walkstyle_replaced_by_short_walkstyle': str(self.default_walkstyle_replaced_by_short_walkstyle), 'default_walkstyle_replaced_by_swimming_walkstyle': str(self.default_walkstyle_replaced_by_swimming_walkstyle), 'default_walkstyle_replaced_by_posture_walkstyle': str(self.default_walkstyle_replaced_by_posture_walkstyle)}
        requests = []
        entry['Walkstyle Requests'] = requests
        for walkstyle_request in self.walkstyle_requests:
            rel_entry = {'walkstyle': str(walkstyle_request.walkstyle), 'priority': walkstyle_request.priority, 'can_replace_with_short_walkstyle': walkstyle_request.can_replace_with_short_walkstyle}
            requests.append(rel_entry)
        archiver.archive(data=entry, object_id=self.sim.id)
