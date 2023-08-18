import csv
import sys


def main():

    # TODO: Check for command-line usage
    if len(sys.argv) != 3:
        sys.exit("Usage: python dna.py database sequence")

    # TODO: Read database file into a variable
    FileName = sys.argv[1]
    file = open(FileName, "r")
    reader = csv.DictReader(file)
    all_sequences = reader.fieldnames[1:]  # reading headers
    strs_count = {}

    # TODO: Read DNA sequence file into a variable
    SequenceFileName = sys.argv[2]
    with open(SequenceFileName, "r") as DNAfile:  # opening dna sequence
        DNAdata = DNAfile.readline()

    # TODO: Find longest match of each STR in DNA sequence
    for str in all_sequences:
        strs_count[str] = longest_match(DNAdata, str)


    # TODO: Check database for matching profiles
    for row in reader:
        passed = 0
        person = row  # assigning a row to a person and checking
        for str in all_sequences:
            if int(person[str]) == int(strs_count[str]):  # if str == str increment the value of passed
                passed += 1
                if passed == len(all_sequences):  # if passed equals the value of all sequences then it should be this person
                    print(person["name"])
                    sys.exit(0)

    file.close()  # closing a file, because opening with with aint working

    print("No match")


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
