% Archivo: 04-d-simpleparser.pl
% Fecha: [2015-03-09]
% Modifcicación: [2019-04-09]
% Versión: 001
% Autor: Jorge Antonio Leoni de León
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Para poner en funcionamiento la gramática están las siguientes opciones:
%
% (1) phrase(oracion,[el,artista,toma,el,vino]).
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
oracion --> sintagma_nominal, sintagma_verbal.
sintagma_nominal --> determinante, nombre.
sintagma_verbal --> verbo, sintagma_nominal.
sintagma_verbal --> verbo.

determinante --> [el].
determinante --> [un].

nombre --> [arbol].
nombre --> [artista].
nombre --> [vino].

verbo --> [esculpe].
verbo --> [toma].
verbo --> [reflexiona].
