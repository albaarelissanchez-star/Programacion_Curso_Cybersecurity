-- CONSULTAS sistema academico

-- 1. Seleccionar todos los estudiantes
SELECT *
FROM estudiante;

-- 2. Listar solo nombres y apellidos
SELECT nombre, apellido
FROM estudiante;

-- 3. Filtrar estudiantes de un departamento
SELECT *
FROM estudiante
WHERE id_departamento = 1;

-- 4. Ordenar estudiantes por fecha de nacimiento (más viejos primero)
SELECT *
FROM estudiante
ORDER BY fecha_nacimiento ASC;

-- 5. Contar cuántos estudiantes hay
SELECT COUNT(*) AS total_estudiantes
FROM estudiante;

-- 6. Buscar estudiantes con apellido 'García'
SELECT *
FROM estudiante
WHERE apellido = 'García';

-- 7. Buscar por patrón (nombres que empiezan con 'A')
SELECT *
FROM estudiante
WHERE nombre LIKE 'A%';

-- 8. Join: Mostrar nombre del estudiante y nombre del departamento
SELECT e.nombre, e.apellido, d.nombre AS departamento
FROM estudiante e
INNER JOIN departamento d
    ON e.id_departamento = d.id_departamento;

-- 9. Promedio de calificaciones por estudiante
SELECT e.id_estudiante, e.nombre, e.apellido, AVG(c.nota) AS promedio
FROM estudiante e
INNER JOIN inscripcion i ON e.id_estudiante = i.id_estudiante
INNER JOIN calificacion c ON i.id_inscripcion = c.id_inscripcion
GROUP BY e.id_estudiante, e.nombre, e.apellido;

-- 10. Cantidad de estudiantes por departamento
SELECT d.nombre AS departamento, COUNT(e.id_estudiante) AS cantidad_estudiantes
FROM departamento d
LEFT JOIN estudiante e ON d.id_departamento = e.id_departamento
GROUP BY d.id_departamento, d.nombre;

-- 11. Cursos impartidos por cada profesor
SELECT p.nombre, p.apellido, c.nombre AS curso
FROM profesor p
INNER JOIN clase cl ON p.id_profesor = cl.id_profesor
INNER JOIN curso c ON cl.id_curso = c.id_curso;

-- 12. Estudiantes con promedio mayor a 90
SELECT e.id_estudiante, e.nombre, e.apellido, AVG(c.nota) AS promedio
FROM estudiante e
INNER JOIN inscripcion i ON e.id_estudiante = i.id_estudiante
INNER JOIN calificacion c ON i.id_inscripcion = c.id_inscripcion
GROUP BY e.id_estudiante, e.nombre, e.apellido
HAVING AVG(c.nota) > 90;

-- 13. Top 5 estudiantes con mejores promedios
SELECT e.id_estudiante, e.nombre, e.apellido, AVG(c.nota) AS promedio
FROM estudiante e
INNER JOIN inscripcion i ON e.id_estudiante = i.id_estudiante
INNER JOIN calificacion c ON i.id_inscripcion = c.id_inscripcion
GROUP BY e.id_estudiante, e.nombre, e.apellido
ORDER BY promedio DESC
LIMIT 5;












