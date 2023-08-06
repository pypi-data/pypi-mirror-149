import datetime


def get_wdb_records(sqlshell,
                    time_start=None, time_end=None, what_time='time_in',
                    trash_cat=None, trash_type=None, carrier=None,
                    auto_id=None, polygon_object_id=None, client=None,
                    *args, **kwargs):
    """ Вернуть статистику по заданным фильтрам """
    if not time_start:
        time_start = datetime.datetime.today() - datetime.timedelta(days=1)
    if not time_end:
        time_end = datetime.datetime.now()
    command = "SELECT rt.id as record_id, rt.trash_cat, rt.trash_type, " \
              "rt.brutto, rt.cargo, rt.tara, rt.time_in, rt.time_out, " \
              "rt.carrier, rt.operator, rt.auto, rt.client_id, dpo.id," \
              "concat('Бр.: ' || gross,  '| Тр.: ' || tare, " \
              "'| Доб.: ' || additional, " \
              "'| Изм.: ' || changing ) as full_notes, " \
              "auto_table.car_number, mpc.manual_pass, rpom.object_id " \
              "FROM records rt " \
              "LEFT JOIN auto auto_table ON (rt.auto=auto_table.id) " \
              "LEFT JOIN duo_records_owning dro ON (rt.id=dro.record) " \
              "LEFT JOIN duo_pol_owners dpo ON (dro.owner = dpo.id) " \
              "LEFT JOIN operator_comments oc ON (rt.id=oc.record_id) " \
              "LEFT JOIN records_pol_objects_mapping rpom ON (rt.id=rpom.record_id) " \
              "LEFT JOIN manual_pass_control mpc ON (rt.id=mpc.record_id) " \
              "WHERE {}::date>='{}' and {}::date<='{}'"
    command = command.format(what_time, time_start, what_time, time_end)
    if auto_id:
        command += " and auto_table.id={}".format(auto_id)
    if trash_cat:
        command += " and trash_cat={}".format(trash_cat)
    if trash_type:
        command += " and trash_type={}".format(trash_type)
    if carrier:
        command += " and carrier={}".format(carrier)
    if polygon_object_id:
        command += " and dpo.id={}".format(polygon_object_id)
    if client:
        command += " and client_id={}".format(client)
    response = sqlshell.get_table_dict(command)
    return response
