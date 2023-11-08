-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: notiftkroot.mysql.db
-- Generation Time: Aug 20, 2023 at 12:25 AM
-- Server version: 5.7.42-log
-- PHP Version: 8.1.22

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `notiftkroot`
--

-- --------------------------------------------------------

--
-- Table structure for table `notiftonconcert`
--

CREATE TABLE `notiftonconcert` (
  `id` int(11) NOT NULL,
  `artist` varchar(128) NOT NULL,
  `location` varchar(256) NOT NULL,
  `email` varchar(256) NOT NULL,
  `notifsent` tinyint(1) NOT NULL,
  `end_date` date NOT NULL,
  `url` varchar(256) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `notiftonconcert`
--

INSERT INTO `notiftonconcert` (`id`, `artist`, `location`, `email`, `notifsent`, `end_date`, `url`) VALUES
(1, 'orelsan', 'Zenith Toulouse Metropole ', 'email@gmail.com', 1, '2022-11-20', 'https://www.seetickets.com/fr/ap/event/orelsan/zenith-toulouse-metropole/25087'),
(2, 'orelsan', 'Sud De France Arena ', 'email@gmail.com', 0, '2022-11-29', 'https://www.seetickets.com/fr/ap/event/orelsan/sud-de-france-arena/25077');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `notiftonconcert`
--
ALTER TABLE `notiftonconcert`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `notiftonconcert`
--
ALTER TABLE `notiftonconcert`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
