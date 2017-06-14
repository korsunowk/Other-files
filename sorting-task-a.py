import time

str_index = 0
int_index = 0


def sort_keys(text):
    global str_index

    if text.isdigit():
        str_index += 1
        return int(text)
    else:
        return text


def sorting(origin_list, sorted_list):
    global str_index, int_index
    output = []
    for el in origin_list:
        if el.isdigit():
            output.append(sorted_list[int_index])
            int_index += 1
        else:
            output.append(sorted_list[str_index])
            str_index += 1

    return output


def main():
    origin_text = "car 10 truck 8 4 bus 6 1" * 1000000
    start = time.time()
    origin_list = origin_text.split()
    sorted_list = sorted(origin_list, key=sort_keys)
    output = sorting(origin_list, sorted_list)
    end = time.time()
    print(end-start)
    # print(origin_text)
    # print(" ".join(output))


if __name__ == '__main__':
    main()
