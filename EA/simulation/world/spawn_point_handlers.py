from sims4.gsi.dispatcher import GsiHandler
    cheat.add_token_param('x')
    cheat.add_token_param('y')
    cheat.add_token_param('z')
@GsiHandler('spawn_point', schema)
def generate_spawn_point_data(*args, zone_id:int=None, **kwargs):
    data = []
    zone = services.current_zone()
    if zone is None:
        return data
    for spawn_point in zone.spawn_points_gen():
        entry = {}
        entry['id'] = str(spawn_point.spawn_point_id)
        entry['name'] = spawn_point.get_name()
        center = spawn_point.get_approximate_center()
        entry['x'] = center.x
        entry['y'] = center.y
        entry['z'] = center.z
        entry['lot_id'] = spawn_point.lot_id

        def get_tag_name(tag):
            if not isinstance(tag, Tag):
                tag = Tag(tag)
            return tag.name

        entry['tags'] = ','.join(get_tag_name(tag) for tag in spawn_point.get_tags())
        data.append(entry)
    return data
