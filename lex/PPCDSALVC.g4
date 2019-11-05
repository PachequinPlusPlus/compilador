grammar PPCDSALVC;
@header{
import pprint
import sys
}



programa: 
    'program' ID PUNTOCOMA variables? classes* functions* main ;

main:
    'main' LLA variables? stmt+ LLC;

functions:
    'func' returntypes ID PA parameters? PC LLA functionbloque LLC;

functionbloque:
    variables? stmt+ 'return' exp PUNTOCOMA
    | variables? stmt+ 
    ;

stmt:
    assignment PUNTOCOMA
    | loop
    | condition 
    | imprimir PUNTOCOMA
    | entrada PUNTOCOMA
    | funccall PUNTOCOMA
    | method PUNTOCOMA
    ;
    
returntypes:
    TYPES
    | 'void';

params:
    COMA TYPES ID
    | COMA ID ID;

paramfirst:
    TYPES ID params*
    | ID ID params*;

// check here
parameters:
    paramfirst;

variables:
    'var' LLA typesvar+ LLC;


typesvar:
    ID typesvaraux  secondType* PUNTOCOMA
    | TYPES typesvaraux secondType* PUNTOCOMA;

typesvaraux:
    ID LB INT RB 
    | ID;

secondType:
    COMA ID LB INT RB 
    | COMA ID;

TYPES:
    'int'
    | 'float'
    | 'char'
    ;

classes:
    'class' ID LLA pv? pu? LLC
    | 'class' ID PP ID LLA pv? pu? LLC;

pu:
    'public' PP classdef;
    
pv:
    'private' PP classdef;

classdef:
    variables? functions*;
    

assignment:
    ID IGUAL exp |
    ID LB exp RB IGUAL exp |
    ID PUNTO assignment;

// todo(try to change foraux)
loop:
    'while' PA hyperexp PC LLA stmt* LLC
    | 'for' PA assignment foraux* PUNTOCOMA hyperexp PUNTOCOMA assignment foraux* PC LLA stmt* LLC;

foraux:
    COMA assignment;

method:
    ID PUNTO method
    | ID PUNTO funccall;

// todo(try to change funcaux to (COMA exp)*
funccall:
    ID PA exp multipleexp* PC
    | ID PA PC;

multipleexp:
    COMA exp;

imprimir:
    'print' PA exp multipleexp* PC;

entrada:
    'input' PA ID arreglo? attr? entradaaux* PC;

entradaaux:
    COMA ID arreglo? attr?;

arreglo:
   LB exp RB;

attr:
    PUNTO ID;

relationalop:
    '<'
    | '>'
    | '!='
    | '<='
    | '>='
    | '==';

logicop:
    '&&'
    | '||';

condition:
    'if' PA hyperexp PC LLA stmt* LLC elseif? elseotr?;

elseif:
    'elseif' PA hyperexp PC LLA stmt* LLC;

elseotr:
    'else' LLA stmt* LLC;

hyperexp:
    superexp hyperexpaux*;

hyperexpaux:
    logicop superexp;

superexp:
    exp superexpaux*;

superexpaux:
    relationalop exp;

exp:
    term expaux*;

expaux:
    binbasico term;

binbasico:
    MAS
    | MENOS;

term:
    factor termaux*;

termaux:
    bincomplejo factor;

bincomplejo:
    MULT
    | DIV;

signosunarios:
    '!'
    | '+'
    | '-';

factor:
    signosunarios? factorclases
    | signosunarios? cte
    | signosunarios? parent;

factorclases:
    ID
    | ID arreglo
    | ID PA exp multipleexp* PC
    | ID PUNTO ID metodoaux?;

metodoaux:
    PA exp multipleexp* PC
    | PA PC;

cte:
    INT
    | FLOAT
    | CHAR;


parent:
    PA hyperexp PC;





INT : [1-9][0-9]* | [0];
FLOAT : [0-9]*'.'[0-9]+;
CHAR : '\''.'\'';
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



LLA : '{';
LLC : '}';
PUNTO : '.';
COMA : ',';
PUNTOCOMA : ';';
ID : [a-zA-Z][a-zA-Z0-9]*;
IGN : [ \t\r\n]+ -> skip ; // skip spaces, tabs, newlines


