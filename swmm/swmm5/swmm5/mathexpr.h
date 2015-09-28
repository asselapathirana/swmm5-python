<<<<<<< HEAD
/******************************************************************************
**  MODULE:        MATHEXPR.H
**  PROJECT:       SWMM 5.1
**  DESCRIPTION:   header file for the math expression parser in mathexpr.c.
**  AUTHORS:       L. Rossman, US EPA - NRMRL
**                 F. Shang, University of Cincinnati
**  VERSION:       5.1.001
**  LAST UPDATE:   03/20/14
******************************************************************************/

//  Node in a tokenized math expression list
struct ExprNode
{
    int    opcode;                // operator code
    int    ivar;                  // variable index
    double fvalue;                // numerical value
	struct ExprNode *prev;        // previous node
    struct ExprNode *next;        // next node
};
typedef struct ExprNode MathExpr;

//  Creates a tokenized math expression from a string
MathExpr* mathexpr_create(char* s, int (*getVar) (char *));

//  Evaluates a tokenized math expression
double mathexpr_eval(MathExpr* expr, double (*getVal) (int));

//  Deletes a tokenized math expression
void  mathexpr_delete(MathExpr* expr);
=======
/******************************************************************************
**  MODULE:        MATHEXPR.H
**  PROJECT:       SWMM 5.0
**  DESCRIPTION:   header file for the math expression parser in mathexpr.c.
**  AUTHORS:       L. Rossman, US EPA - NRMRL
**                 F. Shang, University of Cincinnati
**  VERSION:       5.0.010
**  LAST UPDATE:   3/1/07
******************************************************************************/

//  Node in a tokenized math expression list
struct ExprNode
{
    int    opcode;                // operator code
    int    ivar;                  // variable index
    double fvalue;                // numerical value
	struct ExprNode *prev;        // previous node
    struct ExprNode *next;        // next node
};
typedef struct ExprNode MathExpr;

//  Creates a tokenized math expression from a string
MathExpr* mathexpr_create(char* s, int (*getVar) (char *));

//  Evaluates a tokenized math expression
double mathexpr_eval(MathExpr* expr, double (*getVal) (int));

//  Deletes a tokenized math expression
void  mathexpr_delete(MathExpr* expr);
>>>>>>> 69bcb3e905257c4a370e55f483acbc4df825991b
