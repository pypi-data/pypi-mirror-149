# Task 1
def fuzz_buzz():
    for i in range(1, 101):
        if i % 3 == 0:
            if i % 5 == 0:
                print("FuzzBuzz")
                continue
            print("Fuzz")
        elif i % 5 == 0:
            print("Buzz")
        else:
            print(i)


# Task 2
def min_max():
    numbers = [1, 2, '0', '300', -2.5, 'Dog', True, 0o1256, None]


# Task 3
def max_letters_count():
    with open("text.txt", "r") as file:
        tmp_text = file.read()
    char_dict = dict()

    for i in tmp_text.lower():
        if i.isalpha():
            if i in char_dict:
                char_dict[i] += 1
            else:
                char_dict[i] = 0

    max_count_letter = max(char_dict, key=char_dict.get)

    return max_count_letter, char_dict[max_count_letter]


# Task 3
def words_count(queried_word):
    with open("/HWs/week1/text.txt", "r") as file:
        tmp_text = file.read()

    res_dict = {}
    words = tmp_text.split()
    for word in words:
        word = word.strip()
        if word not in res_dict:
            res_dict[word] = 1
        else:
            res_dict[word] += 1

    if queried_word in res_dict:
        return res_dict[queried_word]
    else:
        return 0


# Task 4
def file_size(size):
    ll = ["B", "Kb", "Mb", "Gb"]
    for i in ll:
        if (size // 1024 == 0) or (i == "Gb"):
            return f"{round(float(size), 1)}{i}"
        size /= 1024


# Task 5
def count_multiples_of_3_and_5(max_val):
    res = 0
    for i in range(1, max_val):
        if (i % 3 == 0) or (i % 5 == 0):
            res += i
    return res


if __name__ == '__main__':
    print(words_count('Python'))
