CREATE DATABASE colegio;
USE colegio;

CREATE TABLE estudiantes (
    id_estudiante INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    fecha_nacimiento DATE,
    correo VARCHAR(100)
);

CREATE TABLE cursos (
    id_curso INT AUTO_INCREMENT PRIMARY KEY,
    nombre_curso VARCHAR(100) NOT NULL,
    creditos INT NOT NULL
);

CREATE TABLE matriculas (
    id_matricula INT AUTO_INCREMENT PRIMARY KEY,
    id_estudiante INT NOT NULL,
    id_curso INT NOT NULL,
    fecha_matricula DATE NOT NULL,
    
    CONSTRAINT fk_matriculas_estudiantes
        FOREIGN KEY (id_estudiante) REFERENCES estudiantes(id_estudiante),
    CONSTRAINT fk_matriculas_cursos
        FOREIGN KEY (id_curso) REFERENCES cursos(id_curso)
);

INSERT INTO estudiantes (nombre, apellido, fecha_nacimiento, correo) VALUES
('Alba', 'Sánchez', '2008-05-10', 'albasanchez@gmail.com'),
('Luis', 'Martínez', '2007-11-22', 'luismartinez@gmail.com'),
('Carla', 'Rodríguez', '2009-03-15', 'carlarodriguez@gmail.com');

INSERT INTO cursos (nombre_curso, creditos) VALUES
('Matemáticas', 4),
('Lengua Española', 3),
('Inglés', 2);

INSERT INTO matriculas (id_estudiante, id_curso, fecha_matricula) VALUES
(1, 1, '2025-01-15'),  -- Alba en Matemáticas
(1, 2, '2025-01-15'),  -- Alba en Lengua Española
(2, 1, '2025-01-16'),  -- Luis en Matemáticas
(2, 3, '2025-01-16'),  -- Luis en Inglés
(3, 2, '2025-01-17');  -- Carla en Lengua Española

SELECT e.id_estudiante,
       CONCAT(e.nombre, ' ', e.apellido) AS estudiante,
       c.nombre_curso,
       m.fecha_matricula
FROM matriculas m
JOIN estudiantes e ON m.id_estudiante = e.id_estudiante
JOIN cursos c ON m.id_curso = c.id_curso
ORDER BY estudiante, c.nombre_curso;

SELECT e.id_estudiante,
       CONCAT(e.nombre, ' ', e.apellido) AS estudiante,
       COUNT(m.id_curso) AS cantidad_cursos
FROM estudiantes e
LEFT JOIN matriculas m ON e.id_estudiante = m.id_estudiante
GROUP BY e.id_estudiante, estudiante;

SELECT c.nombre_curso,
       CONCAT(e.nombre, ' ', e.apellido) AS estudiante
FROM matriculas m
JOIN estudiantes e ON m.id_estudiante = e.id_estudiante
JOIN cursos c ON m.id_curso = c.id_curso
WHERE c.nombre_curso = 'Matemáticas';
