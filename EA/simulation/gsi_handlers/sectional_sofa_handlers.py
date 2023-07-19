import services
    cheat.add_token_param('sofaObjId')
    cheat.add_token_param('objId')
    cheat.add_token_param('objId')
    sub_schema.add_field('part_identifier', label='Part Name', width=1)
    sub_schema.add_field('part_location', label='Part Location', width=3)
    sub_schema.add_field('adjacent_parts', label='Adjacent Parts', width=2)
    sub_schema.add_field('overlapping_parts', label='Overlapping Parts', width=2)
@GsiHandler('sectional_sofa_pieces', sectional_sofa_schema)
def generate_sectional_sofa_data(*args, **kwargs):
    zone = services.current_zone()
    piece_data = []
    if zone.object_manager is None:
        return piece_data
    for obj in tuple(zone.object_manager.objects):
        if not isinstance(obj, SectionalSofaTuning.SECTIONAL_SOFA_OBJECT_DEF.cls):
            pass
        else:
            for piece in obj.sofa_pieces:
                part_data = []
                for part in piece.provided_parts:
                    part_info = {}
                    part_info['part_identifier'] = part.part_identifier
                    part_info['part_location'] = str(part.location)
                    part_info['adjacent_parts'] = '\n'.join(part.part_identifier for part in part.adjacent_parts_gen())
                    part_info['overlapping_parts'] = '\n'.join(part.part_identifier for part in part.get_overlapping_parts())
                    part_data.append(part_info)
                piece_data.append({'objId': str(piece.id), 'sofaObjId': str(piece._sofa_container.id), 'classStr': type(piece).__name__, 'definitionStr': piece.definition.name, 'modelStr': str(piece.model), 'locationStr': str(piece.location), 'Part Data': part_data})
    return piece_data
