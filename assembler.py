from cProfile import label


def to_bin(num):
    num = str(bin(int(num)))[2:]
    if len(num) < 3:
        while len(num) < 3:
            num = "0" + num
    return num


def command_line(line):

    command_name = ""
    command_name_started = False
    command_name_over = False
    is_firstr = True
    firstr = ""
    secondr = ""
    result = ""
    result2 = ""
    tempr = ""
    addmode = ""

    for letter in line:

        if not command_name_over:
            if not command_name_started:

                if letter == " ":
                    continue
                
                if letter.islower():
                    command_name += letter
                    command_name_started = True
                    continue
                else:
                    raise Exception("Invalid line")
            else:
                if letter.islower():
                    command_name += letter
                    continue
                if letter == " ":
                    command_name_over = True
                    if command_name in opcode_dict:
                        result += opcode_dict[command_name]
                        continue
                    else:
                        raise Exception("invalid command")

        if letter == " ":
            continue

        if letter == ",":
            is_firstr = False
            continue
        
        if is_firstr == True:
             firstr += letter
             continue
        
        else:
            secondr += letter
            continue

    if command_name == "nop":
        result += "1111"
    firstr = firstr.strip()
    secondr = secondr.strip()

    if (firstr == "" and secondr == "") or (firstr[0] == "r" and secondr == "") or (firstr[0] == "r" and secondr[0] == "r"):
        if firstr.strip() == "":
            result += "000000000000"
        else:
            tempr = to_bin(firstr[1])
            result += tempr

            if secondr == "":
                result += "000000000"

            else:
                tempr = to_bin(secondr[1])
                result += "00"
                result += tempr
                result += "0000"
    else:
        if firstr[0].isupper() and firstr[-1].isnumeric():
            result += "000110000000"
            result2 = firstr
        else:
            if firstr[0].isupper():
                result += "000100000000"
                result2 = firstr
            else:
                if secondr[0].isnumeric():
                    tempr = to_bin(firstr[1])
                    result += tempr
                    result += "010000000"
                    tempr = str(bin(int(secondr)))[2:]
                    if len(tempr) < 16:
                        while len(tempr) < 16:
                            tempr = "0" + tempr
                    result2 = tempr

                else:
                    if secondr[0].isupper() and secondr[-1].isnumeric():
                        tempr = to_bin(firstr[1])
                        result += tempr
                        result += "110000000"
                        result2 = secondr
                    else:
                        if secondr[0].isupper():
                            tempr = to_bin(firstr[1])
                            result += tempr
                            result += "100000000"
                            result2 = secondr
                        else:
                            raise Exception("invalid line")
    
    if len(result) != 16:
        raise Exception("binary word not 16 bits")
    else:
        bin_list.append(result[:8])
        bin_list.append(result[8:16])

        if result2.isnumeric():
            bin_list.append(result2[:8])
            bin_list.append(result2[8:16])

        else:
            if result2 == "":
                pass
            else:
                bin_list.append(result2)
    
                
        


            















def string_line(line):
    got_dot = False
    leng = 0
    ascii_bin = ""
    string_skip = 6

    for letter in line:

        if not got_dot:
            if letter == ".":
                got_dot = True

        else:
            if string_skip > 0:
                string_skip -= 1
                continue

            elif letter == '"' or letter == " ":
                continue

            else:
                leng = len(bin(ord(letter))[2:])
                leng = 8 - leng

                for i in range(leng):
                    ascii_bin += "0"

                ascii_bin += bin(ord(letter))[2:]
                bin_list.append(ascii_bin)
                ascii_bin = ""

    bin_list.append("00000000")












def data_line(line):

    leng = 0
    binnum = ""
    num = ""
    got_dot = False
    global line_counter

    for letter in line:

        if not got_dot:
            if letter == ".":
                got_dot = True

        else:
            if letter.isnumeric():
                num += letter

    if int(num) > 65535:
        raise Exception("number too high!")
    else:
        leng = len(str(bin(int(num)))[2:])
        leng = 16 - leng
        
        for i in range(leng):
            binnum += "0"
        
        binnum += str(bin(int(num)))[2:]
        bin_list.append(binnum[:8])
        bin_list.append(binnum[8:16])


    
            
            








def label_line(line):

    label_name = ""
    got_label = False

    for char in line:

        if not got_label:

            if char.isupper():
                label_name += char
                continue
            elif char == ":":
                got_label = True
                label_dict[label_name] = line_counter
                continue
            else:
                raise Exception("must have : after label")

        if line[len(label_name) + 1 : ].strip() == "":
            raise Exception("invalid line")

        else:

            if char == " ":
                continue
            elif char == ".":
                if line[line.index(".") + 1] == "s":
                    string_line(line)
                    break
                elif line[line.index(".") + 1] == "d":
                    data_line(line)
                    break
                else:
                    raise Exception("invalid line")
            elif char.islower():
                command_line(line[len(label_name) + 1 :])
                break
            else:
                raise Exception("invalid line")

            



            


            
            

def main():

    #c:\junk\test.txt

    global opcode_dict
    opcode_dict = {
        "mov": "0000",
        "cmp": "0001",
        "add": "0010",
        "sub": "0011",
        "not": "0100",
        "cir": "0101",
        "lea": "0110",
        "inc": "0111",
        "dec": "1000",
        "jmp": "1001",
        "jne": "1010",
        "jz": "1011",
        "xor": "1100",
        "or": "1101",
        "rol": "1110",
        "nop": "1111"
    }

    
    global label_dict
    label_dict = {}

    global line_counter
    line_counter = 1

    global bin_list
    bin_list = []

    global bin_list2
    bin_list2 = []

    first_char = ""
    assembly_path = input("enter the input file's path: ")
    try:
        input_file = open(assembly_path, "r")
    except:
        print ("file not found")

    for line in input_file:
        
        if line.strip() == "":
            continue

        line = line.strip()

        first_char = line[0]
        if first_char == "#":
            continue
        elif first_char == ".":
            continue
        elif first_char.isupper():
            label_line(line)
        elif first_char.islower():
            command_line(line)
        else:
            raise Exception("invalid line")

        line_counter += 1

    input_file.close()

    assembly_path2 = input("enter the target file's path: ")
    try:
        output_file = open(assembly_path2, "a")
    except:
        raise Exception("file not found")

    for line in bin_list:
        output_file.write(line)
        output_file.write("\n")
    
    output_file.close()

    output_file = open(assembly_path2, "r")

    for line in output_file:
        bin_list2.append(line)

    output_file.close()

    output_file = open(assembly_path2, "r+")
    output_file.truncate(0)
    output_file.close()
    
    bin_list3 = []
    temp = ""
    tempnum = ""
    operation = ""
    summer = 0

    for line in bin_list2:
        line = line.strip()

        if line.isnumeric():
            bin_list3.append(line)
            continue

        else:
            for letter in line:
                if letter.isupper():
                    temp += letter
                    continue
                elif letter == "+":
                    operation = "+"
                    continue
                elif letter == "-":
                    operation = "-"
                    continue
                elif letter.isnumeric():
                    tempnum += letter

            if operation == "":
                tempnum = str(bin(int(label_dict[temp])))[2:]
            elif operation == "+":
                summer = int(label_dict[temp]) + int(tempnum)
                tempnum = str(bin(summer))[2:]
            elif operation == "-":
                summer = int(label_dict[temp]) - int(tempnum)
                tempnum = str(bin(summer))[2:]

            if len(tempnum) < 16:
                while len(tempnum) < 16:
                    tempnum = "0" + tempnum

            bin_list3.append(tempnum[:8])
            bin_list3.append(tempnum[8:16])
            temp = ""
            tempnum = ""
            operation = ""
            summer = 0

    output_file = open(assembly_path2, "a")
    for line in bin_list3:
        output_file.write(line)
        output_file.write("\n")

    print("voila!")









if __name__ == "__main__":
    main()