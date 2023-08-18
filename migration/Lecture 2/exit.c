#include <stdio.h>
#include <cs50.h>
#include <string.h>

int main(int argc, string argv[0])
{
    if (argc != 2)
    {
        printf("missing command-line argument\n");
        return 1;
    }
    printf("hello, %s\n", argv[1]);
    return 0;
}