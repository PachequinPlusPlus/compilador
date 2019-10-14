grammar Patito;
@header{
import pprint
import sys
}
programa: 
    'program' ID PUNTOCOMA vars? classes? functions? main {print("Accepted")};


main:
    'main' LLA stmt+ LLC;

functions:
    'func' returntype ID PA parameters PC LLA functionbloque LLC;

functionbloque:
    vars? stmt+ 'return' exp 
    | vars? stmt+ 
    ;

stmt:
    assignment PUNTOCOMA
    | loop
    | condition PUNTOCOMA
    | print PUNTOCOMA
    | input PUNTOCOMA
    | funccall PUNTOCOMA
    | method PUNTOCOMA
    ;
    

returntype:
    type
    | 'void';

parameters:
    type ID ',' parameters
    | ID ID ',' parameters
    |
    ;

vars:
    'var' LLA varsaux LLC;

varsaux:
    typevar varsAux
    |
    ;

typevar:
    ID typevaraux PUNTOCOMA
    | type typevaraux PUNTOCOMA;


type:
    'int'
    | 'float'
    | 'char'
    ;

classes:
    'class' ID LLA pv? pu? LLC
    | 'class' ID PP ID LLA pv? pu? LLC;

pu:
    'public' classdef;
    
pv:
    'private' classdef;

classdef:
    vars? functions?;
    
    
typevaraux:
    ID LB INT RB ',' typevaraux
    | ID typevaraux
    | 
    ;

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
PP : ':';
LB : '[';
RB : ']';
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


