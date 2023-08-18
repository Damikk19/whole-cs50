import cs50

text = cs50.get_string("Text: ")

letters = 0
words = 1
sentences = 0

for i in range(len(text)):  # pętla for
    c = text[i]
    if c.isalpha():  # jesli litera w alfabecie to letters +1
        letters += 1


for i in range(len(text)):
    c = text[i]
    if c == " ":
        words += 1


for i in range(len(text)):  # warunki
    c = text[i]
    if c == ".":
        sentences += 1
    elif c == "?":
        sentences += 1
    elif c == "!":
        sentences += 1

L = (float(letters / words) * 100)
S = float((sentences / words) * 100)

index = float(0.0588 * L - 0.296 * S - 15.8)


if index > 16:  # wypisywanie oceny
    print("Grade 16+")
elif index < 1:  # wypisywanie oceny
    print("Before Grade 1")
else:  # wypisywanie oceny
    print(f"Grade {round(index)}")
