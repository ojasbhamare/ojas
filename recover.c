#include <stdio.h>
#include <stdlib.h>
#include <cs50.h>

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./recover image\n");
        return 1;
    }

    FILE *file = fopen(argv[1], "r");

    if (!file)
    {
        printf("Cannot open the file.\n");
        return 1;
    }


    for (int i = 0;true ; i++)
    {
        char full[512];
        fread(full,1, 512, file);
        /*if (fread(full, 1, 512, file) < 512)
        {
            fwrite(img, 1, 512, full);
            break;
        }*/

        int num = 0;
        string name = "dcmoskcodcfdsvsdkc";

        FILE *img = NULL;

        bool first = true;
        if (full[0] == (char) 0xff && full[1] == (char) 0xd8 && full[2] == (char)0xff && (full[3] & 0xf0) == 0xe0)
        {
            if (first)
            {
                sprintf(name, "%03i.jpg", num);
                img = fopen(name, "w");

                fwrite(full, 1, 512, img);
                first = false;
            }

            else
            {

                fclose(img);
                num += 1;
                sprintf(name, "%03i.jpg", num);
                img = fopen(name, "w");

                fwrite(full,1, 512, img);
            }
        }
        else
        {
            fwrite(full,1, 512, img);
        }

    }
}
