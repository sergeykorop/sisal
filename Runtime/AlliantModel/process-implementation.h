/* AlliantModel */

#define GetProcId lib_processor_number()
#define GETPROCID(x) x = GetProc

static int AlliantTransfer( ProcId, ARs )
int ProcId;
struct ActRec *ARs;
{
  register struct ActRec *MyAR;

  MyAR = &ARs[ProcId];

  (*(MyAR->ChildCode))( MyAR->ArgPointer, 
			MyAR->SliceBounds[1], MyAR->SliceBounds[2] );
}


static int InParallel = FALSE; /* Used by Alliant model */

#define AlternateModelSpawn(FirstAR,Count) {\
    if ( InParallel ) { \
      register int Id; \
      for ( Id = 0; Id < Count; Id++ ) \
	Transfer( Id, FirstAR ); \
    } else { \
      InParallel = TRUE; \
      concurrent_call( 0, Transfer, Count, FirstAR ); \
      InParallel = FALSE; \
    }
