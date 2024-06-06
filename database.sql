-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 02-06-2024 a las 15:15:06
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
('MARTHA', 'FUERTE', '15', '1000476351'),
('LINA', 'VASQUEZ', '25', '1025369784'),
('MARCELA', 'ALVAREZ', '26', '1113537397'),
('FRANCO', 'MESA', '22', '1783246222'),
('CAMILA', 'PEÑA', '5', '1783364'),
('SOFIA', 'MUEH', '45', '4786455'),
('LINA', 'FRANCO', '45', '47895467'),
('VALERIA', 'MEJIA', '61', '54789224'),
('JUANA', 'ARCO', '12', '54961148'),
('AMANDA', 'MIGUEL', '47', '566484984'),
('JUAN', 'JURADO', '63', '57845962'),
('JULIO', 'VEGA', '36', '61249781'),
('MATEO', 'ASPRILLA', '10', '66974589'),
('CHUCHO', 'HERRERA', '78', '75698664'),
('TATA', 'HERRERA', '78', '789215'),
('JULIO', 'MESA', '78', '78925156'),
('PAOLA', 'HERRERA', '78', '789664'),
('GLORIA', 'MEDINA', '60', '8896547'),
('GINA', 'JURADO', '78', '981646'),
('FABIO', 'PLAZA', '78', '999662');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `pacientes`
--
ALTER TABLE `pacientes`
  ADD PRIMARY KEY (`identificacion`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
