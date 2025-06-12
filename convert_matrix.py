from utils import generate_labels, save_to_file




if __name__ == "__main__":
    input_file_name = input("Enter the input file name: ")
    lines = []
    with open(input_file_name, 'r') as file:
        for line in file:
            lines.append(line.strip().split())
    n = len(lines)
    labels = generate_labels(n)

    output_file_name = input("Enter the output file name: ")
    with open(output_file_name, 'w') as file:
        for i in range(n):
            for j in range(n):
                file.write(f"{labels[i]} {labels[j]} {lines[i][j]}\n")
