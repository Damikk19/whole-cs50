// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <cs50.h>
#include <strings.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 26;

int word_count = 0;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // TODO
    int check_index = hash(word);

    node *cursor = table[check_index];

    while (cursor != NULL)
    {
        if (strcasecmp(cursor->word, word) == 0)
        {
            return true;
        }
        cursor = cursor->next;
    }
    return false;

}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO: Improve this hash function
    int hash_value = 0;

    for (int i = 0; word[i] != '\0'; i++)
    {
        hash_value += tolower(word[i]);
    }

    return (hash_value % N);
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // TODO
    FILE *file = fopen(dictionary, "r"); //opening a file
    if (file == NULL)
    {
        return false;
    }

    for (int i = 0; i < N; i++)
    {
        table[i] = NULL;
    }

    char tempWord[LENGTH + 1]; //assigning a word string

    while (fscanf(file, "%s\n", tempWord) != EOF) //scanning until the end of the file
    {

        node *n = malloc(sizeof(node)); //mallocing a node size of node

        strcpy(n->word, tempWord); //copying a string from string word to word in node

        int bucket = hash(n->word); // hshing a bucket for a word

        if (table[bucket] == NULL) // if there is nothing then do this
        {
            n->next = NULL;
            table[bucket] = n;
        }
        else // if there is something then point at first thing in bucket
        {
            n->next = table[bucket];
            table[bucket] = n;
        }
        word_count++;
    }
    fclose(file); //closing a file
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    return word_count; //returning a wordcount that we are incrementing in load
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // TODO
    for (int i = 0; i < N; i++)
    {
        node *tempNode = table[i];

        while (tempNode != NULL)
        {
            node *deletingtempNode = tempNode;
            tempNode = tempNode->next;
            free(deletingtempNode);
        }

        table[i] = NULL;
    }
    return true;
}
