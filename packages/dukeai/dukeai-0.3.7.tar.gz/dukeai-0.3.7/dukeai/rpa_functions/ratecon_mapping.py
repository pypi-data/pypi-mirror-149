import re
from .ratecon_schema_check import  schema_keys_validator, schema_key_type_validator
from .ratecon_schema_check import note_schema, reference_schema


def reference_schema_fix(reference_list):
    try:
        passed_references = list()
        if type(reference_list) == list:
            for reference in reference_list:
                if type(reference) == dict:
                    base_keys, matched_keys, success = schema_keys_validator(reference_schema, reference,
                                                                             'REFERENCE',
                                                                             True)
                    if success:
                        base_keys, matched_type_keys, success = schema_key_type_validator(reference_schema,
                                                                                          reference,
                                                                                          'REFERENCE', True)
                        if success:
                            passed_references.append(reference)

            return passed_references
        return []
    except:
        return []


def notes_schema_fix(notes_list):
    try:
        passed_notes = list()
        if type(notes_list) == list:
            for note in notes_list:
                if type(note) == dict:
                    base_keys, matched_keys, success = schema_keys_validator(note_schema, note,
                                                                             'NOTES',
                                                                             True)
                    if success:
                        base_keys, matched_type_keys, success = schema_key_type_validator(note_schema,
                                                                                          note,
                                                                                          'NOTES',
                                                                                          True)
                        if success:
                            passed_notes.append(note)

            return passed_notes
        return []
    except:
        return []


def stops_refs_notes_fix(stops_list):
    try:
        if type(stops_list) == list:
            for stop in stops_list:
                if type(stop) == dict:
                    if 'notes' in stop['notes'].keys():
                        stop['notes'] = notes_schema_fix(stop['notes'])

                    if 'references' in stop['references'].keys():
                        stop['references'] = reference_schema_fix(stop['references'])

        return stops_list
    except:
        return stops_list


def entity_id_fix(entity_list):
    try:
        if type(entity_list) == list:
            for n, ent in enumerate(entity_list):
                if type(ent) == dict:
                    ent_schema_test = True
                    for key in ['name', 'city', 'state', 'postal']:
                        if key not in ent.keys():
                            ent_schema_test = False

                    if ent_schema_test:
                        entity_id = ''
                        if type(ent['name']) == str:
                            print('a')
                            entity_name = re.sub('[^A-Za-z0-9]+', '', ent['name'])
                            entity_id = entity_id + entity_name
                        if type(ent['city']) == str:
                            print('b')
                            entity_city = re.sub('[^A-Za-z0-9]+', '', ent['city'])
                            entity_id = entity_id + entity_city
                        if type(ent['state']) == str:
                            entity_state = re.sub('[^A-Za-z0-9]+', '', ent['state'])
                            entity_id = entity_id + entity_state
                        if type(ent['postal']) == str:
                            entity_postal = re.sub('[^A-Za-z0-9]+', '', ent['postal'])
                            entity_id = entity_id + entity_postal
                        print(entity_id)
                        ent['id'] = entity_id.upper()
        success = True
        return success
    except:
        success = False
        return success


def ratecon_map(map_extract):
    try:
        final_mapping_check = True
        map_extract['references'] = reference_schema_fix(map_extract['references'])
        map_extract['notes'] = notes_schema_fix(map_extract['notes'])
        map_extract['stops'], stop_fix_success = stops_refs_notes_fix(map_extract['stops'])
        if stop_fix_success is False:
            final_mapping_check = False
        entity_fix_success = entity_id_fix(map_extract['entities'])
        if entity_fix_success is False:
            final_mapping_check = False
        for stop in map_extract['stops']:
            entity_fix_success = entity_id_fix(stop['entities'])
            if entity_fix_success is False:
                final_mapping_check = False
        return map_extract, final_mapping_check
    except:
        success = False
        return map_extract, success
