#include <stdio.h>
#include <cs50.h>
#include <string.h>

typedef struct
{
    string name;
    int votes;
}
candidate;

bool vote(string name, int n, candidate *candidates);
int print_winner(candidate *cads, int n);

int main(int argc ,char *argv[])
{
    int n = argc - 1;
    candidate candidates[n];

    for(int i = 0; i < n ; i++)
    {
        candidates[i].name = argv[i+1];
        candidates[i].votes = 0;
    }

    int nos = get_int("Number of voters: ");
    for(int i = 0; i < nos; i++)
    {
        string name = get_string("Vote: ");
        vote(name, n, candidates);
    }
    print_winner(candidates, n);
}


bool vote(string name, int n, candidate *candidates)
    {
        for (int i = 0; i < n ; i++)
        {
            if (strcmp(candidates[i].name, name) == 0)
            {
                candidates[i].votes += 1;
                return 0;
            }
        }
        printf("Invalid vote.\n");
        return 1;
    }

int print_winner(candidate *candidates, int n)
{
    candidate winner = candidates[0];
    for (int i = 1; i < n ; i++)
    {
        if (candidates[i].votes > winner.votes)
        {
            winner = candidates[i];
        }
    }
    for (int i = 0; i < n ; i++)
    {
        if (candidates[i].votes == winner.votes)
        {
            printf("%s\n",candidates[i].name);
        }
    }
    return 0;
}