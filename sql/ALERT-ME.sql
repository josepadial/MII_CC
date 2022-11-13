-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Servidor: db
-- Tiempo de generación: 13-11-2022 a las 11:47:09
-- Versión del servidor: 8.0.31
-- Versión de PHP: 8.0.19

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `ALERT-ME`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cambios`
--

CREATE TABLE `cambios` (
  `id` int NOT NULL,
  `message` json DEFAULT NULL,
  `externalId` varchar(12) DEFAULT NULL,
  `name` varchar(1000) DEFAULT NULL,
  `plannedStartTime` varchar(100) DEFAULT NULL,
  `plannedEndTime` varchar(100) DEFAULT NULL,
  `additionalInformation` varchar(8000) DEFAULT NULL,
  `isCore` tinyint(1) DEFAULT NULL,
  `affectsAll` tinyint(1) DEFAULT NULL,
  `createdAt` varchar(100) DEFAULT NULL,
  `updatedAt` varchar(100) DEFAULT NULL,
  `MaintenanceImpacts` json DEFAULT NULL,
  `MaintenanceEvents` json DEFAULT NULL,
  `instanceKeys` varchar(500) DEFAULT NULL,
  `serviceKeys` varchar(500) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `incidencias`
--

CREATE TABLE `incidencias` (
  `id` int NOT NULL,
  `externalId` varchar(12) DEFAULT NULL,
  `message` json DEFAULT NULL,
  `additionalInformation` varchar(8000) DEFAULT NULL,
  `isCore` tinyint(1) DEFAULT NULL,
  `affectsAll` tinyint(1) DEFAULT NULL,
  `createdAt` varchar(100) DEFAULT NULL,
  `updatedAt` varchar(100) DEFAULT NULL,
  `IncidentImpacts` json DEFAULT NULL,
  `IncidentEvents` json DEFAULT NULL,
  `instanceKeys` varchar(500) DEFAULT NULL,
  `serviceKeys` varchar(500) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `cambios`
--
ALTER TABLE `cambios`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `incidencias`
--
ALTER TABLE `incidencias`
  ADD PRIMARY KEY (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
