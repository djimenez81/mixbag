% Archivo: 06-parser_tagging.pl
% Fecha: [2015-03-09]
% Modificación: [2019-04-09]
% Versión: 006
% Autor: Jorge Antonio Leoni de León
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Para poner en funcionamiento la gramática están las siguientes opciones:
%
% (1) oracion(S,[unos,lectores,leen,los,libros],[]).
%
% (2) phrase(oracion(Tree), [el,arbol,reflexiona]).
%
% (3) phrase(oracion(Tree),Sentence).
%
% (4) between(1,8,N), length(S,N), phrase(oracion(_),S), writeln(S), sleep(0.2),false.
%
% (5) phrase(oracion(Tree), X), io__write_term_as_tree(X).
%
% (6) phrase(oracion(Arbol), [los,japoneses,compran,unas,novelas]), io__write_term_as_tree(Arbol).
%
% (7) tokenize_line(ORACION), oracion(ESTRUCTURA, ORACION, []).
%
% (8) tokenize_line(INPUT), phrase(oracion(Arbol), INPUT), io__write_term_as_tree(Arbol).
%
% Observaciones:
%
% (a) Para que (5) y (8) funcionen, es necesario el programa '00-io.pl'.
%
% (b) La opción (4) despliega todas las opciones que contengan de uno a ocho elementos
% terminales. Es posible adaptarlo para todas las otras posibilidad de funcionamiento.
%
% (c) Los comandos en (7) y (8) requieren invocar '00-tokenizer-nugues.pl'.
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%oracion --> oracion(N,V).

oracion(oracion(N,V)) --> sintagma_nominal(N,RASGO), sintagma_verbal(V,RASGO).

sintagma_nominal(sintagma_nominal(D,N),RASGO) --> sintagma_determinante(D,RASGO), nombre(N,RASGO).
sintagma_nominal(sintagma_nominal(P),RASGO) --> pronombre(P,RASGO).

sintagma_determinante(sintagma_determinante(D),RASGO) --> determinante(D, RASGO).

% Si en esta regla, el sn tiene activo RASGO, habrá concordancia a lo
% largo de todo el árbol y Prolog buscará unificar con el rasgo 'plu' el
% sujeto, el verbo y el complemento directo, lo que es incorrecto,
% puesto nada más el sujeto y el verbo deben concordar, así como el
% determinante y el nombre:
%
% sintagma_verbal(sintagma_verbal(V,N),RASGO) --> verbo(V,RASGO),
% sintagma_nominal(N,RASGO).

sintagma_verbal(sintagma_verbal(V,N),RASGO) --> verbo(V,RASGO), sintagma_nominal(N,_).
sintagma_verbal(sintagma_verbal(V),RASGO) --> verbo(V,RASGO).

pronombre(pronombre(el),sg) --> [el].
pronombre(pronombre(ella),sg) --> [ella].

pronombre(pronombre(ellos),plu) --> [ellos].
pronombre(pronombre(ellas),plu) --> [ellas].


determinante(determinante(mucho),sg) --> [mucho].
determinante(determinante(el),sg) --> [el].
determinante(determinante(la),sg) --> [la].

determinante(determinante(un),sg) --> [un].
determinante(determinante(una),sg) --> [una].

determinante(determinante(las),plu) --> [las].
determinante(determinante(los),plu) --> [los].

determinante(determinante(muchos),plu) --> [muchos].
determinante(determinante(unas),plu) --> [unas].
determinante(determinante(unos),plu) --> [unos].

%nombre(nombre([]),_) --> [].

nombre(nombre(arbol),sg) --> [arbol].
nombre(nombre(artista),sg) --> [artista].
nombre(nombre(consejero),sg) --> [consejero].
nombre(nombre(dragon),sg) --> [dragon].
nombre(nombre(estudiante),sg) --> [estudiante].
nombre(nombre(fortaleza),sg) --> [fortaleza].
nombre(nombre(fuego),sg) --> [fuego].
nombre(nombre(libro),sg)  --> [libro].
nombre(nombre(modelo),sg) --> [modelo].
nombre(nombre(novela),sg) --> [novela].
nombre(nombre(reina),sg) --> [reina].
nombre(nombre(vino),sg) --> [vino].

nombre(nombre(arboles),plu) --> [arboles].
nombre(nombre(artistas),plu) --> [artistas].
nombre(nombre(botellas),plu) --> [botellas].
nombre(nombre(esculturas),plu) --> [esculturas].
nombre(nombre(estudiantes),plu) --> [estudiantes].
nombre(nombre(habitantes),plu) --> [habitantes].
nombre(nombre(japoneses),plu) --> [japoneses].
nombre(nombre(lectores),plu) --> [lectores].
nombre(nombre(libros),plu) --> [libros].
nombre(nombre(novelas),plu) --> [novelas].
nombre(nombre(opciones),plu) --> [opciones].
nombre(nombre(soldados),plu) --> [soldados].

verbo(verbo(compra),sg) --> [compra].
verbo(verbo(considera),sg) --> [considera].
verbo(verbo(escupe),sg) --> [escupe].
verbo(verbo(esculpe),sg) --> [esculpe].
verbo(verbo(reflexiona),sg) --> [reflexiona].
verbo(verbo(tiene),sg) --> [tiene].
verbo(verbo(toma),sg) --> [toma].

verbo(verbo(compran),plu) --> [compran].
verbo(verbo(defienden),plu) --> [defienden].
verbo(verbo(discuten),plu) --> [discuten].
verbo(verbo(esculpen),plu) --> [esculpen].
verbo(verbo(leen),plu) --> [leen].
verbo(verbo(protegen),plu) --> [protejen].
verbo(verbo(toman),plu) --> [toman].
verbo(verbo(visitan),plu) --> [visitan].
