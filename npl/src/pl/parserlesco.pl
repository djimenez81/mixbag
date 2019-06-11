% Archivo: parlesco.pl
% Fecha: [2019-05-06]
% Modifcicación: [2019-06-10]
% Versión: 002
% Autor: David Jimenez
%


%%%%%%%%%%%%%
%%%%%%%%%%%%%
%%         %%
%%  NOTAS  %%
%%         %%
%%%%%%%%%%%%%
%%%%%%%%%%%%%

% Oracion 23 debe ser poco azucar no azucar poco.
% Oracion 24 debe ser "esos sordo amigo"

% Ultima hecha 25


%%%%%%%%%%%%%%
%%%%%%%%%%%%%%
%%          %%
%%  REGLAS  %%
%%          %%
%%%%%%%%%%%%%%
%%%%%%%%%%%%%%

sing_det --> det(1), sing_det_1.
sing_det --> sing_det_1.

sing_det_1 --> det(2), sing_det_2.
sing_det_1 --> sing_det_2.

sing_det_2 --> det(3), sing_det_3.
sing_det_2 --> sing_det_3.

sing_det_3 --> det(4), sing_det_4.
sing_det_3 --> sing_det_4.

sing_det_4 --> det(5), sing_nom.
sing_det_4 --> sing_nom.

sing_nom --> nom, sing_adj.
sing_nom --> nom.

sing_adj --> adj, sing_adj.
sing_adj --> adj.


%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%
%%                 %%
%%  DETERMINANTES  %%
%%                 %%
%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%

det(1) --> [aquel];
           [ese];
           [esos];
           [este].

det(2) --> [mi];
           [tu];
           [su];
           [nuestro].

det(3) --> [otro];
           [todo].

det(4) --> [un];
           [uno];
           [dos];
           [tres];
           [cuatro];
           [cinco];
           [quince];
           [mucho];
           [poco];
           [todo].

det(5) --> [primero];
           [segundo];
           [ultimo].


%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%
%%           %%
%%  NOMBRES  %%
%%           %%
%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%
nom --> [abuelo];
        [bola];
        [carro];
        [casa];
        [dia];
        [dinero];
        [doctor];
        [examen];
        [esposo];
        [iglesia];
        [manzana];
        [minuto];
        [pelicula];
        [persona];
        [perro];
        [problema];
        [profesor];
        [queque];
        [sordo];
        [vez].



%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%
%%             %%
%%  ADJETIVOS  %%
%%             %%
%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%
adj --> [blanco];
        [bonito];
        [bueno];
        [caliente];
        [dificil];
        [enfermo];
        [enojado];
        [frio];
        [gordo];
        [grande];
        [hombre];
        [lluvioso];
        [mujer];
        [nuevo];
        [perdido];
        [profesor];
        [verde];
        [viejo].


%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%
%%              %%
%%  PRONOMBRES  %%
%%              %%
%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%
pro_nom --> [yo];
            [tu];
            [el];
            [nosotros];
            [ustedes];
            [ellos].
