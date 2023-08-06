from colorama import Fore


def check_rate_con_data(rate_con):
    try:
        data_check_passed = True
        if type(rate_con['shipment']) == dict:
            if rate_con['shipment']['charges'] is None:
                print(Fore.RED + f"[FAILED]['DATA-CHECK'][SHIPMENT-CHARGES][{type(rate_con['shipment']['charges'])}]" + Fore.BLACK)
                data_check_passed = False

        if type(rate_con['shipment']) != dict:
            print(Fore.RED + f"[FAILED]['DATA-CHECK'][SHIPMENT][{type(rate_con['shipment'])}]" + Fore.BLACK)
            data_check_passed = False

        if type(rate_con['receiver']) != dict:
            print(Fore.RED + f"[FAILED]['DATA-CHECK'][RECEIVER][{type(rate_con['receiver'])}]" + Fore.BLACK)
            data_check_passed = False

        if type(rate_con['sender']) != str:
            print(Fore.RED + f"[FAILED]['DATA-CHECK'][SENDER][{type(rate_con['sender'])}]" + Fore.BLACK)
            data_check_passed = False

        if type(rate_con['client']) != str:
            print(Fore.RED + f"[FAILED]['DATA-CHECK'][CLIENT][{type(rate_con['client'])}]" + Fore.BLACK)
            data_check_passed = False

        if type(rate_con['entities']) == list:
            for entity in rate_con['entities']:
                if type(entity['name']) != str:
                    print(Fore.RED + f"[FAILED]['DATA-CHECK'][ENTITIES][NAME][{type(entity['name'])}]" + Fore.BLACK)
                    data_check_passed = False

                if type(entity['city']) != str:
                    print(Fore.RED + f"[FAILED]['DATA-CHECK'][ENTITIES][CITY][{type(entity['city'])}]" + Fore.BLACK)
                    data_check_passed = False

                if type(entity['state']) != str:
                    print(Fore.RED + f"[FAILED]['DATA-CHECK'][ENTITIES][STATE][{type(entity['state'])}]" + Fore.BLACK)
                    data_check_passed = False

                if type(entity['postal']) != str:
                    print(Fore.RED + f"[FAILED]['DATA-CHECK'][ENTITIES][POSTAL][{type(entity['postal'])}]" + Fore.BLACK)
                    data_check_passed = False

        if type(rate_con['stops']) == list:
            if len(rate_con['stops']) > 0:
                for stop in rate_con['stops']:
                    if type(stop['_stoptype']) != str:
                        print(Fore.RED + f"[FAILED]['DATA-CHECK'][STOP][_STOP-TYPE][{type(stop['_stoptype'])}]" + Fore.BLACK)
                        data_check_passed = False

                    if type(stop['stoptype']) != str:
                        print(Fore.RED + f"[FAILED]['DATA-CHECK'][STOP][STOP-TYPE][{type(stop['stoptype'])}]" + Fore.BLACK)
                        data_check_passed = False

                    if type(stop['order_detail']) == list:
                        if len(stop['order_detail']) < 1:
                            print(Fore.RED + f"[FAILED]['DATA-CHECK'][STOP][NO-order_detail][{len(stop['order_detail'])}]" + Fore.BLACK)
                            data_check_passed = False

                    if type(stop['dates']) == list:
                        if len(stop['dates']) < 1:
                            print(Fore.RED + f"[FAILED]['DATA-CHECK'][STOP][NO-STOP-DATES][{len(stop['dates'])}]" + Fore.BLACK)
                            data_check_passed = False

                    for entity in stop['entities']:
                        # if type(entity['address']) == list:
                        #     if len(entity['address']) == 0:
                        #         print(Fore.RED + f"[FAILED]['DATA-CHECK'][ENTITIES][Address-Length][{type(entity['address'])}]" + Fore.BLACK)
                        #         data_check_passed = False

                        if type(entity['name']) != str:
                            print(Fore.RED + f"[FAILED]['DATA-CHECK'][ENTITIES][NAME][{type(entity['name'])}]" + Fore.BLACK)
                            data_check_passed = False

                        if type(entity['city']) != str:
                            print(Fore.RED + f"[FAILED]['DATA-CHECK'][ENTITIES][CITY][{type(entity['city'])}]" + Fore.BLACK)
                            data_check_passed = False

                        if type(entity['state']) != str:
                            print(Fore.RED + f"[FAILED]['DATA-CHECK'][ENTITIES][STATE][{type(entity['state'])}]" + Fore.BLACK)
                            data_check_passed = False

                        if type(entity['postal']) != str:
                            print(Fore.RED + f"[FAILED]['DATA-CHECK'][ENTITIES][POSTAL][{type(entity['postal'])}]" + Fore.BLACK)
                            data_check_passed = False
            else:
                print(Fore.RED + f"[FAILED]['DATA-CHECK'][STOP][NO-STOPS-FOUND][{len(rate_con['stops'])}]" + Fore.BLACK)
                data_check_passed = False

        if data_check_passed is True:
            print(Fore.GREEN + f"[PASSED][ALL-DATA-CHECK]" + Fore.BLACK)
        else:
            print(Fore.RED + f"[FAILED][DATA-CHECK]" + Fore.BLACK)

        return data_check_passed
    except Exception as e:
        data_check_passed = False
        print(Fore.RED + f"[FAILED][RateCon-DataCheck-Error][{e}][{Exception}]" + Fore.BLACK)
        return data_check_passed
