% Archivo: uno.pl
% Fecha de creación: 2019-03-18
% Modificación: 2019-03-18
% Versión: 1
% Autor: David Jiménez

% Lista de parentescos familiares

% Familia paterna
parent(luz,santiago).
parent(luz,gina).
parent(luz,dyala).
parent(luz,cuca).
parent(luz,luis).

parent(paulino,santiago).
parent(paulino,gina).
parent(paulino,dyala).
parent(paulino,cuca).
parent(paulino,luis).
parent(paulino,rolando).
parent(paulino,catalina).

parent(norma,rolando).
parent(norma,catalina).

parent(santiago,david).
parent(santiago,gloriana).
parent(santiago,daniela).
parent(santiago,daniel).
parent(santiago,gabriel).

parent(maribel,david).
parent(maribel,gloriana).

parent(eva,daniela).

parent(siria,daniel).
parent(siria,gabriel).

parent(gina,balta).
parent(gina,esteban).
parent(gina,malamala).
parent(gina,carlos).

parent(dyala,josecito).
parent(dyala,javi).
parent(dyala,gorgie).
parent(dyala,ronald).

parent(cuca,pri).

parent(luis,karina).

parent(gloriana,joel).
parent(gloriana,emmanuel).
parent(gloriana,yanoa).
parent(gloriana,thiago).

parent(jose,valeria).

parent(georgie,carolina).
parent(georgie,diego).

parent(javi,dani).
parent(javi,ale).
parent(javi,cami).

parent(malamala,ruben).
parent(malamala,estebitan).
parent(malamala,nacho).
parent(malamala,alicia).

parent(pri,matias).

parent(rolando,arturo).
parent(rolando,elena).

% Familia materna

parent(beto,jorge).
parent(beto,maribel).
parent(beto,rosa).
parent(beto,sonia).
parent(beto,sissy).
parent(beto,luisito).
parent(beto,sofi).

parent(vicky,jorge).
parent(vicky,maribel).
parent(vicky,rosa).
parent(vicky,sonia).
parent(vicky,sissy).
parent(vicky,luisito).
parent(vicky,sofi).

parent(rosa,tati).
parent(rosa,nati).

parent(sissy,bernie).

parent(sofi,tefy).
parent(sofi,coche).

% REGLAS.

sibling(X,Y) :- parent(Z,X),parent(Z,Y),not(X=Y).

grandparent(X,Y) :- parent(X,Z),parent(Z,Y).

cousin(X,Y) :- grandparent(Z,X),grandparent(Z,Y),not(sibling(X,Y)).

uncleaunt(X,Y) :- parent(Z,X),grandparent(Z,Y),not(parent(X,Y)).
