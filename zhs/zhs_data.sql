-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 27, 2024 at 03:06 PM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `zhs_data`
--

-- --------------------------------------------------------

--
-- Table structure for table `admins`
--

CREATE TABLE `admins` (
  `id` int(5) NOT NULL,
  `username` varchar(100) NOT NULL,
  `userpassword` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `admins`
--

INSERT INTO `admins` (`id`, `username`, `userpassword`) VALUES
(1, 'admin', 'admin123');

-- --------------------------------------------------------

--
-- Table structure for table `bookings`
--

CREATE TABLE `bookings` (
  `name` varchar(200) NOT NULL,
  `email` varchar(200) NOT NULL,
  `package` varchar(200) NOT NULL,
  `price` int(200) NOT NULL,
  `deptr_date` date NOT NULL,
  `contact` varchar(255) DEFAULT NULL,
  `byuser` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `packages`
--

CREATE TABLE `packages` (
  `country` varchar(100) NOT NULL,
  `duration` int(10) NOT NULL,
  `person` int(10) NOT NULL,
  `price` int(20) NOT NULL,
  `description` varchar(400) NOT NULL,
  `image` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `packages`
--

INSERT INTO `packages` (`country`, `duration`, `person`, `price`, `description`, `image`) VALUES
('uae', 9, 1, 290000, '8 days 9 nights stay \r\ntransportation included\r\nreturn ticket \r\n4 star hotel stay\r\ncity tours', 'images/Dubai_Skylines_at_night_(Pexels_3787839).jpg'),
('Thailand', 10, 2, 450, '5 days stay in pattaya\r\n5 days stay in phuket\r\nbeach trips\r\ncity trips\r\nreturn airticket\r\nvisa included ', 'images/thailand.avif'),
('Australia', 8, 1, 340000, '4 days stay in melbourne\r\n4 days stay in sydney\r\nreturn air ticket\r\nvisa included \r\n4 star hotel stays', 'images/australia.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `tickets`
--

CREATE TABLE `tickets` (
  `name` varchar(200) NOT NULL,
  `email` varchar(200) NOT NULL,
  `package` varchar(200) NOT NULL,
  `price` int(200) NOT NULL,
  `deptr_date` date NOT NULL,
  `contact` int(200) NOT NULL,
  `byuser` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `tickets`
--

INSERT INTO `tickets` (`name`, `email`, `package`, `price`, `deptr_date`, `contact`, `byuser`) VALUES
('zafar', 'zafar@gmail.com', 'uae ', 290000, '2023-12-15', 2147483647, 'zafar'),
('hamza', 'hamza@gamil.com', 'Australia ', 340000, '2024-07-26', 3432332, 'zafar');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`name`, `email`, `password`) VALUES
('zafar', 'zafar.mahesar@gmail.com', 'zafar123'),
('zafar', 'zafar@gmail.com', 'Zafar123'),
('admin', 'admin@gmail.com', 'admin123'),
('Apple', 'hamza33@gmail.com', 'Hamza2242'),
('Pasta', 'pasta@gmail.com', 'Pasta123'),
('Ahmed', 'ahmed@gmail.com', 'Ahmed123'),
('Ali', 'ali@gmail.com', 'Ali123');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admins`
--
ALTER TABLE `admins`
  ADD PRIMARY KEY (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
