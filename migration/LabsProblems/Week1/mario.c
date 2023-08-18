#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // Height = n
    int n;
    do
    {
        n = get_int("Height: ");
    }
    while (n > 8  || n < 1);
    
     for (int i = 0; i < n; i++) // zjadz linii
    {
        for (int j = 0; j < n; j++)  //rysowanie poziome
        {
            if (i + j < n - 1)
            {
                printf(" ");
            }
            else
            {
                printf("#");
            }
        }
        printf("\n");
    }
    
}