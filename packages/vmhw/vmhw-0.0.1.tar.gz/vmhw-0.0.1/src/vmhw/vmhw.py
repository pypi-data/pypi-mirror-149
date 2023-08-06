def create_text():
    text = input('What would be the text? Enter it with space:')
    text = text.split()
    for i in range (len(text)):
        try:
            text[i] = int(text[i])
        except:
            pass
    return text


def VM():
    text = create_text()
    _list = input('Please enter the instructions you want to operate or simply a number, seperate by space:')
    _list = _list.split(" ")
    empty = []
    X = []
    for i in range (len(_list)):
        if _list[i] == 'load':
            index = int(_list[i+1])
            empty.append(text[index])
        elif _list[i] == 'print':
            print(empty[-1])
            empty.pop()
        elif _list[i] == 'dup':
            copy = empty[-1]
            empty.pop()
            empty.append(copy)
            empty.append(copy)
        elif _list[i] == 'add_two':
            X.append(int(empty.pop()))
            X.append(int(empty.pop()))
            empty.append(X[0] + X[1])
        elif _list[i] == 'mul_two':
            X.append(int(empty.pop()))
            X.append(int(empty.pop()))
            empty.append(X[0] * X[1])
        elif _list[i] == 'mod_two':
            X.append(int(empty.pop()))
            X.append(int(empty.pop()))
            empty.append(X[0] % X[1])
        elif _list[i] == 'toint':
            temp = []
            temp.append(int(float(empty[-1])))
            empty.pop()
            empty.append(temp[-1])
        elif _list[i] == 'jump':
            index = int(_list[i+1])
            i == index
        elif _list[i] == 'jump_if':
            number = int(_list[i+1])
            if int(empty[-1]) != number:
                new_index = int(_list[i+2])
                i = new_index + i
                
        if len(_list) == 1:
            try:
                num = int(_list[i])
                if num % 2 == 0:
                    print('The number {} is even'.format(num))
                else:
                    print('The number {} is odd'.format(num))
            except:
                print('Invalid Entry. Please try again')