import os, subprocess

input_file  = "xfoil_input.txt"
tmp_file    = "airfoil.tmp"
xfoil_input = """load
{airfoil}
pane
ppar

oper
v {Re}
m {Ma}
iter 200
pacc
{tmp_file}

aseq
{start_alpha}
{end_alpha}
.5

quit
"""

def read_values(filename):
    column_names = []
    data = {}
    with open(filename, 'r') as input:
        in_header = True
        for line in input:
            columns = line.split()
            if in_header:
                print("1")
                if len(columns) and '---' in columns[0]:
                    print("2")
                    in_header = False
                if len(columns) and columns[0] == 'alpha':
                    print("3")
                    column_names = columns
            else:
                print("4")
                columns = [float(column) for column in columns]
                data[columns[0]] = dict(zip(column_names, columns))
    return data



def run_airfoil(airfoil, Re, Ma, start_alpha = -1.0, end_alpha = 20):
    if os.path.exists(tmp_file):
        os.remove(tmp_file)
    if os.path.exists(input_file):
        os.remove(input_file)
    input = xfoil_input.format(airfoil=airfoil,
                               Re=Re, Ma=Ma, 
                               tmp_file=tmp_file,
                               start_alpha=start_alpha,
                               end_alpha=end_alpha)
    with open(input_file, 'w') as file:
        file.write(input)
    os.system("xfoil < " + input_file)
    return read_values(tmp_file)

