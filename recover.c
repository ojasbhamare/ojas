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
    int num = 0;
    char name[8];
    FILE *img = NULL;
    bool first = true;
    while (true)
    {
        BYTE buffer[512];
        if (fread(buffer, sizeof(BYTE), 512, file) < 512)
        {
            fwrite(buffer, sizeof(BYTE), 512,img);
            break;
        }
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
            if (img == NULL)
            {
                continue;
            }

            fwrite(buffer,sizeof(BYTE), 512, img);
        }

    }
}
