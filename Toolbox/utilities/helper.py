


def add_comma(value):
    res = ""
    if value != "":
        try:
            try_split = str(value).split(".")

            if len(try_split[1]) == 1 and try_split[1] == "0":
                res = ('{:,}'.format(int(f"{try_split[0]}")))
            else:
                res = ('{:,}'.format(float(value)))
        
        except IndexError:
            res = ('{:,}'.format(int(value)))

        except ValueError:
            return res
    else:
        return res

    return str(res)


def mod_round(value):
    mod = ""
    prev_round = round(value,2) #4.56

    splitter = str(prev_round).split(".")

    if len(splitter[1]) == 2: #4.56
        mod = f"{splitter[0]}{splitter[1][0]}{splitter[1][1]}0" #4_560
    if len(splitter[1]) == 1: #4.5
        mod = f"{splitter[0]}{splitter[1][0]}00" #4_500

    return int(mod)
       

def deal_with_decimal(value, float_values = 1000):
    total = 0

    try:
        act_val = str(value).split(".")

        if len(act_val[1]) >= 3:
            if int(act_val[1][2])==9:
                init_val = float(f"{act_val[0]}.{act_val[1][0]}{act_val[1][1]}{int(act_val[1][2])}")

            elif int(act_val[1][2])>=5:
                init_val = float(f"{act_val[0]}.{act_val[1][0]}{act_val[1][1]}{int(act_val[1][2])+1}")
               
            elif int(act_val[1][2])<5:
                init_val = float(f"{act_val[0]}.{act_val[1][0]}{act_val[1][1]}{act_val[1][2]}")

            total = mod_round(init_val)

        elif len(act_val[1]) < 3:
            total = int(float((f"{act_val[0]}.{act_val[1]}"))*float_values)

    except Exception as e:
        total = int(value*float_values)
    
    return total