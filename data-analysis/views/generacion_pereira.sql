create view generacion_pereira as
SELECT 
a."pkAgente",
g."pkRecurso",
r."NombreRecurso" ,
r."Tipo_Recurso" ,
a."Actividad" ,
a."Estado" ,
g."Date",
hora,
t.temperatura_solar,
generacion
FROM tablasxm_dev.generacion g
inner join recursos r 
on g."pkRecurso" =r."pkRecurso"
inner join agentes a 
on r."pkAgente" =a."pkAgente"
left join temperatura_solar t
on t."pkRecurso" =g."pkRecurso" and g."Date" =t."Date"
where r."pkAgente"='EEPG' 
;