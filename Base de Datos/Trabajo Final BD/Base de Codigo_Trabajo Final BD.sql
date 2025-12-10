CREATE DATABASE IF NOT EXISTS sistema_academico;
USE sistema_academico;

CREATE TABLE departamento (
    id_departamento INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion VARCHAR(255)
);
CREATE TABLE estudiante (
    id_estudiante INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    fecha_nacimiento DATE,
    genero ENUM('M','F') NULL,
    id_departamento INT,
    CONSTRAINT fk_estudiante_departamento
        FOREIGN KEY (id_departamento) REFERENCES departamento(id_departamento)
);
CREATE TABLE profesor (
    id_profesor INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    correo VARCHAR(150),
    id_departamento INT,
    CONSTRAINT fk_profesor_departamento FOREIGN KEY (id_departamento)
        REFERENCES departamento (id_departamento)
);
CREATE TABLE curso (
    id_curso INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    codigo VARCHAR(20) NOT NULL UNIQUE,
    creditos INT NOT NULL,
    id_departamento INT,
    CONSTRAINT fk_curso_departamento
        FOREIGN KEY (id_departamento) REFERENCES departamento(id_departamento)
);
CREATE TABLE clase (
    id_clase INT AUTO_INCREMENT PRIMARY KEY,
    id_curso INT NOT NULL,
    id_profesor INT NOT NULL,
    periodo VARCHAR(20) NOT NULL,     -- Ej: 2025-1
    aula VARCHAR(20),
    horario VARCHAR(50),
    CONSTRAINT fk_clase_curso
        FOREIGN KEY (id_curso) REFERENCES curso(id_curso),
    CONSTRAINT fk_clase_profesor
        FOREIGN KEY (id_profesor) REFERENCES profesor(id_profesor)
);
CREATE TABLE inscripcion (
    id_inscripcion INT AUTO_INCREMENT PRIMARY KEY,
    id_estudiante INT NOT NULL,
    id_clase INT NOT NULL,
    fecha_inscripcion DATE NOT NULL,
    estado ENUM('ACTIVA','RETIRADA','APROBADA','REPROBADA') DEFAULT 'ACTIVA',
    CONSTRAINT fk_inscripcion_estudiante
        FOREIGN KEY (id_estudiante) REFERENCES estudiante(id_estudiante),
    CONSTRAINT fk_inscripcion_clase
        FOREIGN KEY (id_clase) REFERENCES clase(id_clase)
);
CREATE TABLE calificacion (
    id_calificacion INT AUTO_INCREMENT PRIMARY KEY,
    id_inscripcion INT NOT NULL,
    tipo VARCHAR(50) NOT NULL,   -- Ej: 'Parcial 1', 'Examen Final'
    nota DECIMAL(5,2) NOT NULL,  -- 0.00 - 100.00
    fecha_registro DATE NOT NULL,
    observaciones VARCHAR(255),
    CONSTRAINT fk_calificacion_inscripcion
        FOREIGN KEY (id_inscripcion) REFERENCES inscripcion(id_inscripcion)
	-- INSERTADO
                                 
-- Departamentos
INSERT INTO departamento (nombre, descripcion) VALUES
('Informática', 'Departamento de tecnologías de la información'),
('Matemáticas', 'Departamento de matemáticas básicas y avanzadas'),
('Lenguas', 'Departamento de idiomas y comunicación');

-- Estudiantes
INSERT INTO estudiante (nombre, apellido, fecha_nacimiento, genero, id_departamento) VALUES
('Ana', 'García', '2005-03-10', 'F', 1),
('Luis', 'Pérez', '2004-07-21', 'M', 1),
('María', 'Rodríguez', '2005-11-02', 'F', 2),
('Carlos', 'López', '2003-01-15', 'M', 3);

-- Profesores
INSERT INTO profesor (nombre, apellido, correo, id_departamento) VALUES
('José', 'Martínez', 'jmartinez@instituto.edu', 1),
('Elena', 'Torres', 'etorres@instituto.edu', 2),
('Pedro', 'Ramírez', 'pramirez@instituto.edu', 3);

-- Cursos
INSERT INTO curso (nombre, codigo, creditos, id_departamento) VALUES
('Programación I', 'INF101', 4, 1),
('Base de Datos', 'INF201', 4, 1),
('Cálculo I', 'MAT101', 3, 2),
('Inglés Básico', 'LEN101', 3, 3);

-- Clase
INSERT INTO clase (id_curso, id_profesor, periodo, aula, horario) VALUES
(1, 1, '2025-1', 'LAB-1', 'Lun-Mie 8:00-10:00'),
(2, 1, '2025-1', 'LAB-2', 'Mar-Jue 10:00-12:00'),
(3, 2, '2025-1', 'AULA-3', 'Lun-Mie 2:00-4:00'),
(4, 3, '2025-1', 'AULA-4', 'Mar-Jue 2:00-4:00');

-- Inscrpciones
INSERT INTO inscripcion (id_estudiante, id_clase, fecha_inscripcion, estado) VALUES
(1, 1, '2025-01-10', 'ACTIVA'),
(1, 2, '2025-01-10', 'ACTIVA'),
(2, 1, '2025-01-11', 'ACTIVA'),
(3, 3, '2025-01-12', 'ACTIVA'),
(4, 4, '2025-01-13', 'ACTIVA');

-- Calificaciones
INSERT INTO calificacion (id_inscripcion, tipo, nota, fecha_registro, observaciones) VALUES
(1, 'Parcial 1', 85.50, '2025-02-01', 'Buen desempeño'),
(1, 'Examen Final', 90.00, '2025-03-15', 'Muy buen desempeño'),
(2, 'Parcial 1', 75.00, '2025-02-02', 'Debe mejorar'),
(3, 'Examen Final', 88.00, '2025-03-16', 'Aprobado'),
(4, 'Examen Final', 92.00, '2025-03-17', 'Excelente');

-- CONSULTAS

-- Listar todos los estudiantes
SELECT * FROM estudiante;

-- Listar solo nombre y apellido de estudiantes
SELECT nombre, apellido FROM estudiante;

-- Filtrar estudiantes de un departamento específico (por ejemplo, Informática)
SELECT * FROM estudiante WHERE id_departamento = 1;

-- Ordenar estudiantes por fecha de nacimiento (más viejos primero)
SELECT * FROM estudiante ORDER BY fecha_nacimiento ASC;

-- JOINS

-- Estudiante y su departamento
SELECT e.nombre, e.apellido, d.nombre AS departamento
FROM estudiante e
JOIN departamento d ON e.id_departamento = d.id_departamento;

-- Profesores y sus departamentos
SELECT p.id_profesor, p.nombre, p.apellido, d.nombre AS departamento
FROM profesor p
JOIN departamento d ON p.id_departamento = d.id_departamento;

-- Clases con curso y profesor
SELECT c.id_clase, cu.nombre AS curso, p.nombre AS profesor
FROM clase c
JOIN curso cu ON c.id_curso = cu.id_curso
JOIN profesor p ON c.id_profesor = p.id_profesor;

-- Inscripciones con datos del estudiante, clase y curso
SELECT i.id_inscripcion, e.nombre AS estudiante, cu.nombre AS curso, p.nombre AS profesor
FROM inscripcion i
JOIN estudiante e ON i.id_estudiante = e.id_estudiante
JOIN clase cl ON i.id_clase = cl.id_clase
JOIN curso cu ON cl.id_curso = cu.id_curso
JOIN profesor p ON cl.id_profesor = p.id_profesor;

-- Notas de los estudiantes (uniendo hasta calificación)
SELECT e.nombre AS estudiante,
       e.apellido,
       cu.nombre AS curso,
       ca.tipo AS tipo_evaluacion,
       ca.nota
FROM calificacion ca
JOIN inscripcion i ON ca.id_inscripcion = i.id_inscripcion
JOIN estudiante e ON i.id_estudiante = e.id_estudiante
JOIN clase cl ON i.id_clase = cl.id_clase
JOIN curso cu ON cl.id_curso = cu.id_curso;

-- ESTADÍSTICAS

SELECT d.nombre AS departamento, COUNT(e.id_estudiante) AS total_estudiantes
FROM departamento d
LEFT JOIN estudiante e ON d.id_departamento = e.id_departamento
GROUP BY d.nombre;

SELECT AVG(nota) AS promedio_general
FROM calificacion;

-- CRUD

INSERT INTO estudiante (nombre, apellido, fecha_nacimiento, id_departamento)
VALUES ('Mario', 'Santos', '2002-08-10', 3);

UPDATE estudiante
SET apellido = 'Ramírez'
WHERE id_estudiante = 1;

DELETE FROM estudiante
WHERE id_estudiante = 4;








