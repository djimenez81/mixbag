function [  ] = printCloudsOverlay(C1, C2, pivote1, pivote2, angulo)
%PRINTMAXCLOUDOVERLAY Imprime las 2 nubes de puntos y muestra su traslape
%El paquete de Computer Vision no está en las licencias de la U.

  R = [cos(angulo), -sin(angulo); sin(angulo), cos(angulo)];

  C1nueva = C1 - C1(pivote1,:);
  C2nueva = (C2 - C2(pivote2,:))*R';

%Primero imprimimos la superposición

  scatter(C1nueva(:,1), C1nueva(:,2), 20, 'rs', 'LineWidth', 2)
  hold on %Permite que la nueva gráfica se sobreescriba sobre la vieja
  scatter(C2nueva(:,1), C2nueva(:,2), 20, 'bd', 'LineWidth', 1)
  grid on
  hold off

end
