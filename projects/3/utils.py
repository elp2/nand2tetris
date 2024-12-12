def ram8():
    for i in range(64):
        group = i // 8
        num = i % 8
        print(f'\tRAM8(in= in, load= l{group}{num}, address= address[0..2], out= r{group}{num});')
    print("----")
    for lg in range(8):
        print(f'\tDMux8Way(in= l{lg}, sel= address[0..2], a= l{lg}0, b= l{lg}1, c= l{lg}2, d= l{lg}3, e= l{lg}4, f= l{lg}5, g= l{lg}6, h= l{lg}7);')
    print("----")

    for lg in range(8):
        print(f'\tMux8Way16(a= r{lg}0, b= r{lg}1, c= r{lg}2, d= r{lg}3, e= r{lg}4, f= r{lg}5, g= r{lg}6, h= r{lg}7, sel= address[0..2], out=r{lg});')
    print("----")


    

ram8()