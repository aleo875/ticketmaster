-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Versión del servidor:         8.2.0 - MySQL Community Server - GPL
-- SO del servidor:              Win64
-- HeidiSQL Versión:             12.6.0.6765
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Volcando estructura de base de datos para ticketmaster
CREATE DATABASE IF NOT EXISTS `ticketmaster` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `ticketmaster`;

-- Volcando estructura para tabla ticketmaster.eventos
CREATE TABLE IF NOT EXISTS `eventos` (
  `id_evento` int NOT NULL AUTO_INCREMENT,
  `tipo_evento` varchar(50) NOT NULL,
  `nombre_evento` varchar(100) NOT NULL,
  `ubicacion` varchar(150) NOT NULL,
  `capacidad` int NOT NULL,
  `horario` datetime NOT NULL,
  `precio` decimal(10,2) NOT NULL,
  `restricciones` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id_evento`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Volcando datos para la tabla ticketmaster.eventos: ~3 rows (aproximadamente)
INSERT INTO `eventos` (`id_evento`, `tipo_evento`, `nombre_evento`, `ubicacion`, `capacidad`, `horario`, `precio`, `restricciones`) VALUES
	(1, 'Teatro', 'El Rey León', 'Teatro Metropolitan', 500, '2023-11-20 19:00:00', 1200.00, 'Todas las edades'),
	(2, 'Cine', 'Dune 2 (IMAX)', 'Cinepolis VIP', 150, '2023-11-21 21:00:00', 180.00, 'Mayores de 12 años'),
	(3, 'Museo', 'Exposición Louvre', 'Museo de Antropología', 300, '2023-11-22 10:00:00', 400.00, 'Sin restricciones');

-- Volcando estructura para tabla ticketmaster.transacciones
CREATE TABLE IF NOT EXISTS `transacciones` (
  `id_transaccion` int NOT NULL AUTO_INCREMENT,
  `id_usuario` int DEFAULT NULL,
  `id_evento` int DEFAULT NULL,
  `cantidad_boletos` int NOT NULL,
  `metodo_pago` varchar(50) NOT NULL,
  `total_pagado` decimal(10,2) NOT NULL,
  `estado` varchar(50) DEFAULT 'Completada',
  `codigo_boleto` varchar(100) NOT NULL,
  `fecha_compra` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_transaccion`),
  UNIQUE KEY `codigo_boleto` (`codigo_boleto`),
  KEY `id_usuario` (`id_usuario`),
  KEY `id_evento` (`id_evento`),
  CONSTRAINT `transacciones_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`),
  CONSTRAINT `transacciones_ibfk_2` FOREIGN KEY (`id_evento`) REFERENCES `eventos` (`id_evento`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Volcando datos para la tabla ticketmaster.transacciones: ~2 rows (aproximadamente)
INSERT INTO `transacciones` (`id_transaccion`, `id_usuario`, `id_evento`, `cantidad_boletos`, `metodo_pago`, `total_pagado`, `estado`, `codigo_boleto`, `fecha_compra`) VALUES
	(1, 1, 1, 2, 'PayPal', 2400.00, 'Completada', '6C36571A', '2026-04-15 02:51:39'),
	(2, 1, 1, 2, 'PayPal', 2400.00, 'Completada', '7C969F9C', '2026-04-15 02:56:38');

-- Volcando estructura para tabla ticketmaster.usuarios
CREATE TABLE IF NOT EXISTS `usuarios` (
  `id_usuario` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `correo` varchar(100) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `telefono` varchar(20) NOT NULL,
  PRIMARY KEY (`id_usuario`),
  UNIQUE KEY `correo` (`correo`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Volcando datos para la tabla ticketmaster.usuarios: ~1 rows (aproximadamente)
INSERT INTO `usuarios` (`id_usuario`, `nombre`, `correo`, `password_hash`, `telefono`) VALUES
	(1, 'Leonardo Alexei Fonseca Nava', 'fonsecaalexe@gmail.com', '$2b$12$kBPJZmTi5ShYIlc4PVK7O.sqI2iFNbNDmJlU/qMXLi95Q10EiVSx2', '+5213411622206');

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
