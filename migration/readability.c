#include <ctype.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>
#include <wctype.h>
#include <math.h>

int main()
{
    string text = get_string("Text: ");
    string space = " ";


    int letters = 0;
    int words = 1;
    int sentences = 0;
    for (int i = 0, len = strlen(text); i < len; i++) // liczenie literek
    {

        char c = text[i];
        if (isalpha(c))
        {
            letters += 1;
        }
    }


    for (int i = 0, len = strlen(text); i < len; i++) // liczenie słów
    {

        char c = text[i];
        if (text[i] == ' ')
        {
            words += 1;
        }
    }
    

    for (int i = 0, len = strlen(text); i < len; i++) // liczenie zdań
    {

        char c = text[i];
        if (text[i] == '.') //kropka
        {
            sentences += 1;
        }
        else if (text[i] == '?')//znak zapytania
        {
            sentences += 1;
        }
        else if (text[i] == '!')// wykrzyknik
        {
            sentences += 1;
        }
    }

// wzor na index
    float L = (letters / (float) words)  * 100;
    float S = (sentences / (float) words)  * 100;

    float index = 0.0588 * L - 0.296 * S - 15.8;


    if (index > 16) //wypisywanie oceny
    {
        printf("Grade 16+\n");
    }
    else if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else
    {
        printf("Grade %i\n", (int) round(index));
    }
}

