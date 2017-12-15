#include <ctype.h>
#include <stdio.h>
#include <string.h>

typedef struct {
    int PropN[4];
    int PropWire[4][20];
    int DriftN[2];
    int DriftWire[2][20];
    int DriftTime[2][20];
} EventStruct;

/*	Geometry (mm):
             |    |       |       |       |       |
    beam --> |<15>|<-390->|<-380->|<-300->|<-300->|
             |    |       |       |       |       |
             D1   D2      P1      P2      P3      P4
*/
#define ZD1	   0.
#define ZD2	  15.
#define ZP1	 405.
#define ZP2	 785.
#define ZP3	1085.
#define ZP4	1385.

int readEvent(FILE *fIn, EventStruct *Event)
{
    char str[2048];
    char *tok;
    char *tm;
    char mode;
    int num;
    const char delim[] = " \t\n\r";
    
    if (fIn == NULL) return 0;
    if (!fgets(str, sizeof(str), fIn)) return 0;
    mode = ' ';
    num = 0;
    memset(Event, 0, sizeof(EventStruct));
    tok = strtok(str, delim);
    for(;;) {
	if (tok == NULL) break;
	if (isalpha(tok[0])) {
	    mode = toupper(tok[0]);
	    num = strtol(&tok[1], NULL, 0) - 1;
	} else {
	    switch(mode) {
	    case 'P':
		if (num < 4 && num >= 0 && Event->PropN[num] < 20) {
		    Event->PropWire[num][Event->PropN[num]] = strtol(tok, NULL, 0);
		    Event->PropN[num]++;
		}
		break;
	    case 'D':
		if (num < 2 && num >= 0 && Event->DriftN[num] < 20) {
		    Event->DriftWire[num][Event->DriftN[num]] = strtol(tok, &tm, 0);
		    Event->DriftTime[num][Event->DriftN[num]] = strtol(&tm[1], NULL, 0);
		    Event->DriftN[num]++;
		}
		break;
	    default:
		break;
	    }
	}
	tok = strtok(NULL, delim);
    }
    return 1;
}
