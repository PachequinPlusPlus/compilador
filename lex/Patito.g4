grammar Patito;
@header{
import pprint
import sys
}
programa: 
    'program' ID PUNTOCOMA bloque {print("Accepted")};
bloque : LLA estatuto LLC;
estatuto : asignacion estatuto
            | condicion estatuto
            | escritura estatuto
            |
            ;
asignacion : ID IGUAL expresion PUNTOCOMA;
expresion : exp expresionaux;
expresionaux : CMP exp
                |
                ;

condicion : 'if' PA expresion PC bloque elsex PUNTOCOMA;

escritura : 'print' PA exporstring escrituraaux PC PUNTOCOMA;

exporstring : expresion
            | CTESTRING
            ;

escrituraaux : ',' exporstring 
            |
            ;
exp : termino signo;
signo : MAS exp
        | MENOS exp
        |
        ;

termino : factor terminoaux;
terminoaux : MULT factor
        | DIV factor
        | 
        ;
factor : PA expresion PC
	| factoraux varcte;
factoraux : MAS
	| MENOS
	| 
	;
varcte : ID
        | INT
        | FLOAT
        ;
INT : [1-9][0-9]*;
FLOAT : [0-9]*'.'[0-9]+;
MAS : '+';
MENOS : '-';
MULT : '*';
DIV : '/';
CMP : '>'
	| '<'
	| '<>';
IGUAL : '=';
PA : '(';
PC : ')';

CTESTRING : '"'.*?'"';

elsex : 'else' bloque
        | 
        ;
LLA : '{';
LLC : '}';
PUNTOCOMA : ';';
ID : [a-zA-Z][a-zA-Z0-9]*;
IGN : [ \t\r\n]+ -> skip ; // skip spaces, tabs, newlines


