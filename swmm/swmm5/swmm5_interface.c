// swmm5_iface.c
//
// Example code for interfacing SWMM 5 with C/C++ programs.
//
// Remember to #include the file swmm5_iface.h in the calling program.

#include <stdio.h>
//#include <windows.h>
#include "./swmm5/swmm5.h"

int    SWMM_Nperiods;                  // number of reporting periods
int    SWMM_FlowUnits;                 // flow units code
int    SWMM_Nsubcatch;                 // number of subcatchments
int    SWMM_Nnodes;                    // number of drainage system nodes
int    SWMM_Nlinks;                    // number of drainage system links
int    SWMM_Npolluts;                  // number of pollutants tracked
double SWMM_StartDate;                 // start date of simulation
int    SWMM_ReportStep;                // reporting time step (seconds)
int    SWMM_Offset2IDS;                 // where the ID section start.
int    SWMM5_VERSION;                    //version integer.

//int    RunSwmmExe(char* cmdLine);
int    RunSwmmDll(char* inpFile, char* rptFile, char* outFile);
int    OpenSwmmOutFile(char* outFile);
int    GetSwmmResult(int iType, int iIndex, int vIndex, int period, float* value);
void   CloseSwmmOutFile(void);
int    countids;

static const int SUBCATCH = 0;
static const int NODE     = 1;
static const int LINK     = 2;
static const int SYS      = 3;

int SubcatchVars;               // number of subcatch reporting variables
int NodeVars;                   // number of node reporting variables
int LinkVars;                   // number of link reporting variables
int SysVars;                    // number of system reporting variables

static const int RECORDSIZE = 4;       // number of bytes per file record



static FILE*  Fout;                    // file handle
static int    StartPos;                // file position where results start
static int    BytesPerPeriod;          // bytes used for results in each period
static void   ProcessMessages(void);

/*
//-----------------------------------------------------------------------------
int RunSwmmExe(char* cmdLine)
//-----------------------------------------------------------------------------
{
  int exitCode;
  STARTUPINFO si;
  PROCESS_INFORMATION  pi;

  // --- initialize data structures
  memset(&si, 0, sizeof(si));
  memset(&pi, 0, sizeof(pi));
  si.cb = sizeof(si);
  si.wShowWindow = SW_SHOWNORMAL;

  // --- launch swmm5.exe
  exitCode = CreateProcess(NULL, cmdLine, NULL, NULL, 0,
			 0, NULL, NULL, &si, &pi);

  // --- wait for program to end
  exitCode = WaitForSingleObject(pi.hProcess, INFINITE);

  // --- retrieve the error code produced by the program
  GetExitCodeProcess(pi.hProcess, &exitCode);

  // --- release handles
  CloseHandle(pi.hProcess);
  CloseHandle(pi.hThread);
  return exitCode;
}

*/
//-----------------------------------------------------------------------------
int RunSwmmDll(char* inpFile, char* rptFile, char* outFile)
//-----------------------------------------------------------------------------
{
  int err;
  double elapsedTime;

  // --- open a SWMM project
  err = swmm_open(inpFile, rptFile, outFile);
  if (!err)
  {
    // --- initialize all processing systems
    err = swmm_start(1);
    if (err == 0)
    {
      // --- step through the simulation
      do
      {
        // --- allow Windows to process any pending events
        ProcessMessages();

        // --- extend the simulation by one routing time step
        err = swmm_step(&elapsedTime);

        /////////////////////////////////////////////
        // --- call progress reporting function here,
        //     using elapsedTime as an argument
        /////////////////////////////////////////////

      } while (elapsedTime > 0.0 && err == 0);

      // --- close all processing systems
      swmm_end();
    }
  }

  // --- close the project
  swmm_close();
  return err;
}


//-----------------------------------------------------------------------------
void ProcessMessages(void)
//-----------------------------------------------------------------------------
{

/****  Only use this function with a Win32 application *****
  MSG msg;
  while (TRUE)
  {
    if (PeekMessage(&msg, NULL, 0, 0, PM_REMOVE))
    {
      if (msg.message == WM_QUIT) break;
      else
      {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
      }
    }
    else break;
  }
***********************************************************/

}



//-----------------------------------------------------------------------------
int OpenSwmmOutFile(char* outFile)
//-----------------------------------------------------------------------------
{
  int magic1, magic2, errCode, offset, offset0, version;
  int err;
  // if the file is already open, do not open it!

  // --- open the output file
  Fout = fopen(outFile, "rb");
  if (Fout == NULL) return 2;

  // --- check that file contains at least 14 records
  fseek(Fout, 0L, SEEK_END);
  if (ftell(Fout) < 14*RECORDSIZE)
  {
    fclose(Fout);
    return 1;
  }

  // --- read parameters from end of file
  fseek(Fout, -6*RECORDSIZE, SEEK_END);
  fread(&SWMM_Offset2IDS, RECORDSIZE, 1, Fout);
  fread(&offset0, RECORDSIZE, 1, Fout);
  fread(&StartPos, RECORDSIZE, 1, Fout);
  fread(&SWMM_Nperiods, RECORDSIZE, 1, Fout);
  fread(&errCode, RECORDSIZE, 1, Fout);
  fread(&magic2, RECORDSIZE, 1, Fout);

  // --- read magic number from beginning of file
  fseek(Fout, 0L, SEEK_SET);
  fread(&magic1, RECORDSIZE, 1, Fout);

  // --- perform error checks
  if (magic1 != magic2) err = 1;
  else if (errCode != 0) err = 1;
  else if (SWMM_Nperiods == 0) err = 1;
  else err = 0;

  // --- quit if errors found
  if (err > 0 )
  {
    fclose(Fout);
    Fout = NULL;
    return err;
  }

  // --- otherwise read additional parameters from start of file
  fread(&version, RECORDSIZE, 1, Fout);
  SWMM5_VERSION=version;
  fread(&SWMM_FlowUnits, RECORDSIZE, 1, Fout);
  fread(&SWMM_Nsubcatch, RECORDSIZE, 1, Fout);
  fread(&SWMM_Nnodes, RECORDSIZE, 1, Fout);
  fread(&SWMM_Nlinks, RECORDSIZE, 1, Fout);
  fread(&SWMM_Npolluts, RECORDSIZE, 1, Fout);

  // Skip over saved subcatch/node/link input values
  offset = (SWMM_Nsubcatch+2) * RECORDSIZE  // Subcatchment area
             + (3*SWMM_Nnodes+4) * RECORDSIZE  // Node type, invert & max depth
             + (5*SWMM_Nlinks+6) * RECORDSIZE; // Link type, z1, z2, max depth & length
  offset = offset0 + offset;
  fseek(Fout, offset, SEEK_SET);

  // Read number & codes of computed variables
  fread(&SubcatchVars, RECORDSIZE, 1, Fout); // # Subcatch variables
  fseek(Fout, SubcatchVars*RECORDSIZE, SEEK_CUR);
  fread(&NodeVars, RECORDSIZE, 1, Fout);     // # Node variables
  fseek(Fout, NodeVars*RECORDSIZE, SEEK_CUR);
  fread(&LinkVars, RECORDSIZE, 1, Fout);     // # Link variables
  fseek(Fout, LinkVars*RECORDSIZE, SEEK_CUR);
  fread(&SysVars, RECORDSIZE, 1, Fout);     // # System variables

  // --- read data just before start of output results
  offset = StartPos - 3*RECORDSIZE;
  fseek(Fout, offset, SEEK_SET);
  fread(&SWMM_StartDate, sizeof(double), 1, Fout);
  fread(&SWMM_ReportStep, RECORDSIZE, 1, Fout);

  // --- compute number of bytes of results values used per time period
  BytesPerPeriod = 2*RECORDSIZE +      // date value (a double)
                   (SWMM_Nsubcatch*SubcatchVars +
                    SWMM_Nnodes*NodeVars+
                    SWMM_Nlinks*LinkVars +
                    SysVars)*RECORDSIZE;

  // --- return with file left open
  return err;
}

void InitGetIDName()
/** This function is strongly associated with GetIDName, GetInt. See comments there. **/
{
    countids=0;
    fseek(Fout,SWMM_Offset2IDS,SEEK_SET);
}

int GetInt()
{
    /** This function is strongly associated with GetIDName.
    User should always call
    1. InitGetIDName
    2. GetIDName function the required number of times.
    3. This function three required number of times.
    3. It should also be made sure that no other calls are made that will change the file position untill (2)
    is completely finished.
**/
    int unit;
    fread(&unit,RECORDSIZE,1,Fout);
    return unit;
}

void GetIDName(char* value)
/** This function is strongly associated with InitGetIDName. User should always call
1. InitGetIDName
2. This function the required number of times.
3. It should also be made sure that no other calls are made that will change the file position untill (2)
is completely finished.
{
**/
{

    int idsize;
    fread(&idsize,RECORDSIZE,1,Fout);
    fread(value,idsize,1,Fout);
    value[idsize]='\0'; // null termination is needed. C needs spoonfeeding!

}

//-----------------------------------------------------------------------------
int GetSwmmResult(int iType, int iIndex, int vIndex, int period, float* value)
//-----------------------------------------------------------------------------
{
  int offset;

  // --- compute offset into output file
  *value = 0.0;
  offset = StartPos + (period-1)*BytesPerPeriod + 2*RECORDSIZE;
  if ( iType == SUBCATCH )
  {
    offset += RECORDSIZE*(iIndex*SubcatchVars + vIndex);
  }
  else if (iType == NODE)
  {
    offset += RECORDSIZE*(SWMM_Nsubcatch*SubcatchVars +
                          iIndex*NodeVars + vIndex);
  }
  else if (iType == LINK)
  {
    offset += RECORDSIZE*(SWMM_Nsubcatch*SubcatchVars +
                          SWMM_Nnodes*NodeVars +
                          iIndex*LinkVars + vIndex);
  }
  else if (iType == SYS)
  {
    offset += RECORDSIZE*(SWMM_Nsubcatch*SubcatchVars +
                          SWMM_Nnodes*NodeVars +
                          SWMM_Nlinks*LinkVars + vIndex);
  }
  else return 1; // changed this 0>1 to match rest of the EPA convention (e.g. epanet)

  // --- re-position the file and read the result
  fseek(Fout, offset, SEEK_SET);
  fread(value, RECORDSIZE, 1, Fout);
  return 0; // changed this 1>0 to match rest of the EPA convention (e.g. epanet)
}


//-----------------------------------------------------------------------------
void CloseSwmmOutFile(void)
//-----------------------------------------------------------------------------
{
  if (Fout != NULL)
  {
    fclose(Fout);
    Fout = NULL;
  }
}

