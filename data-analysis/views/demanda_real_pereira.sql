create 	view demanda_real_pereira as 
SELECT d."pkAgente",
    a."Actividad",
    a."Estado",
    d."Date",
    d.hora,
    d.demanda_real
   FROM (demanda_real d
     JOIN agentes a ON ((d."pkAgente" = a."pkAgente")))
  WHERE (((a."Actividad")::text = 'COMERCIALIZACIÓN'::text) AND (d."pkAgente" = 'EEPC'::text));