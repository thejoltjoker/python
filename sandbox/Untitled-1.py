for i in range(1000):
    print("=IFERROR(VLOOKUP(A{},BOXES!A1:D99, 4, 0))".format(i))
