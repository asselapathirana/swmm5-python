<<<<<<< HEAD
//-----------------------------------------------------------------------------
//  mempool.h
//
//  Header for mempool.c
//
//  The type alloc_handle_t provides an opaque reference to the
//  alloc pool - only the alloc routines know its structure.
//-----------------------------------------------------------------------------

typedef struct
{
   long  dummy;
}  alloc_handle_t;

alloc_handle_t *AllocInit(void);
char           *Alloc(long);
alloc_handle_t *AllocSetPool(alloc_handle_t *);
void            AllocReset(void);
void            AllocFreePool(void);
=======
//-----------------------------------------------------------------------------
//  mempool.h
//
//  Header for mempool.c
//
//  The type alloc_handle_t provides an opaque reference to the
//  alloc pool - only the alloc routines know its structure.
//-----------------------------------------------------------------------------

typedef struct
{
   long  dummy;
}  alloc_handle_t;

alloc_handle_t *AllocInit(void);
char           *Alloc(long);
alloc_handle_t *AllocSetPool(alloc_handle_t *);
void            AllocReset(void);
void            AllocFreePool(void);
>>>>>>> 69bcb3e905257c4a370e55f483acbc4df825991b
