CREATE DATABASE biblioteca;
USE biblioteca;

CREATE TABLE autores (
    id_autor INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    nacionalidad VARCHAR(50)
);

CREATE TABLE libros (
    id_libro INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(150) NOT NULL,
    anio_publicacion INT,
    id_autor INT,
    
    CONSTRAINT fk_libros_autores
        FOREIGN KEY (id_autor) REFERENCES autores(id_autor)
);

INSERT INTO autores (nombre, nacionalidad) VALUES
('Gabriel García Márquez', 'Colombiana'),
('Isabel Allende', 'Chilena'),
('Mario Vargas Llosa', 'Peruana');

INSERT INTO libros (titulo, anio_publicacion, id_autor) VALUES
('Cien años de soledad', 1967, 1),
('El coronel no tiene quien le escriba', 1961, 1),
('La casa de los espíritus', 1982, 2),
('Paula', 1994, 2),
('La ciudad y los perros', 1963, 3);

SELECT l.id_libro, l.titulo, l.anio_publicacion, a.nombre AS autor
FROM libros l
JOIN autores a ON l.id_autor = a.id_autor;

SELECT titulo, anio_publicacion
FROM libros
WHERE anio_publicacion > 1970;

SELECT a.nombre AS autor, COUNT(l.id_libro) AS cantidad_libros
FROM autores a
LEFT JOIN libros l ON a.id_autor = l.id_autor
GROUP BY a.id_autor, a.nombre;
