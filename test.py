def main(file):
    with open(file) as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        new_lines.append(line.strip().split())

    data = []
    group = []

    index = 0
    while index < len(new_lines)-2:
        line_0 = new_lines[index]
        line_1 = new_lines[index+1]
        line_2 = new_lines[index+2]

        if line_0[0].lower() == 'input' and line_0[0].lower() == 'temp' and line_0[0].lower() == 'input' and


main('')
