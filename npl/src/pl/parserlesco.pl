% Archivo: 04-b-parser_list.pl
% Fecha: [2019-05-06]
% Modifcicación: [2019-04-09]
% Versión: 001
% Autor: David Jimenez
%

% sintagma_nominal --> sintagma_nominal, calificativo.
sintagma_nominal --> determinante_d, sintagma_nominal_d.
sintagma_nominal --> sintagma_nominal_d.

sintagma_nominal_d --> determinante_po, sintagma_nominal_po.
sintagma_nominal_d --> sintagma_nominal_po.

sintagma_nominal_po --> determinante_pr, sintagma_nominal_pr.
sintagma_nominal_po --> sintagma_nominal_pr.

sintagma_nominal_pr --> determinante_cc, sintagma_nominal_cc.
sintagma_nominal_pr --> sintagma_nominal_cc.

sintagma_nominal_cc --> determinante_co, sintagma_nominal_co.
sintagma_nominal_cc --> sintagma_nominal_co.

sintagma_nominal_co --> nombre, calificacion.
sintagma_nominal_co --> nombre.

calificacion --> calificativo, calificacion.
calificacion --> calificativo.


% DETERMINANTES DEMOSTRATIVOS
determinante_d --> [este].
determinante_d --> [ese].
determinante_d --> [aquel].


% DETERMINANTES POSESIVOS
determinante_po --> pronombre.

% DETERMINANTES PREDETERMINANTES
determinante_pr --> [otro].
determinante_pr --> [todo].


% DETERMINANTES CUANTIFICADORES DE CANTIDAD
determinante_cc --> [un].
determinante_cc --> [uno].
determinante_cc --> [dos].
determinante_cc --> [tres].
determinante_cc --> [cuatro].
determinante_cc --> [cinco].

determinante_cc --> [mucho].
determinante_cc --> [todo].

% DETERMINANTES CUANTIFICADORES DE ORDEN
determinante_co --> [primero].
determinante_co --> [segundo].


% NOMBRES
nombre --> [doctor].
nombre --> [perro].

% CALIFICATIVOS
calificativo --> [hombre].
calificativo --> [grande].

% PRONOMBRES
pronombre --> [yo].
pronombre --> [usted].
pronombre --> [el].
pronombre --> [ella].
pronombre --> [nosotros].
pronombre --> [ustedes].
pronombre --> [ellos].
