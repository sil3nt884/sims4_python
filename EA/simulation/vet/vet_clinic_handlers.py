from gsi_handlers.gameplay_archiver import GameplayArchiver
def log_vet_flow_entry(sims, source, message):
    archive_data = {'sims': sims, 'source': source, 'message': message}
    host_archiver.archive(data=archive_data)

    cheat.add_token_param('situation_id')
@GsiHandler('vet_customers', vet_clinic_customer_schema)
def generate_customer_data(zone_id:int=None):
    customer_situations_data = []
    zone_director = get_vet_clinic_zone_director()
    if zone_director is None:
        return customer_situations_data
    waiting_situations_ids = list(zone_director._waiting_situations.keys())
    waiting_situations_ids_list_fixed = tuple(waiting_situations_ids)

    def add_customer_situation_data(customer_situation):
        is_waiting_situation = customer_situation.id in waiting_situations_ids
        order_in_queue = waiting_situations_ids_list_fixed.index(customer_situation.id) if is_waiting_situation else 'Not In Queue'
        customer_situations_data.append({'waiting_start_time': str(customer_situation.wait_start_time), 'waiting_queue_order': str(order_in_queue), 'situation_id': str(customer_situation.id), 'pet': str(customer_situation.get_pet()), 'owner': str(customer_situation.get_pet_owner()), 'current_state': customer_situation.current_state_type.__name__, 'vet': str(customer_situation.get_vet())})
        if is_waiting_situation:
            waiting_situations_ids.remove(customer_situation.id)

    for customer_situation in zone_director.customer_situations_gen():
        add_customer_situation_data(customer_situation)
    if waiting_situations_ids:
        for customer_situation_id in tuple(waiting_situations_ids):
            customer_situation = services.get_zone_situation_manager().get(customer_situation_id)
            if customer_situation is not None:
                add_customer_situation_data(customer_situation)
    return customer_situations_data
