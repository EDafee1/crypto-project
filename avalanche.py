def getAva(cipher):
    a = cipher
    a = int(''.join(format(ord(x), 'b') for x in a))
    b = [int(x) for x in str(a)]

    if b[0] == 1:
        b[0] = 0
    elif b[0] == 0:
        b[0] = 1

    b = int(''.join([str(n) for n in b]))

    a_xor_b = a ^ b

    bin_a_xor_b = bin(a_xor_b)

    one_count = 0
    for i in bin_a_xor_b:
        if i == "1":
            one_count+=1

    len_a = len(bin(a))
    len_b = len(bin(b))

    if (len_a) >= (len_b):
        AVA = (one_count/ len (bin(a))) * 100
    else:
        AVA = (one_count/ len (bin(b))) * 100

    return AVA