-- CONSULTAS — universidad2

-- 1. Seleccionar todos los estudiantes 
SELECT * 
FROM Estudiante;

-- 2. Listar solo los nombres y apellidos 
SELECT Nombre, Apellido 
FROM Estudiante;

-- 3. Filtrar estudiantes de un departamento
SELECT *
FROM Estudiante
WHERE DepartamentoID = 1;

-- 4. Ordenar estudiantes por fecha de nacimiento (más viejos primero) 
SELECT *
FROM Estudiante
ORDER BY FechaNacimiento ASC;

-- 5. Contar cuántos estudiantes hay 
SELECT COUNT(*) AS TotalEstudiantes
FROM Estudiante;

-- 6. Buscar estudiantes con apellido 'García' 
SELECT *
FROM Estudiante
WHERE Apellido = 'García';

-- 7. Buscar nombres que empiezan con 'A'
SELECT *
FROM Estudiante
WHERE Nombre LIKE 'A%';

-- 8. JOIN: Mostrar nombre del estudiante y nombre del departamento 
SELECT 
    e.Nombre AS EstudianteNombre,
    e.Apellido AS EstudianteApellido,
    d.Nombre AS Departamento
FROM Estudiante e
INNER JOIN Departamento d
    ON e.DepartamentoID = d.DepartamentoID;

-- 9. Promedio de calificaciones por estudiante 
SELECT 
    e.EstudianteID,
    e.Nombre,
    e.Apellido,
    AVG(c.Nota) AS Promedio
FROM Estudiante e
INNER JOIN Inscripcion i
    ON e.EstudianteID = i.EstudianteID
INNER JOIN Calificacion c
    ON i.InscripcionID = c.InscripcionID
GROUP BY e.EstudianteID, e.Nombre, e.Apellido
ORDER BY Promedio DESC;

-- 10. Cantidad de estudiantes por departamento 
SELECT 
    d.Nombre AS Departamento,
    COUNT(e.EstudianteID) AS CantidadEstudiantes
FROM Departamento d
LEFT JOIN Estudiante e
    ON d.DepartamentoID = e.DepartamentoID
GROUP BY d.DepartamentoID, d.Nombre
ORDER BY CantidadEstudiantes DESC;

-- 11. Cursos impartidos por cada profesor 
SELECT 
    p.ProfesorID,
    p.Nombre AS ProfesorNombre,
    p.Apellido AS ProfesorApellido,
    COUNT(c.ClaseID) AS TotalCursosImpartidos
FROM Profesor p
LEFT JOIN Clase c
    ON p.ProfesorID = c.ProfesorID
GROUP BY p.ProfesorID, p.Nombre, p.Apellido
ORDER BY TotalCursosImpartidos DESC;

-- 12. Estudiantes con promedio mayor a 90 
SELECT E.Nombre, E.Apellido, AVG(C.Nota)*10 AS Promedio
FROM Estudiante E
JOIN Inscripcion I ON E.EstudianteID = I.EstudianteID
JOIN Calificacion C ON I.InscripcionID = C.InscripcionID
GROUP BY E.EstudianteID
HAVING AVG(C.Nota)*10 > 90; 

-- 13. TOP 5 estudiantes con mejores promedios 
SELECT 
    e.EstudianteID,
    e.Nombre,
    e.Apellido,
    AVG(c.Nota) AS Promedio
FROM Estudiante e
INNER JOIN Inscripcion i
    ON e.EstudianteID = i.EstudianteID
INNER JOIN Calificacion c
    ON i.InscripcionID = c.InscripcionID
GROUP BY e.EstudianteID, e.Nombre, e.Apellido
ORDER BY Promedio DESC
LIMIT 5;
