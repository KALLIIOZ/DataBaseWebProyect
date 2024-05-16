DROP TABLE IF EXISTS Desarrolladores;
DROP TABLE IF EXISTS Plataformas;
DROP TABLE IF EXISTS Reseñas;
DROP TABLE IF EXISTS Generos;
DROP TABLE IF EXISTS Compras;

-- Crear tabla Desarrolladores
CREATE TABLE Desarrolladores (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Nombre VARCHAR(255) NOT NULL,
    Contacto VARCHAR(255)
);

-- Crear tabla Plataformas
CREATE TABLE Plataformas (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Nombre VARCHAR(255) NOT NULL,
    Especificaciones TEXT
);

-- Crear tabla Generos
CREATE TABLE Generos (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Nombre VARCHAR(255) NOT NULL
);

-- Crear tabla Videojuegos
CREATE TABLE Videojuegos (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Nombre VARCHAR(255) NOT NULL,
    Desarrollador_ID INT,
    Plataforma_ID INT,
    Genero_ID INT,
    Fecha_lanzamiento DATE,
    Precio DECIMAL(10, 2),
    FOREIGN KEY (Desarrollador_ID) REFERENCES Desarrolladores(ID),
    FOREIGN KEY (Plataforma_ID) REFERENCES Plataformas(ID),
    FOREIGN KEY (Genero_ID) REFERENCES Generos(ID)
);

-- Crear tabla Usuarios
CREATE TABLE Usuarios (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Nombre_usuario VARCHAR(255) NOT NULL,
    Correo_electronico VARCHAR(255) NOT NULL,
    Contrasena VARCHAR(255) NOT NULL
); 

Crear tabla Reseñas
CREATE TABLE Reseñas (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Usuario_ID INT,
    Videojuego_ID INT,
    Calificación INT,
    Comentario TEXT,
    FOREIGN KEY (Usuario_ID) REFERENCES Usuarios(ID),
    FOREIGN KEY (Videojuego_ID) REFERENCES Videojuegos(ID)
);

INSERT INTO Desarrolladores (Nombre, Contacto) VALUES 
('Mojang Studios', 'help@mojang.com'),
('Rockstar Games', 'help@rockstargames.com'),
('EA mobile', 'help@eamobile.com'),
('EA Sports', 'help@easports.com'),
('Nintendo', 'help@nintendo.com'),
('Arrowhead Studios', 'help@arrowhead.com'),
('FromSoftware', 'help@fromsoftware.com'),
('Riot Games', 'help@riotgames.com'),
('Respawn Entertainment', 'help@respawnentertainment.com'),
('Epic Games','help@epicgames.com');

INSERT INTO Plataformas (Nombre, Especificaciones) VALUES
('Playstation 4', 'Especificaciones de la consola PS4'),
('PC', 'Especificaciones generales para juegos de PC'),
('Xbox', 'Especificaciones generales para juegos de xbox'),
('Nintendo Switch', 'Especificaciones generales para juegos de Nintendo');

INSERT INTO Generos (Nombre) VALUES
('Acción'),
('Aventura'),
('Soulslike'),
('Metroidvania'),
('Open World'),
('MMORPG'),
('Estrategia');
