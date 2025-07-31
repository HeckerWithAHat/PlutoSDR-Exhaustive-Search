def lempel_ziv_encoding(raw_text):
    main_output = ""
    dict_index = 1
    encoding = {}
    text = list(raw_text)
    i = 1
    encoding[text[0]] = dict_index
    dict_index += 1
    main_output += str(1)
    main_output += str(0)
    main_output += text[0]
    while i < len(text):
        char = text[i]
        if char in encoding.keys():
            string = char
            j = i + 1

            while ((string in encoding.keys()) and j < len(text)):
                string += text[j]
                j += 1
            if string not in encoding.keys():
                still_in_dict = string[:-1]
                new_char = string[-1]
                inx = encoding.get(still_in_dict)
                length = len(str(inx))
                main_output += str(length)
                main_output += str(inx)
                main_output += new_char
                encoding[string] = dict_index
                dict_index += 1
            else:
                inx = encoding.get(string)
                length = len(str(inx))
                main_output += str(length)
                main_output += str(inx)
        else:
            encoding[char] = dict_index
            main_output += str(1)
            main_output += str(0)
            main_output += char
            dict_index += 1
            j = i + 1
        i = j
    return format(int(main_output), 'b')

def lempel_ziv_decoding(encoded_text):
    decoding = {}
    decoded_output = ""
    i = 0
    dict_index = 1
    encoded_text = ''.join(list(map(str, encoded_text)))
    encoded_text = str(int(encoded_text, 2))
    while i < len(encoded_text):
        length_of_index = int(encoded_text[i])
        i += 1
        if length_of_index == 0:
            char = encoded_text[i]
            i += 1
            decoded_output += char
            decoding[dict_index] = char
            dict_index += 1
        else:
            index = int(encoded_text[i:i + length_of_index])
            i += length_of_index

            if i < len(encoded_text):
                char = encoded_text[i]
                i += 1
                if index == 0:
                    string = char
                else:
                    string = decoding[index] + char
            else:
                string = decoding[index]

            decoded_output += string
            decoding[dict_index] = string
            dict_index += 1
    return decoded_output