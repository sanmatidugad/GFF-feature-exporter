#! /usr/bin/ python3
import argparse

parser = argparse.ArgumentParser(description="This tool finds the required fasta sequnce from gff files")    #Create an ArgumentParser object
parser.add_argument("--source", help="Path to the input file")    # Add a command-line argument for the input file
parser.add_argument("--type", help="Type to filter. Any of the features present in the third column")    # Add a command-line argument for the type
parser.add_argument("--attribute", help="Attribute name. Tags such as ID, Name, Parent, Name, dbxref, etc. ")    # Add command-line arguments for attribute
parser.add_argument("--value", help="Attribute value. Tag-Value duch as YAL069W, ARS103, etc ")   # Add command-line arguments for value

args = parser.parse_args()    # Parse the command-line arguments
input_file_path = args.source    # Access the input file path from the parsed arguments

# input_file_path = 'Saccharomyces_cerevisiae_S288C.annotation.gff'
# file_type = 'gene'
# attribute = 'Name'
# value = 'YAL068W'


data_dict = {}    # Initialize  an empty dictionary to store table in the form of dictionary of lists
fasta_dict = {}    # Initialize an empty dictionary to store the FASTA data

start_coordinate = ''    #store start coordinates of the gene
end_coordinate = ''   # store end coordinates of the gene
chromosome = ''    #store the chromosome on which the gene resides

collect_lines = False    # Flag to indicate when to collect lines for FASTA data.
current_key = None    # Initialize variables to store the current key and value
current_value = ""

try:
    with open(input_file_path, 'r') as file:
        for line in file:
            line = line.strip()  # Remove leading/trailing whitespace

            if collect_lines:
                if line.startswith(">"):
                    # If a new key is encountered, save the previous key and its value in the FASTA dictionary
                    if current_key is not None:
                        fasta_dict[current_key] = current_value
                    # Set the new key
                    current_key = line[1:]
                    current_value = ""
                else:
                    current_value += line

            # Check if the line starts with "chr"
            if line.startswith("chr") or line[0].isdigit():
                # Split the line into columns using tab as the delimiter
                columns = line.strip().split('\t')

                # Iterate through the columns and add them to the corresponding list in the dictionary
                for i, column in enumerate(columns):
                    if i not in data_dict:
                        data_dict[i] = []
                    data_dict[i].append(column)

            elif line == "##FASTA":
                collect_lines = True    # Start collecting lines after encountering "##FASTA"

        #Check for the specified type, attribute, and value in the third column
        if args.type and args.attribute and args.value:
            attribute_value = args.attribute + "=" + args.value
            #print(attribute_value)
            third_column_values = data_dict[2]    #Access the third column values

            matching_indices = []    # for all gene lines
            matching_values = []    # for exact location of attribute_value

            for i, each in enumerate(third_column_values):
                #print(i, value)
                if each in args.type:    #finding all lines with the required type
                    matching_indices.append(i)
            for i , each in enumerate(data_dict[8]):    #finding the required attribute_value in the the 9th column
                if attribute_value in each:
                    matching_values.append(i)    #getting index of this value
            #print("Index of the matching value from the 9th column" , matching_values)

            for i in matching_values:
                if i in matching_indices:
                    print("Unique")
                    start_coordinate += (data_dict[3][i])
                    end_coordinate += (data_dict[4][i])
                    chromosome += data_dict[0][i]

            for i in matching_values:
                if i in matching_indices and data_dict[6][i] == '+':
                    print("\nSequence is present on Positive Strand")
                elif i in matching_indices and data_dict[6][i] == '-':
                    print("\nSequence is Present on Negative Strand")
                elif i in matching_indices and data_dict[6][i] == '.':
                    print("\nSequence strand undetermined")

    # Add the last key and its value to the FASTA dictionary
    if current_key is not None:
        fasta_dict[current_key] = current_value

    # print(start_coordinate)
    # print(end_coordinate)
    # print(chromosome)

    line_length = 60
    gene_sequence = fasta_dict[chromosome][int(start_coordinate)-1: int(end_coordinate)-1]
    lines = [gene_sequence[i:i+line_length] for i in range(0, len(gene_sequence), line_length)]
    formatted_text = "\n".join(lines)    # Join the lines with line breaks and print

    print(">" + args.type + ":" + args.attribute + ":" + args.value)
    print(formatted_text)

except FileNotFoundError:
    print(f"File not found: {input_file_path}")
except KeyError:
    print(f"Provided feature type, attribute or tag-value may not be present in the file: {args.type}, {args.attribute}, {args.value}")
