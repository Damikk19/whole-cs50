#include "helpers.h"
#include <stdio.h>
#include <math.h>

typedef uint8_t BYTE;


// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width]) // filtr grayscale
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int average = round((image[i][j].rgbtRed + image[i][j].rgbtGreen + image[i][j].rgbtBlue) / 3.0);
            image[i][j].rgbtRed = average;
            image[i][j].rgbtGreen = average;
            image[i][j].rgbtBlue = average;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width]) // filtr sepia
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++) //filtr sepia
        {
            int sepiaRed = round(0.393 * image[i][j].rgbtRed + 0.769 * image[i][j].rgbtGreen + 0.189 * image[i][j].rgbtBlue);
            if (sepiaRed > 255)
            {
                sepiaRed = 255;
            }
            int sepiaGreen = round(0.349 * image[i][j].rgbtRed + 0.686 * image[i][j].rgbtGreen + 0.168 * image[i][j].rgbtBlue);
            if (sepiaGreen > 255)
            {
                sepiaGreen = 255;
            }
            int sepiaBlue = round(0.272 * image[i][j].rgbtRed + 0.534 * image[i][j].rgbtGreen + 0.131 * image[i][j].rgbtBlue);
            if (sepiaBlue > 255)
            {
                sepiaBlue = 255;
            }
            image[i][j].rgbtRed = sepiaRed; //ustalamy kadzy pixel z filtrem sepia
            image[i][j].rgbtGreen = sepiaGreen;
            image[i][j].rgbtBlue = sepiaBlue;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width]) // filtr reflect
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width / 2; j++) //dla kazdego pixela bierzemy jego odpowiednik z drugiej strony
        {
            int tmpRed = image[i][j].rgbtRed;
            image[i][j].rgbtRed = image[i][width - 1 - j].rgbtRed;
            image[i][width - 1 - j].rgbtRed = tmpRed;

            int tmpGreen = image[i][j].rgbtGreen;
            image[i][j].rgbtGreen = image[i][width - 1 - j].rgbtGreen;
            image[i][width - 1 - j].rgbtGreen = tmpGreen;

            int tmpBlue = image[i][j].rgbtBlue;
            image[i][j].rgbtBlue = image[i][width - 1 - j].rgbtBlue;
            image[i][width - 1 - j].rgbtBlue = tmpBlue;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width]) //filtr blur
{
    RGBTRIPLE copy[height][width]; // copy to array, kopia image

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int RedSum = 0;
            int GreenSum = 0;
            int BlueSum = 0;
            float pixel_number = 0;

            for (int h = -1; h < 2; h++)
            {
                for (int w = -1; w < 2; w++)
                {
                    if (i + h < 0 || i + h > height - 1 || j + w < 0 || j + w > width - 1) // warunek, aby nie wyjść z pixeli obrazka
                    {
                        continue;
                    }
                    else
                    {
                        RedSum += image[i + h][j + w].rgbtRed;
                        GreenSum += image[i + h][j + w].rgbtGreen;
                        BlueSum += image[i + h][j + w].rgbtBlue;

                        pixel_number++;
                    }
                }
            }
            copy[i][j].rgbtRed = round(RedSum / pixel_number);
            copy[i][j].rgbtGreen = round(GreenSum / pixel_number);
            copy[i][j].rgbtBlue = round(BlueSum / pixel_number);
        }
    }


    for (int i = 0; i < height; i++) // zmieniamy image na copy które ma już box blura
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j].rgbtRed = copy[i][j].rgbtRed;
            image[i][j].rgbtGreen = copy[i][j].rgbtGreen;
            image[i][j].rgbtBlue = copy[i][j].rgbtBlue;
        }
    }
    return;
}