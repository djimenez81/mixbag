% Archivo: parserlesco.pl
% Fecha: [2019-05-06]
% Modifcicación: [2019-06-30]
% Versión: 003
% Autor: David Jimenez
%


%%%%%%%%%%%%%
%%%%%%%%%%%%%
%%         %%
%%  NOTAS  %%
%%         %%
%%%%%%%%%%%%%
%%%%%%%%%%%%%

% Ejemplo de uso
%
% ?- phrase(sint_det,[tres,mi,perro,mujer,grande]).


%%%%%%%%%%%%%%
%%%%%%%%%%%%%%
%%          %%
%%  REGLAS  %%
%%          %%
%%%%%%%%%%%%%%
%%%%%%%%%%%%%%

sint_det --> det(1), sint_det_1.
sint_det --> pro_nom, sint_adj.
sint_det --> sint_det_1.
sint_det --> pro_nom.

sint_det_1 --> det(2), sint_det_2.
sint_det_1 --> sint_det_2.

sint_det_2 --> det(3), sint_det_3.
sint_det_2 --> sint_det_3.

sint_det_3 --> det(4), sint_det_4.
sint_det_3 --> sint_det_4.

sint_det_4 --> det(5), sint_nom.
sint_det_4 --> sint_nom.

sint_nom --> nom, sint_adj.
sint_nom --> nom.

sint_adj --> adj, sint_adj.
sint_adj --> adj.


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
           [este];
           [estos].

det(2) --> [mi];
           [tu];
           [su];
           [nuestro].

det(3) --> [otro];
           [todos];
           [todo].

det(4) --> [un];
           [uno];
           [dos];
           [tres];
           [cuatro];
           [cinco];
           [doce];
           [quince];
           [mucho];
           [poco];
           [todo].

det(5) --> [primer];
           [primero];
           [segundo];
           [tercer];
           [tercero];
           [ultimo].


%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%
%%           %%
%%  NOMBRES  %%
%%           %%
%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%
nom --> [abuelo];
        [agua];
        [almohada];
        [amigo];
        [anteojo];
        [arroz];
        [bola];
        [bombillo];
        [camisa];
        [carro];
        [casa];
        [clase];
        [cobija];
        [dia];
        [dinero];
        [doctor];
        [ducha];
        [enano];
        [esposo];
        [estudiante];
        [examen];
        [grupo];
        [guayaba];
        [hermano];
        [hijo];
        [hombre];
        [identidad];
        [iglesia];
        [jugador];
        [leon];
        [libro];
        [lista];
        [llave];
        [maleta];
        [mama];
        [manzana];
        [mar];
        [minuto];
        [mujer];
        [nino];
        [noche];
        [ojo];
        [ojos];
        [oportunidad];
        [pajaro];
        [papa];
        [parqueo];
        [pelicula];
        [persona];
        [perro];
        [piso];
        [pollo];
        [pregunta];
        [problema];
        [profesor];
        [queque];
        [recuerdo];
        [semana];
        [sordo];
        [suegro];
        [teatro];
        [televisor];
        [trabajo];
        [vez];
        [viento];
        [vida];
        [vino].



%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%
%%             %%
%%  ADJETIVOS  %%
%%             %%
%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%
adj --> [aburrido];
        [acido];
        [amigo];
        [azul];
        [bebe];
        [blanco];
        [bonito];
        [bueno];
        [caliente];
        [calor];
        [cansado];
        [carro];
        [casado];
        [chino];
        [cultura];
        [dificil];
        [dinero];
        [dulce];
        [enfermo];
        [enojado];
        [frio];
        [frito];
        [gordo];
        [grande];
        [hombre];
        [ingles];
        [inteligente];
        [lagrima];
        [largo];
        [lluvioso];
        [malo];
        [mama];
        [manana];
        [mejor];
        [miedo];
        [morena];
        [mujer];
        [negro];
        [nuevo];
        [oyente];
        [perdido];
        [profesional];
        [profesor];
        [publico];
        [rojo];
        [ruidoso];
        [siguiente];
        [sordo];
        [suave];
        [trabajo];
        [valiente];
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
