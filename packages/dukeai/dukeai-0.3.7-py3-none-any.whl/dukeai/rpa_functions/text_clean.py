def data_clean(text):
    try:
        strip_po = [i.strip() for i in text.split('\n')]
        remove_space = [i for i in strip_po if i not in [' ', '']]
        remove_space_between = [i.split('  ') for i in remove_space]
        cleaned_data = list()
        count = 0
        for i in remove_space_between:
            cleaned_data.append([])
            for j in i:
                if j not in ['']:
                    cleaned_data[count].append(j.strip())
            count += 1

        return cleaned_data

    except Exception as e:
        print(f"[KVT-EXTRACT][Data-Clean-Error][{str(e)}]")
        return []
