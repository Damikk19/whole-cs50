#include <ctype.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>
#include <wctype.h>


int main(int argc, string argv[])
{
    // check that program was run with one command-line argument
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

    // iterate over argument to make sure that all char are digits
    for (int i = 0, len = strlen(argv[1]); i < len; i++)
    {
        if (isdigit(argv[1][i]))
        {
            printf("passed\n");
        }
        else
        {
            printf("Usage: ./caesar key\n");
            return 1;
        }

    }

    // convert that command-line argument from str to int
    int number = atoi(argv[1]);
    printf("number: %i\n", number);




    // prompt user for plain text
    string plaintext = get_string("plaintext: ");


    // iterate over each character of the plaintext
    printf("ciphertext: ");
    for (int i = 0, len = strlen(plaintext); i < len; i++)
    {
        char c = plaintext[i]; // making a char c from i'th letter of plaintext
        if (isalpha(c))
        {
            if (islower(c)) // checking if is lower
            {
                char a = 'a';
                printf("%c", (((c - a) + number) % 26) + a);
            }
            else if (isupper(c)) // checking if is upper
            {
                char a = 'A';
                printf("%c", (((c - a) + number) % 26) + a);
            }
        }
        else //printing char as normal if not alphabetical
        {
            printf("%c", c);
        }

    }
    printf("\n");



}


