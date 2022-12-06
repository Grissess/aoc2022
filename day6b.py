def som(s, sz=4):
    for i in range(len(s) - sz):
        sl = s[i:i+sz]
        if len(set(sl)) == sz:
            return i+sz
    return None

while True:
    t = input('Message: ')
    print(som(t, 14))
