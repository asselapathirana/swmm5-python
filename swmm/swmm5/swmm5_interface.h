// swmm5_iface.h
//
// Header file for SWMM 5 interfacing functions
//
// #include this file in any C module that references the functions
// contained in swmm5_iface.c.
//
extern int    SWMM_Nperiods;           // number of reporting periods
extern int    SWMM_FlowUnits;          // flow units code
extern int    SWMM_Nsubcatch;          // number of subcatchments
extern int    SWMM_Nnodes;             // number of drainage system nodes
extern int    SWMM_Nlinks;             // number of drainage system links
extern int    SWMM_Npolluts;           // number of pollutants tracked
extern double SWMM_StartDate;          // start date of simulation
extern int    SWMM_ReportStep;         // reporting time step (seconds)
extern int    SWMM_Offset2IDS;                 // version
extern int    SWMM5_VERSION;

int    RunSwmmDll(char* inpFile, char* rptFile, char* outFile);
int    OpenSwmmOutFile(char* outFile);
int    GetSwmmResult(int iType, int iIndex, int vIndex, int period, float* value);
void   CloseSwmmOutFile(void);
void   GetIDName(char* value);
void InitGetIDName();
int GetInt();

extern  int SubcatchVars;               // number of subcatch reporting variables
extern  int NodeVars;                   // number of node reporting variables
extern  int LinkVars;                   // number of link reporting variables
extern  int SysVars;                    // number of system reporting variables

