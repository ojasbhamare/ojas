#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for(int j = 0; j < width; j++)
        {
            int r = image[i][j].rgbtRed;
            int g = image[i][j].rgbtGreen;
            int b = image[i][j].rgbtBlue;
            float ans1 = (r + g + b)/3.0;
            int ans = round(ans1);
            image[i][j].rgbtRed = ans;
            image[i][j].rgbtGreen = ans;
            image[i][j].rgbtBlue = ans;

        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    /*  sepiaRed = .393 * originalRed + .769 * originalGreen + .189 * originalBlue
  sepiaGreen = .349 * originalRed + .686 * originalGreen + .168 * originalBlue
  sepiaBlue = .272 * originalRed + .534 * originalGreen + .131 * originalBlue*/


    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int r = image[i][j].rgbtRed;
            int g = image[i][j].rgbtGreen;
            int b = image[i][j].rgbtBlue;

            float ansr = 0.393 * r + .769 * g + .189 * b;
            float ansg = 0.349 * r + .686 * g + .168 * b;
            float ansb = 0.272 * r + .534 * g + .131 * b;

            if (ansr > 255)
            {
                ansr = 255;
            }
            if (ansg > 255)
            {
                ansg = 255;
            }
            if (ansb > 255)
            {
                ansb = 255;
            }

            image[i][j].rgbtRed = round(ansr);
            image[i][j].rgbtGreen = round(ansg);
            image[i][j].rgbtBlue = round(ansb);

        }
    }


    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE ans[height][width];

    for (int i = 0; i < height; i++)
    {
        for(int j = 0; j < width; j++)
        {
            ans[i][j] = image[i][j];
        }
    }

    for (int i = 0; i < height; i++)
    {
        for(int j = 0; j < width; j++)
        {
            int b = width - j - 1;
            image[i][j] = ans[i][b];
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE ans[height][width];

    for (int i = 0; i < height; i++)
    {
        for(int j = 0; j < width; j++)
        {
            ans[i][j] = image[i][j];
        }
    }

    for (int i = 0; i < height; i++)
    {
        for(int j = 0; j < width; j++)
        {
            float sumr = 0, sumg = 0, sumb = 0, count = 0;
            for (int h = i - 1; h <= h+1; h++)
            {
                for(int k = j - 1; k <= k+1; k++)
                {
                    if (h > 0 && k > 0 && h < height && k < width)
                    {
                        sumr += ans[h][k].rgbtRed;
                        sumg += ans[h][k].rgbtGreen;
                        sumb += ans[h][k].rgbtBlue;
                        count += 1;
                    }
                }
            }
            int ansr = round(sumr / count);
            int ansg = round(sumg / count);
            int ansb = round(sumb / count);

            image[i][j].rgbtRed = ansr;
            image[i][j].rgbtGreen = ansg;
            image[i][j].rgbtBlue = ansb;

        }
    }


    return;
}
