#  BLANK main DICTIONARY:
def get_rate_confirmation_schema():
    rate_confirmation_schema = {
                                    "transaction_type": "204",
                                    "sender": None,  # BROKER or SHIPPER if they are not having a broker. Example: "Werner Logistics"
                                    "receiver": {
                                                "name": None,  # carrier-name on top right of page
                                                "isa_qual": "ZZ",  # hard-coded
                                                "isa_ID": None  # client email
                                                },
                                    "client": None,  # hard-coded. Example: "Werner Logistics"
                                    "submitted_time": None,     # time we received the email
                                    "identifier": None,
                                    "identifier_type": None,
                                    "shipment": {
                                                    "equipment_number": None,
                                                    "weight": None,
                                                    "weight_unit_code": None,
                                                    "weight_qualifier": "GROSS WEIGHT",  # hard-coded
                                                    "volume": None,
                                                    "volume_qualifier": None,
                                                    "truck_type": None,
                                                    "temperature": None,
                                                    "trucklength": None,
                                                    "charges": None,
                                                    "loading_quantity": None
                                                },
                                    "purpose": "ORIGINAL",
                                    "references": [],  # append references_schema here for reference numbers ABOVE Shipper/Consignee
                                    "dates": [],  # append dates_schema here if any, don't include stop dates
                                    "notes": [],  # append notes_schema here for notes/comments ABOVE Shipper/Consignee
                                    "entities": [],  # append entities_schema here
                                    "stops": [],  # append stops_schema here
                                }
    return rate_confirmation_schema


# BLANK references DICTIONARY:
# used for rate-con level references as well as stop-level references
def get_reference_schema():
    reference_schema = {
                            "id": None,
                            "idtype": None,
                            "_idtype": None
                        }
    return reference_schema


# BLANK dates DICTIONARY:
def get_dates_schema():
    dates_schema = {
                        "date": None,  # dd/mm/yyyy hh:mm
                        "datetype": None,  # always "RESPOND BY", "EP", or "LP"?None
                        "time": None,
                        "timetype": None  # always "MUST RESPOND BY", "EARLIEST REQUESTED (PICKUP|DROP) TIME", "LATEST REQUESTED (PICKUP|DROP) TIME"?
                   }

    return dates_schema


# BLANK references DICTIONARY:
# used for rate-con level notes as well as stop-level notes
def get_note_schema():
    note_schema = {
                    "note": None,
                    "notetype": None,
                    "_notetype": None
                  }
    return note_schema


# BLANK entities DICTIONARY VARIABLE:
#  can be Broker, Shipper, or Consignee
def get_entity_schema(entity_type):
    entity_schema = {
                        "name": None,
                        "type": None,
                        "_type": None,
                        "id": "10",  # hard-coded
                        "idtype": "MUTUALLY DEFINED",  # hard-coded
                        "_idtype": "ZZ",  # hard-coded
                        "address": [],     # List object ['address part 1', 'address part 2']
                        "city": None,
                        "state": None,
                        "postal": None,
                        "country": None,
                        "contacts": {
                                        "contactname": None,
                                        "contact_type": None,
                                        "contact_number": None,
                                        "contact_number_type": None
                                    }
                    }

    if entity_type.upper() == "SHIPPER":
        entity_schema['type'] = "SHIPPER"
        entity_schema['_type'] = "SH"
        return entity_schema
    elif entity_type.upper() == "CONSIGNEE":
        entity_schema['type'] = "CONSIGNEE"
        entity_schema['_type'] = "CN"
        return entity_schema
    elif entity_type.upper() == "BROKER":
        entity_schema['type'] = "BROKER"
        entity_schema['_type'] = "BK"
        return entity_schema
    else:
        print("Select correct entity type (SHIPPER/CONSIGNEE/BROKER)")
    return entity_schema


# BLANK purchase_order DICTIONARY to be appended to "order_detail" in stops dictionary IF:
# -- if only ONE PO, fill out "stops"["order_detail"] and ignore this extra dictionary.
# -- if multiple PO's use this dictionary and append to "order_detail"["purchase_order_number"] in stops dictionary.
def get_purchase_order_schema():
    purchase_order_schema = {
                                "purchase_order_number": None,
                                "date": None,
                                "cases": None,  # quantity
                                "weight_unit_code": None,  # "L" for pounds, "K" for Kilo
                                "weight": None,
                                "volume_type": None,  # "cubic feet", etc
                                "volume_units": None
                            }
    return purchase_order_schema


# BLANK stops DICTIONARY:
#  _stopType Codes for Picks & Drops:
#  Picks:
#  LD (Load)   <--- Duke to use this one in general
#  PL (Partial Load)
#  CL (Complete Load)
#  RT (Retrieval of Trailer)

#  Drops:
#  UL (Unload)  <-- Duke to use this one in general
#  PU (Partial Unload)
#  CU (Complete Unload)
#  DT (Drop Trailer)

def get_stops_schema(stop_type: str, ordinal: int):
    stop_schema = {
                    "stoptype": None,  # see stoptype codes for pickups and drops
                    "_stoptype": None,  # see stoptype codes for pickups and drops
                    "ordinal": ordinal,  # starts from 1, EX: 1,2,3,4
                    "dates": [],  # append dates_schema here
                    "references": [],  # append references_schema here for stop references
                    "order_detail": [],
                    "entities": [],  # append entities_schema here for stop-level entities
                    "notes": []  # append notes_schema here for stop-level notes/comments
                }

    if stop_type.upper() == "PICK":
        stop_schema['stoptype'] = "PICK"
        stop_schema['_stoptype'] = "LD"
        return stop_schema
    elif stop_type.upper() == "DROP":
        stop_schema['stoptype'] = "DROP"
        stop_schema['_stoptype'] = "UL"
        return stop_schema
    else:
        print("Select correct entity type (PICK/DROP)")
    return stop_schema
