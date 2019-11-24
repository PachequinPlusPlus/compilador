grammar PPCDSALVC;
@header{
import pprint
import sys
}


start:
    programa;

programa: 
    'program' ID PUNTOCOMA variables? classes* functions* main ;

main:
    'main' LLA variables? stmt* LLC;

functions:
    'func' returntypes ID PA parameters? PC LLA functionbloque LLC;

functionbloque:
    variables? stmt* rt exp PUNTOCOMA
    | variables? stmt* 
    ;

rt:
    'return';

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
    ID LB scte RB 
    | ID;

secondType:
    COMA ID LB scte RB 
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
    ID PUNTO assignment |
    ID LB exp RB IGUAL exp ;



// todo(try to change foraux)
loop:
    ciclo
    | fciclo;

ciclo:
    'while' whilecond whilestmt;

whilecond:
    PA hyperexp PC ;

whilestmt:
    LLA stmt* LLC;

fciclo:
    'for' PA fassign PUNTOCOMA fciclocond PUNTOCOMA fcicloupd PC fciclobody;

fciclobody:
    LLA stmt* LLC;


fcicloupd:
    assignment foraux*;

fciclocond:
    hyperexp;

fassign:
    assignment foraux*;

foraux:
    COMA assignment;

method:
    ID PUNTO method
    | ID PUNTO mcall;

mcall:
    ID PA fparam PC;

// todo(try to change funcaux to (COMA exp)*
funccall:
    ID PA fparam PC;

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
    'if' PA hyperexp PC conditionsecond;

conditionsecond:
     LLA stmt* LLC elseif* elseotr?; 

elseif:
    'elseif' PA hyperexp PC conditionthird;

conditionthird:
    LLA stmt* LLC ;

elseotr:
    'else' LLA stmt* LLC;

hyperexp:
    superexp hyperexpaux*;

hyperexpaux:
    logicop superexp;

superexp:
    exp superexpaux?;

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
    | ID PA fparam PC
    | ID PUNTO ID PA fparam PC
    | ID PUNTO ID;


metodoaux:
    PA exp multipleexp* PC
    | PA PC;

fparam:
    exp nparam*
    |
    ;
nparam:
    COMA exp
    ;

scte:
    INT;

cte:
    INT
    | FLOAT
    | CHAR;


parent:
    PA hyperexp PC;


INT : [1-9][0-9]* | [0];
FLOAT : [0-9]*'.'[0-9]+;
CHAR: '\'' (~['\\\r\n\u0085\u2028\u2029] | CommonCharacter) '\'';

fragment CommonCharacter
    : SimpleEscapeSequence
    | HexEscapeSequence
    | UnicodeEscapeSequence
    ;
    fragment SimpleEscapeSequence
    : '\\\''
    | '\\"'
    | '\\\\'
    | '\\0'
    | '\\a'
    | '\\b'
    | '\\f'
    | '\\n'
    | '\\r'
    | '\\t'
    | '\\v'
    ;
    fragment HexEscapeSequence
    : '\\x' [0-9a-fA-F]
    | '\\x' [0-9a-fA-F][0-9a-fA-F]
    | '\\x' [0-9a-fA-F][0-9a-fA-F][0-9a-fA-F]
    | '\\x' [0-9a-fA-F][0-9a-fA-F][0-9a-fA-F][0-9a-fA-F]
    ;

fragment UnicodeEscapeSequence
    : '\\u' [0-9a-fA-F][0-9a-fA-F][0-9a-fA-F][0-9a-fA-F]
    | '\\U' [0-9a-fA-F][0-9a-fA-F][0-9a-fA-F][0-9a-fA-F]
            [0-9a-fA-F][0-9a-fA-F][0-9a-fA-F][0-9a-fA-F]
    ;
MAS : '+';
MENOS : '-';
MULT : '*';
DIV : '/';

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


