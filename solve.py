from binaryninja import BinaryViewType

bv = BinaryViewType.get_view_of_file("/home/chris/ctfs/imaginary/rev/vmmod_player/out.bin")

def sub_17e(r10):
    r12 = 0
    r11 = r10
    r11 = r11 & 1
    r12 = r12 ^ r11
    r11 = r10
    r11 = r11 >> 1
    r11 = r11 & 2
    r12 = r12 ^ r11
    r11 = r10
    r11 = r11 >> 2
    r11 = r11 & 4
    r12 = r12 ^ r11
    r11 = r10
    r11 = r11 >> 3
    r11 = r11 & 8
    r12 = r12 ^ r11
    r10 = r12
    return r10

def sub_147(r10):
    r12 = 0
    r11 = r10
    r11 = r11 >> 1
    r11 = r11 & 1
    r12 = r12 ^ r11
    r11 = r10
    r11 = r11 >> 2
    r11 = r11 & 2
    r12 = r12 ^ r11
    r11 = r10
    r11 = r11 >> 3
    r11 = r11 & 4
    r12 = r12 ^ r11
    r11 = r10
    r11 = r11 >> 4
    r11 = r11 & 8
    r12 = r12 ^ r11
    r10 = r12
    return r10

b = bv.read(0x1e1,0x36)
x = list(b)
r0 = 0
while True:
    val = b[r0]
    r4 = sub_17e(val)
    r10 = sub_147(val)
    r10 = r10 << 4
    r4 = r4^r10
    x[r0] = r4
    r0 = r0 - 0x35
    if r0 == 0:
        break
    else:
        r0 = r0+0x36

flipper = 0
def sub_100(r10,r11,r12):
    r0 = 0
    global flipper
    while True:
        if flipper%2==0:
            r10 = r10 & r11
        else:
            r10 = r10 ^ r11
        flipper += 1
        r11 = r12
        r0 -= 1
        if r0 == 0:
            return r10
        else:
            r0+=2

flag = b"ictf"
flag_test = [0]*50
correct = bytes(x)
r0 = 0
r5 = 0
r11 = 0x69
while True:
    tmp_r11=r11
    r10 = flag_test[r0]
    r12 = 0x54
    r10 = sub_100(r10,r11,r12) 
    r3 = r10
    r10 = flag_test[r0]
    r11 = ~r11
    r12 = 0x12
    r12 = ~r12
    r10 = sub_100(r10,r11,r12)
    r4 = r10
    r10 = correct[r5]
    r5 += 1
    r10 = (r10^r3)%256
    if r10 == 0:
        r10 = correct[r5]
        r5 += 1
        r10 = (r10 ^ r4)%256
        if r10 == 0:
            flag+=bytes([flag_test[r0]])
            r11 = r3
            r11 = r11 + r4
            r0 += 1
            r0 -= 27
            if r0 == 0:
                print(flag)
                exit()
            else:
                r0 += 27
        else:
            r5-=1
            flag_test[r0] += 1
            r5-=1
            r11=tmp_r11
    else:
        flag_test[r0] += 1
        r5-=1
        r11=tmp_r11
        
