CREATE VIEW demanda_real_pereira AS
SELECT d."pkAgente",
    a."Actividad",
    a."Estado",
    d."Date",
    CASE 
        WHEN d.hora = 24 THEN (d."Date" + INTERVAL '1 day')::timestamp
        ELSE (d."Date" + ((d.hora-1)::text || ' hours')::interval)::timestamp
    END AS datetime,
    d.hora,
    d.demanda_real
FROM demanda_real d
JOIN agentes a ON d."pkAgente" = a."pkAgente"
WHERE a."Actividad" = 'COMERCIALIZACIÓN' AND d."pkAgente" = 'EEPC';