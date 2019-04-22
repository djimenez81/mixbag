% Archivo: uno.pl
% Fecha de creación: 2019-03-18
% Modificación: 2019-03-18
% Versión: 1
% Autor: David Jiménez

% Lista de parentescos familiares

% Familia paterna

male(santiago).
male(luis).
male(paulino).
male(rolando).
male(david).
male(daniel).
male(gabriel).
male(balta).
male(esteban).
male(carlos).
male(josesito).
male(javi).
male(ronald).
male(joel).
male(emmanuel).
male(thiago).
male(diego).
male(ruben).
male(estebitan).
male(nacho).
male(matias).
male(arturo).
male(beto).
male(jorge).
male(luisito).
male(bernie).



male(tytos).
male(tywin).
male(tyrion).
male(jaime).
male(joffrey).
male(tommen).
male(emmon_frey).
male(kevan).
male(lancel).
male(martyn).
male(willem).
male(tyrek).
male(gerion).



female(luz).
female(gina).
female(dyala).
female(cuca).
female(catalina).
female(gloriana).
female(daniela).
female(maribel).
female(norma).
female(eva).
female(siria).
female(malamala).
female(gorgie).
female(pri).
female(karina).
female(yanoa).
female(valeria).
female(carolina).
female(dani).
female(ale).
female(cami).
female(alicia).
female(elena).
female(rosa).
female(sonia).
female(sissy).
female(sofi).
female(vicky).
female(tati).
female(nati).
female(tefy).
female(coche).


female(jeyne_marbrand).
female(joanna).
female(cersei).
female(myrcella).
female(genna).
female(dorna).
female(janei).
female(darlessa_marbrand).
female(joy_hill).




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

parent(josecito,valeria).

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

% Lanister

parent(tytos,tywin).
parent(tytos,genna).
parent(tytos,kevan).
parent(tytos,tyggett).
parent(tytos,gerion).

parent(jeyne_marbrand,tywin).
parent(jeyne_marbrand,genna).
parent(jeyne_marbrand,kevan).
parent(jeyne_marbrand,tyggett).
parent(jeyne_marbrand,gerion).

parent(tywin,cersei).
parent(tywin,jaime).
parent(tywin,tyrion).

parent(joanna,cersei).
parent(joanna,jaime).
parent(joanna,tyrion).

parent(cersei,joffrey).
parent(cersei,myrcella).
parent(cersei,tommen).

parent(jaime,joffrey).
parent(jaime,myrcella).
parent(jaime,tommen).

parent(kevan,lancel).
parent(kevan,martyn).
parent(kevan,willem).
parent(kevan,janei).

parent(dorna,lancel).
parent(dorna,martyn).
parent(dorna,willem).
parent(dorna,janei).

parent(tyggett,tyrek).

parent(darlessa_marbrand,tyrek).

parent(gerion,joy_hill).

partners(genna,emmon_frey).
partners(X,Y) :- coparents(X,Y).



% REGLAS.

sibling(X,Y) :- parent(Z,X),parent(Z,Y),not(X=Y).

grandparent(X,Y) :- parent(X,Z),parent(Z,Y).

cousin(X,Y) :- grandparent(Z,X),grandparent(Z,Y),not(sibling(X,Y)),not(X=Y).

uncleaunt(X,Y) :- parent(Z,X),grandparent(Z,Y),not(parent(X,Y)).

coparents(X,Y) :- parent(X,Z),parent(Y,Z).

metamour(X,Y) :- coparents(X,Z),coparents(Y,Z).

mother(X,Y) :- parent(X,Y),female(X).

father(X,Y) :- parent(X,Y),male(X).

daughter(X,Y) :- parent(Y,X),female(X).

son(X,Y) :- parent(Y,X),male(X).

mom(X) :- parent(X,_),female(X).

dad(X) :- parent(X,_),male(X).

granny(X) :- grandparent(X,_),female(X).

granpa(X) :- grandparent(X,_),male(X).

uncle(X,Y) :- uncleaunt(X,Y),male(X).

aunt(X,Y) :- uncleaunt(X,Y),female(X).

nephew(X,Y) :- uncleaunt(Y,X),male(Y).

niece(X,Y) :- uncleaunt(Y,X),female(Y).


genealogy(A,D) :- parent(A,D),
                  write(D),
                  write(' <=1= '),
                  write(A).

genealogy(A,D) :- parent(A,X),
                  genealogy(X,D),
                  write(' <=2= '),
                  write(A).
