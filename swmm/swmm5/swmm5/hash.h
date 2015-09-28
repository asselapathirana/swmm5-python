<<<<<<< HEAD
//-----------------------------------------------------------------------------
//   hash.h
//
//   Header file for Hash Table module hash.c.
//-----------------------------------------------------------------------------

#define HTMAXSIZE 1999
#define NOTFOUND  -1

struct HTentry
{
    char   *key;
    int    data;
    struct HTentry *next;
};

typedef struct HTentry *HTtable;

HTtable *HTcreate(void);
int     HTinsert(HTtable *, char *, int);
int     HTfind(HTtable *, char *);
char    *HTfindKey(HTtable *, char *);
void    HTfree(HTtable *);
=======
//-----------------------------------------------------------------------------
//   hash.h
//
//   Header file for Hash Table module hash.c.
//-----------------------------------------------------------------------------

#define HTMAXSIZE 1999
#define NOTFOUND  -1

struct HTentry
{
    char   *key;
    int    data;
    struct HTentry *next;
};

typedef struct HTentry *HTtable;

HTtable *HTcreate(void);
int     HTinsert(HTtable *, char *, int);
int     HTfind(HTtable *, char *);
char    *HTfindKey(HTtable *, char *);
void    HTfree(HTtable *);
>>>>>>> 69bcb3e905257c4a370e55f483acbc4df825991b
