-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 05-06-2024 a las 12:16:27
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
-- Estructura de tabla para la tabla `medicos`
--

CREATE TABLE `medicos` (
  `nombre` varchar(50) NOT NULL,
  `apellido` varchar(50) NOT NULL,
  `edad` int(3) NOT NULL,
  `num_registro` int(20) NOT NULL,
  `especialidad` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `medicos`
--

INSERT INTO `medicos` (`nombre`, `apellido`, `edad`, `num_registro`, `especialidad`) VALUES
('JOSE ALBERTO', 'HURTADO VARGAS', 54, 1010, 'NEUROLOGIA'),
('ANDRES ', 'MARQUEZ ESCOBAR', 32, 8080, 'OTORRINOLARINGOLOGO'),
('MARIA', 'VARGAS CONTRERAS', 28, 2324, 'CARDIOLOGIA'),
('CATALINA', 'SANCHEZ VALVUENA', 22, 1090, 'NUTRICION');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pacientes`
--

CREATE TABLE `pacientes` (
  `nombre` varchar(50) NOT NULL,
  `apellido` varchar(50) NOT NULL,
  `edad` varchar(3) NOT NULL,
  `identificacion` varchar(20) NOT NULL,
  `med_cabecera` varchar(255) NOT NULL,
  `url` varchar(10000) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `pacientes`
--

INSERT INTO `pacientes` (`nombre`, `apellido`, `edad`, `identificacion`, `med_cabecera`, `url`) VALUES
('MICHAEL', 'SALAZAR', '21', '1001456812', '', ''),
('ESTEBAN', 'ARTUNDUAGA', '22', '123', '', ''),
('LIONEL ANDRES', 'MESSI', '34', '10', '', ''),
('JOSUE', 'PANIAGUA', '21', '789', '', ''),
('MICHAEL DAVID', 'SALAZAR', '23', '9090', '', ''),
('PUEDE', 'SER', '45', '456788', '', ''),
('', '', '', '', '', ''),
('HOLLA', 'SALUD', '34', '0880', '', '');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
