CREATE DATABASE ventas;
USE ventas;

CREATE TABLE clientes (
    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    correo VARCHAR(100),
    telefono VARCHAR(20)
);

CREATE TABLE productos (
    id_producto INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    precio DECIMAL(10,2) NOT NULL
);

CREATE TABLE facturas (
    id_factura INT AUTO_INCREMENT PRIMARY KEY,
    fecha DATE NOT NULL,
    id_cliente INT NOT NULL,
    id_producto INT NOT NULL,
    cantidad INT NOT NULL,
    -- Claves foráneas
    CONSTRAINT fk_facturas_clientes
        FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente),
    CONSTRAINT fk_facturas_productos
        FOREIGN KEY (id_producto) REFERENCES productos(id_producto)
);

INSERT INTO clientes (nombre, apellido, correo, telefono) VALUES
('Juan', 'Pérez', 'juanperez@gmail.com', '809-555-1111'),
('Alba', 'Sánchez', 'albasanchez@gmail.com', '809-555-2222'),
('Carlos', 'Gómez', 'carlosgomez@gmail.com', '809-555-3333');

INSERT INTO productos (nombre, precio) VALUES
('Laptop', 45000.00),
('Mouse', 500.00),
('Teclado', 1200.00);

INSERT INTO facturas (fecha, id_cliente, id_producto, cantidad) VALUES
('2025-12-01', 1, 1, 1),  -- Juan compra 1 Laptop
('2025-12-02', 1, 2, 2),  -- Juan compra 2 Mouse
('2025-12-03', 2, 3, 1),  -- María compra 1 Teclado
('2025-12-04', 3, 1, 1);  -- Carlos compra 1 Laptop

SELECT f.id_factura,
       f.fecha,
       c.nombre AS nombre_cliente,
       c.apellido AS apellido_cliente,
       p.nombre AS producto,
       f.cantidad,
       (p.precio * f.cantidad) AS total_linea
FROM facturas f
JOIN clientes c ON f.id_cliente = c.id_cliente
JOIN productos p ON f.id_producto = p.id_producto;

SELECT c.id_cliente,
       CONCAT(c.nombre, ' ', c.apellido) AS cliente,
       SUM(p.precio * f.cantidad) AS total_comprado
FROM clientes c
JOIN facturas f ON c.id_cliente = f.id_cliente
JOIN productos p ON f.id_producto = p.id_producto
GROUP BY c.id_cliente, cliente;

SELECT p.id_producto,
       p.nombre,
       SUM(f.cantidad) AS total_vendido
FROM productos p
JOIN facturas f ON p.id_producto = f.id_producto
GROUP BY p.id_producto, p.nombre
ORDER BY total_vendido DESC;
