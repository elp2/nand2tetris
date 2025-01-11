        # do Output.create(49,3084, 3598, 3855, 3084, 3084, 3084, 3084, 3084, 16191, 0, 0); // 1
        # # do Output.create(50,7710, 13107, 12336, 6168, 3084, 1542, 771, 13107, 16191, 0, 0);   // 2



def extractchars(line):
    line = line.replace("\n", "")
    if "do Output.create" not in line:
        return line
    
    doc_start = line.find("do Output.create")
    nums_start = line.find(",", doc_start)
    nums_end = line.find(");", nums_start)
    nums = line[nums_start+1:nums_end].split(",")

    pixels = [int(n) for n in nums]

    # Double each glyph.
    pixels = [str(twos_complement(format(p, f"0{8}b"))) for p in pixels]

    return line[:nums_start] + ", " + ", ".join(pixels) + line[nums_end:]

def twos_complement(asbin):
    if asbin[0] == "1":
        return int(asbin+asbin, 2) - pow(2, 16)
    else:
        return int(asbin+asbin, 2)

def doublechars(charArray):
    ret = []
    for c in charArray:
        asbin = format(c, f"0{8}b")
        ret.append(twos_complement(asbin))
    return ret

def main():
    # Duplicates the characters to fill all 16 bits.
    with open('Output.jack', 'r') as f:
        lines = f.readlines()

    ret = []
    # Process each line
    for line in lines:
        ret.append(extractchars(line))
    print("\n".join(ret))

if __name__ == '__main__':
    main()
