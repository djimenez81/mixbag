% Archivo: gramej.pl
% Fecha: [2019-05-13]
% Modifcicación: [2019-04-09]
% Versión: 001
% Autor: David Jimenez
%




% Defina una gramática con reglas DCG que dé cuenta de las frases
% siguientes:
% la reina tiene un dragón
% la reina cabalga un dragón
% el dragón escupe fuego
% el consejero considera las opciones
% los guardas protegen la fortaleza
% los soldados defienden los habitantes
% los habitantes llegan a los refugios

oracion --> sintagma_nominal(G,N),sintagma_verbal(N).

sintagma_nominal(G,N) --> determinante(G,N),nombre(G,N).
sintagma_nominal(G,N) --> determinante(G,N),nombre(G,N),adjetivo(G,N).
sintagma_nominal(G,N) --> nombre_propio(G,N).

sintagma_verbal(N) --> verbo(N),sintagma_nominal(_,_).
sintagma_verbal(N) --> verbo(N),sintagma_preposicional.
sintagma_verbal(N) --> verbo(N),nombre(_,_).

sintagma_preposicional --> preposicion,sintagma_nominal(_,_).


determinante(masc,sing) --> [el]; [un].
determinante(fem,sing) --> [la]; [una].
determinante(masc,plu) --> [los]; [unos].
determinante(fem,plu) --> [las]; [unas].

nombre(fem,sing) --> [reina]; [fortaleza].

nombre(masc,sing) --> [dragon]; [fuego]; [consejero].

nombre(fem,plu)  --> [opciones].

nombre(masc,plu)  --> [guardas]; [soldados]; [habitantes]; [refugios].

preposicion --> [a].

verbo(sing) --> [tiene]; [cabalga]; [escupe]; [considera].
verbo(plu) --> [protejen]; [defienden]; [llegan].

nombre_propio(fem,sing) --> [daenerys].
nombre_propio(masc,sing) --> [tyrion].

adjetivo(_,sing) --> [enorme].
adjetivo(_,plu) --> [viables].
adjetivo(_,sing) --> [central].
adjetivo(masc,plu) --> [armados].
