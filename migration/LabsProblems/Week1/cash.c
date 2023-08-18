#include <cs50.h>
#include <stdio.h>
#include <math.h>

int main(void)
{
    float dollar;
    do
    {
        dollar = get_float("Enter your Change: ");
    }
    while (dollar < 0);
    int cents = round(dollar * 100);
    int coins = 0;

    while (cents >= 25) //looking for 25 cents
    {
        cents -= 25;
        coins++;
    }

    while (cents >= 10) //looking for 10 cents
    {
        cents -= 10;
        coins++;
    }

    while (cents >= 5) //looking for 5 cents
    {
        cents -= 5;
        coins++;
    }

    while (cents >= 1) //looking for 1 cent1
    {
        cents -= 1;
        coins++;
    }

    printf("You'll need at least: %i coins", coins);
}