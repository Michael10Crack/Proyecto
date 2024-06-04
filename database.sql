-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 03-06-2024 a las 01:38:21
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `database`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `archivos`
--

CREATE TABLE `archivos` (
  `id` int(11) NOT NULL,
  `clave` varchar(255) NOT NULL,
  `tipo` enum('MAT','CSV') NOT NULL,
  `ruta` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `datos_csv`
--

CREATE TABLE `datos_csv` (
  `id` int(11) NOT NULL,
  `archivo_id` int(11) DEFAULT NULL,
  `nombre_columna` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `datos_mat`
--

CREATE TABLE `datos_mat` (
  `id` int(11) NOT NULL,
  `archivo_id` int(11) DEFAULT NULL,
  `nombre_matriz` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pacientes`
--

CREATE TABLE `pacientes` (
  `nombre` varchar(50) NOT NULL,
  `apellido` varchar(50) NOT NULL,
  `edad` varchar(3) NOT NULL,
  `identificacion` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `pacientes`
--

INSERT INTO `pacientes` (`nombre`, `apellido`, `edad`, `identificacion`) VALUES
('MICHAEL', 'SALAZAR', '21', '1001456812'),
('ESTEBAN', 'ARTUNDUAGA', '22', '123'),
('LIONEL ANDRES', 'MESSI', '34', '10'),
('JOSUE', 'PANIAGUA', '21', '789'),
('MICHAEL DAVID', 'SALAZAR', '23', '9090'),
('PUEDE', 'SER', '45', '456788'),
('', '', '', ''),
('HOLLA', 'SALUD', '34', '0880');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `archivos`
--
ALTER TABLE `archivos`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `datos_csv`
--
ALTER TABLE `datos_csv`
  ADD PRIMARY KEY (`id`),
  ADD KEY `archivo_id` (`archivo_id`);

--
-- Indices de la tabla `datos_mat`
--
ALTER TABLE `datos_mat`
  ADD PRIMARY KEY (`id`),
  ADD KEY `archivo_id` (`archivo_id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `archivos`
--
ALTER TABLE `archivos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `datos_csv`
--
ALTER TABLE `datos_csv`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `datos_mat`
--
ALTER TABLE `datos_mat`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `datos_csv`
--
ALTER TABLE `datos_csv`
  ADD CONSTRAINT `datos_csv_ibfk_1` FOREIGN KEY (`archivo_id`) REFERENCES `archivos` (`id`);

--
-- Filtros para la tabla `datos_mat`
--
ALTER TABLE `datos_mat`
  ADD CONSTRAINT `datos_mat_ibfk_1` FOREIGN KEY (`archivo_id`) REFERENCES `archivos` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
