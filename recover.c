#include <stdio.h>
#include <stdlib.h>
#include <cs50.h>
#include <stdint.h>


typedef uint8_t BYTE;

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
        BYTE buffer[512];
        fread(buffer, sizeof(BYTE), 512, file);
        /*if (fread(buffer, 1, 512, file) < 512)
        {
            fwrite(img, 1, 512, buffer);
            break;
        }*/

        int num = 0;
        string name = "dcmoskcodcfdsvsdkc";

        FILE *img = NULL;

        bool first = true;
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            if (first)
            {
                sprintf(name, "%03i.jpg", num);
                img = fopen(name, "w");

                fwrite(buffer, sizeof(BYTE), 512, img);
                first = false;
            }

            else
            {
                fclose(img);
                num += 1;
                sprintf(name, "%03i.jpg", num);
                img = fopen(name, "w");

                fwrite(buffer,sizeof(BYTE), 512, img);
            }
        }
        else
        {
            fwrite(buffer,sizeof(BYTE), 512, img);
        }

    }
}
