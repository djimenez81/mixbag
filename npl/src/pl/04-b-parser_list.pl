% Archivo: 04-b-parser_list.pl
% Fecha: [2015-04-13]
% Modifcicación: [2019-04-09]
% Versión: 002
% Autor: Jorge Antonio Leoni de León
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Para poner en funcionamiento la gramática están las siguientes opciones:
%
% (1)	a. phrase(oracion,[el,artista,toma,el,vino]).
%		b. oracion([el,artista,esculpe,el,arbol],[]).
%
% (2) oracion(X,L).
%
% (3) oracion(X,[]).
%
% (4) phrase(oracion,L).
%
% (5) between(1,8,N), length(S,N), phrase(oracion,S), writeln(S), sleep(0.2),false.
%
% (6) tokenize_line(X), oracion(X,[]).
%
% Observaciones:
%
% (a) La opción (5) despliega todas las opciones que contengan de uno a ocho elementos
% terminales. Es posible adaptarlo para todas las otras posibilidad de funcionamiento.
%
% (b) En (6) es necesario invocar '00-tokenizer-nugues.pl'.
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
% [trace]  ?- sintagma_nominal([el,arbol],[]).
%  Call: (6) sintagma_nominal([el, arbol], []) ? creep	--> Con q regla obtengo esta L?
%  Call: (7) determinante([el, arbol], _G411) ? creep	--> Creación de una variable
%  Exit: (7) determinante([el, arbol], [arbol]) ? creep	--> d([el,[arbol]], [arbol]) ?
%  Call: (7) nombre([arbol], []) ? creep				--> Ok: n([arbol],[]).
%  Exit: (7) nombre([arbol], []) ? creep
%  Exit: (6) sintagma_nominal([el, arbol], []) ? creep	--> Sí sn--> det sn.
% true .
%

oracion(S0,S) :-
	sintagma_nominal(S0,S1),
	sintagma_verbal(S1,S).

sintagma_nominal(S0,S) :-
	sintagma_determinante(S0,S1),
	nombre(S1,S).

sintagma_determinante(S0,S) :-
	determinante(S0,S).

sintagma_verbal(S0,S) :-
	verbo(S0,S).

sintagma_verbal(S0,S) :-
	verbo(S0,S1),
	sintagma_nominal(S1,S).

determinante([el|S],S).
determinante([un|S],S).

nombre([arbol|S],S).
nombre([artista|S],S).
nombre([profesor|S],S).
nombre([vino|S],S).
nombre([examen|S],S).

verbo([esculpe|S],S).
verbo([toma|S],S).
verbo([reflexiona|S],S).
verbo([entrego|S],S).
