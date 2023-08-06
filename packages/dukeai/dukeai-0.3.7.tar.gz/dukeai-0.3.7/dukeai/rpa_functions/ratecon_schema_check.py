from colorama import Fore

rate_con_schema = {
    "transaction_type": [str],
    "sender": [str, type(None)],  # BROKER or SHIPPER if they are not having a broker. Example: "Werner Logistics"
    "receiver": [dict],
    "client": [str, type(None)],   # hard-coded. Example: "Werner Logistics"
    "submitted_time": [str, type(None)],  # time we received the email
    "identifier": [str, type(None)],
    "identifier_type": [str, type(None)],
    "shipment": [dict],
    "purpose": [str],
    "references": [list],  # append references_schema here for reference numbers ABOVE Shipper/Consignee
    "dates": [list],  # append dates_schema here if any, don't include stop dates
    "notes": [list],  # append notes_schema here for notes/comments ABOVE Shipper/Consignee
    "entities": [list],  # append entities_schema here
    "stops": [list]  # append stops_schema here
}

entity_schema = {
    "name": [str],
    "type": [str],
    "_type": [str],
    "id": [str],  # hard-coded
    "idtype": [str],  # hard-coded
    "_idtype": [str],  # hard-coded
    "address": [list],  # List object ['address part 1', 'address part 2']
    "city": [str, type(None)],
    "state": [str, type(None)],
    "postal": [str, type(None)],
    "country": [str, type(None)],
    "contacts": [dict]
}

receiver_schema = {
    "name": [str, type(None)],  # carrier-name on top right of page
    "isa_qual": [str],  # hard-coded
    "isa_ID": [str, type(None)]  # client email
}

shipment_schema = {
    "equipment_number": [str, type(None)],
    "weight": [str, type(None)],
    "weight_unit_code": [str, type(None)],
    "weight_qualifier": [str],  # hard-coded
    "volume": [str, type(None)],
    "volume_qualifier": [str, type(None)],
    "truck_type": [str, type(None)],
    "temperature": [str, type(None)],
    "trucklength": [str, type(None)],
    "charges": [str, int],
    "loading_quantity": [str, type(None)]
}

stop_schema = {
    "stoptype": [str],  # see stoptype codes for pickups and drops
    "_stoptype": [str],  # see stoptype codes for pickups and drops
    "ordinal": [int],  # starts from 1 EX: 1,2,3
    "dates": [list],  # append dates_schema here
    "references": [list],  # append references_schema here for stop references
    "order_detail": [list],
    "entities": [list],  # append entities_schema here for stop-level entities
    "notes": [list]  # append notes_schema here for stop-level notes/comments
}

note_schema = {
    "note": [str],
    "notetype": [str],
    "_notetype": [str]
}

reference_schema = {
    "id": [str],
    "idtype": [str],
    "_idtype": [str]
}

dates_schema = {
    "date": [str],  # yyyy-mm-dd
    "datetype": [str],  # always "RESPOND BY", "EP", or "LP"?None
    "time": [str, type(None)],  # hh:mm
    "timetype": [str, type(None)]
    # always "MUST RESPOND BY", "EARLIEST REQUESTED (PICKUP|DROP) TIME", "LATEST REQUESTED (PICKUP|DROP) TIME"?
}

contact_schema = {
    "contactname": [str, type(None)],
    "contact_type": [str, type(None)],
    "contact_number": [str, type(None)],
    "contact_number_type": [str, type(None)]
}

purchase_order_schema = {
    "purchase_order_number": [str, type(None)],
    "date": [str, type(None)],
    "cases": [str, type(None)],  # quantity
    "weight_unit_code": [str, type(None)],  # "L" for pounds, "K" for Kilo
    "weight": [str, type(None)],
    "volume_type": [str, type(None)],  # "cubic feet", etc
    "volume_units": [str, type(None)]
}

global schema_check_passed


def schema_keys_validator(schema, actual_dict, key_type, only_warnining=True):
    global schema_check_passed
    try:
        schema_keys = list(schema.keys())
        actual_keys = list(actual_dict.keys())
        matched_keys = list()
        for key in schema_keys:
            if key in actual_keys:
                actual_keys.remove(key)
                matched_keys.append(key)

        if len(actual_keys) > 0:
            print(Fore.RED + f"[FAILED][{key_type} KEYS NOT FOUND]:{actual_keys}" + Fore.BLACK)
            schema_check_passed = False
            return actual_keys, matched_keys, False
        else:
            if not only_warnining:
                print(Fore.GREEN + f'[PASSED][ALL {key_type} KEY FOUND]' + Fore.BLACK)
            return actual_keys, matched_keys, True

    except Exception as e:
        schema_check_passed = False
        print(Fore.RED + f"[FAILED][SCHEMA-CHECK][schema_keys_validator][{e}][{Exception}]" + Fore.BLACK)


def schema_key_type_validator(schema, actual_dict, key_type, only_warnining=True):
    global schema_check_passed
    try:
        schema_check = list()
        matched_type_keys = list()
        for key in list(schema.keys()):
            for value in schema[key]:
                if isinstance(actual_dict[key], value):
                    matched_type_keys.append(key)
                    #                 print(f"{key}: PASSED")
                    break
            else:
                schema_check.append(key)

        if len(schema_check) > 0:
            print(Fore.RED + f"[FAILED][TYPES NOT MATCHED][{key_type}]: {schema_check}" + Fore.BLACK)
            schema_check_passed = False
            return schema_check, matched_type_keys, False
        else:
            if not only_warnining:
                print(Fore.GREEN + f"[PASSED][TYPES MATCHED][{key_type}]" + Fore.BLACK)
            return schema_check, matched_type_keys, True
    except Exception as e:
        schema_check_passed = False
        print(Fore.RED + f"[FAILED][SCHEMA-CHECK][schema_key_type_validator][{e}][{Exception}]" + Fore.BLACK)


def rate_con_schema_validation(actual_rate_con, rate_con_schema, stop_schema, entity_schema, note_schema, reference_schema,
                        purchase_order_schema, contact_schema, dates_schema, shipment_schema, receiver_schema,
                        only_warning=True):
    global schema_check_passed
    try:
        base_keys, matched_keys, success = schema_keys_validator(rate_con_schema, actual_rate_con, 'RATECON',
                                                                 only_warning)
        if success:
            base_keys, base_schema_matched_type_keys, success = schema_key_type_validator(rate_con_schema,
                                                                                          actual_rate_con, 'RATECON',
                                                                                          only_warning)
            base_keys, matched_keys, success = schema_keys_validator(shipment_schema, actual_rate_con['shipment'],
                                                                     'SHIPMENT', only_warning)

            if 'shipment' in base_schema_matched_type_keys:
                base_keys, shipment_schema_matched_type_keys, success = schema_key_type_validator(shipment_schema,
                                                                                                  actual_rate_con[
                                                                                                      'shipment'],
                                                                                                  'SHIPMENT',
                                                                                                  only_warning)

            if 'receiver' in base_schema_matched_type_keys:
                base_keys, matched_keys, receiver_success = schema_keys_validator(receiver_schema,
                                                                                  actual_rate_con['receiver'],
                                                                                  'RECEIVER', only_warning)
                if success:
                    base_keys, receiver_schema_matched_type_keys, success = schema_key_type_validator(receiver_schema,
                                                                                                      actual_rate_con[
                                                                                                          'receiver'],
                                                                                                      'RECEIVER',
                                                                                                      only_warning)

            if 'entities' in base_schema_matched_type_keys:
                for n, entity in enumerate(actual_rate_con['entities']):
                    if type(entity) == dict:
                        base_keys, matched_keys, success = schema_keys_validator(entity_schema, entity, 'ENTITY',
                                                                                 only_warning)
                        if success:
                            base_keys, entity_schema_matched_type_keys, success = schema_key_type_validator(
                                entity_schema, entity, 'ENTITY', only_warning)
                            if 'contacts' in entity_schema_matched_type_keys:
                                base_keys, matched_keys, success = schema_keys_validator(contact_schema,
                                                                                         entity['contacts'],
                                                                                         'ENTITY-CONTACT', only_warning)
                                if success:
                                    base_keys, matched_type_keys, success = schema_key_type_validator(contact_schema,
                                                                                                      entity[
                                                                                                          'contacts'],
                                                                                                      'ENTITY-CONTACT',
                                                                                                      only_warning)
                    else:
                        schema_check_passed = False
                        print(Fore.RED + f'[FAILED][ENTITY][{type(entity)} TYPE WRONG]' + Fore.BLACK)

            if 'stops' in base_schema_matched_type_keys:
                for n, stop in enumerate(actual_rate_con['stops']):
                    if type(stop) == dict:
                        base_keys, matched_keys, success = schema_keys_validator(stop_schema, stop, 'STOPS',
                                                                                 only_warning)
                        if success:
                            base_keys, stop_schema_matched_type_keys, success = schema_key_type_validator(stop_schema,
                                                                                                          stop,
                                                                                                          'STOPS',
                                                                                                          only_warning)
                            if "entities" in stop_schema_matched_type_keys:
                                for entity in stop['entities']:
                                    if type(entity) == dict:
                                        base_keys, matched_keys, success = schema_keys_validator(entity_schema, entity,
                                                                                                 'STOPS-ENTITY',
                                                                                                 only_warning)
                                        if success:
                                            base_keys, entity_schema_matched_type_keys, success = schema_key_type_validator(
                                                entity_schema, entity, 'STOP-ENTITY', only_warning)
                                            if 'contacts' in entity_schema_matched_type_keys:
                                                base_keys, matched_keys, success = schema_keys_validator(contact_schema,
                                                                                                         entity[
                                                                                                             'contacts'],
                                                                                                         'STOPS-ENTITY-CONTACT',
                                                                                                         only_warning)
                                                if success:
                                                    base_keys, matched_type_keys, success = schema_key_type_validator(
                                                        contact_schema, entity['contacts'], 'STOP-ENTITY-CONTACT',
                                                        only_warning)
                                    else:
                                        schema_check_passed = False
                                        print(
                                            Fore.RED + f'[FAILED][STOP-ENTITY][{type(entity)}TYPE WRONG]' + Fore.BLACK)

                            if "order_detail" in stop_schema_matched_type_keys:
                                for purchase_order in stop['order_detail']:
                                    if type(purchase_order) == dict:
                                        base_keys, matched_keys, success = schema_keys_validator(purchase_order_schema,
                                                                                                 purchase_order,
                                                                                                 'STOPS-PURCHASE-ORDER',
                                                                                                 only_warning)
                                        if success:
                                            base_keys, matched_type_keys, success = schema_key_type_validator(
                                                purchase_order_schema, purchase_order, 'STOP-PURCHASE-ORDER',
                                                only_warning)
                                    else:
                                        schema_check_passed = False
                                        print(
                                            Fore.RED + f'[FAILED][STOP-ENTITY][{type(purchase_order)}TYPE WRONG]' + Fore.BLACK)

                            if "references" in stop_schema_matched_type_keys:
                                for reference in stop['references']:
                                    if type(reference) == dict:
                                        base_keys, matched_keys, success = schema_keys_validator(reference_schema,
                                                                                                 reference,
                                                                                                 'STOP-REFERENCE',
                                                                                                 only_warning)
                                        if success:
                                            base_keys, matched_type_keys, success = schema_key_type_validator(
                                                reference_schema,
                                                reference,
                                                'STOP-REFERENCE',
                                                only_warning)
                                    else:
                                        schema_check_passed = False
                                        print(
                                            Fore.RED + f'[FAILED][STOP-REFERENCE]{type(reference)}TYPE WRONG]' + Fore.BLACK)

                            if "notes" in stop_schema_matched_type_keys:
                                for note in stop['notes']:
                                    if type(note) == dict:
                                        base_keys, matched_keys, success = schema_keys_validator(note_schema, note,
                                                                                                 'STOP-NOTES',
                                                                                                 only_warning)
                                        if success:
                                            base_keys, matched_type_keys, success = schema_key_type_validator(
                                                note_schema, note,
                                                'STOP-NOTES',
                                                only_warning)
                                    else:
                                        schema_check_passed = False
                                        print(Fore.RED + f'[FAILED][STOP-NOTES]{type(note)}TYPE WRONG]' + Fore.BLACK)

                            if "dates" in stop_schema_matched_type_keys:
                                for date in stop['dates']:
                                    if type(date) == dict:
                                        base_keys, matched_keys, success = schema_keys_validator(dates_schema, date,
                                                                                                 'STOP-DATE',
                                                                                                 only_warning)
                                        if success:
                                            base_keys, matched_type_keys, success = schema_key_type_validator(
                                                dates_schema,
                                                date, 'STOP-DATE',
                                                only_warning)
                                    else:
                                        schema_check_passed = False
                                        print(Fore.RED + f'[FAILED][STOP-DATE]{type(date)}TYPE WRONG]' + Fore.BLACK)

                    else:
                        schema_check_passed = False
                        print(Fore.RED + f'[FAILED][STOP-ENTITY][{type(stop)}TYPE WRONG]' + Fore.BLACK)

            if 'references' in base_schema_matched_type_keys:
                for reference in actual_rate_con['references']:
                    if type(reference) == dict:
                        base_keys, matched_keys, success = schema_keys_validator(reference_schema, reference,
                                                                                 'REFERENCE',
                                                                                 only_warning)
                        if success:
                            base_keys, matched_type_keys, success = schema_key_type_validator(reference_schema,
                                                                                              reference,
                                                                                              'REFERENCE', only_warning)
                    else:
                        schema_check_passed = False
                        print(Fore.RED + f'[FAILED][REFERENCE][{type(reference)}TYPE WRONG]' + Fore.BLACK)

            if 'dates' in base_schema_matched_type_keys:
                for date in actual_rate_con['dates']:
                    if type(date) == dict:
                        base_keys, matched_keys, success = schema_keys_validator(dates_schema, date, 'DATES',
                                                                                 only_warning)
                        if success:
                            base_keys, matched_type_keys, success = schema_key_type_validator(dates_schema, date,
                                                                                              'DATES',
                                                                                              only_warning)
                    else:
                        schema_check_passed = False
                        print(Fore.RED + f'[FAILED][DATES][{type(date)}TYPE WRONG]' + Fore.BLACK)

            if 'notes' in base_schema_matched_type_keys:
                for note in actual_rate_con['notes']:
                    if type(note) == dict:
                        base_keys, matched_keys, success = schema_keys_validator(note_schema, note, 'NOTES',
                                                                                 only_warning)
                        if success:
                            base_keys, matched_type_keys, success = schema_key_type_validator(note_schema, note,
                                                                                              'NOTES',
                                                                                              only_warning)
                    else:
                        schema_check_passed = False
                        print(Fore.RED + f'[FAILED][NOTES][{type(note)}TYPE WRONG]' + Fore.BLACK)
    except Exception as e:
        schema_check_passed = False
        print(Fore.RED + f"[FAILED][SCHEMA-CHECK][rate_con_validation][{e}][{Exception}]" + Fore.BLACK)


def check_rate_con_schema(rate_con, only_warning=True):
    global schema_check_passed
    try:
        schema_check_passed = True
        rate_con_schema_validation(actual_rate_con=rate_con,
                                   rate_con_schema=rate_con_schema,
                                   stop_schema=stop_schema,
                                   entity_schema=entity_schema,
                                   note_schema=note_schema,
                                   reference_schema=reference_schema,
                                   purchase_order_schema=purchase_order_schema,
                                   contact_schema=contact_schema,
                                   dates_schema=dates_schema,
                                   shipment_schema=shipment_schema,
                                   receiver_schema=receiver_schema,
                                   only_warning=only_warning)
        if schema_check_passed is True:
            print(Fore.GREEN + f"[PASSED][ALL-SCHEMA-CHECK]" + Fore.BLACK)
        else:
            print(Fore.RED + f"[FAILED][SCHEMA-CHECK]" + Fore.BLACK)

        return schema_check_passed
    except Exception as e:
        schema_check_passed = False
        print(Fore.RED + f"[FAILED][SCHEMA-CHECK][rate_con_validation][{e}][{Exception}]")
        return schema_check_passed
