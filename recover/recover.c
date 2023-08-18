#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

typedef uint8_t BYTE;
#define BLOCKSIZE 512


int main(int argc, char *argv[])
{
    if (argc != 2) // telling user of a good usage
    {
        printf("Usage: ./recover one-argument\n");
        return 1;
    }

    //open a file
    FILE *input_fileptr = fopen(argv[1], "r");
    if (input_fileptr == NULL)
    {
        return 1;
    }
    // making a filename of 8 chars, assigning a outfile poitner
    char filename[8];
    FILE *outfile = NULL;
    int JpegCounter = 0;
    BYTE buffer[BLOCKSIZE];

    while (fread(buffer, 1, BLOCKSIZE, input_fileptr) == BLOCKSIZE) //reading 512 bytes into a buffer
    {
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && ((buffer[3] & 0xf0) == 0xe0)) // looking for start of a jpeg
        {
            if (outfile != NULL)
            {
                fclose(outfile);
            }
            sprintf(filename, "%03i.jpg", JpegCounter);
            outfile = fopen(filename, "w");
            JpegCounter++;
        }
        if (outfile != NULL)
        {
            fwrite(buffer, 1, BLOCKSIZE, outfile);
        }
    }

    if (input_fileptr != NULL) //closing any existing files
    {
        fclose(input_fileptr);
    }

    if (outfile != NULL)
    {
        fclose(outfile);
    }

}
