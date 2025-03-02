-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Feb 24, 2025 at 07:29 PM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.0.28

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `zhs`
--

-- --------------------------------------------------------

--
-- Table structure for table `admins`
--

CREATE TABLE `admins` (
  `id` int(11) NOT NULL,
  `username` varchar(100) NOT NULL,
  `userpassword` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `admins`
--

INSERT INTO `admins` (`id`, `username`, `userpassword`) VALUES
(1, 'admin', 'admin'),
(2, 'frk', 'frk');

-- --------------------------------------------------------

--
-- Table structure for table `airline_tickets`
--

CREATE TABLE `airline_tickets` (
  `id` int(11) NOT NULL,
  `email` varchar(255) NOT NULL,
  `airline_name` varchar(255) NOT NULL,
  `departure_location` varchar(255) NOT NULL,
  `destination_location` varchar(255) NOT NULL,
  `departure_date` datetime DEFAULT NULL,
  `return_date` datetime DEFAULT NULL,
  `ticket_price` decimal(10,2) NOT NULL,
  `ticket_class` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `bookings`
--

CREATE TABLE `bookings` (
  `id` int(11) NOT NULL,
  `byuser` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `country` varchar(100) NOT NULL,
  `travel_date` date NOT NULL,
  `members` int(11) NOT NULL,
  `days` int(11) NOT NULL,
  `price` int(20) NOT NULL,
  `hotel_type` varchar(50) NOT NULL,
  `flight_class` varchar(50) NOT NULL,
  `special_request` text DEFAULT NULL,
  `approved` int(11) NOT NULL DEFAULT 0,
  `status` enum('PENDING','USER_PAYMENT','PAID','TICKET') NOT NULL DEFAULT 'PENDING'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `bookings`
--

INSERT INTO `bookings` (`id`, `byuser`, `name`, `email`, `country`, `travel_date`, `members`, `days`, `price`, `hotel_type`, `flight_class`, `special_request`, `approved`, `status`) VALUES
(5, 'namal', 'Namal', 'namal@gmail.com', 'Thailand', '2025-02-25', 2, 10, 450, 'standard', 'economy', 'Details', 0, 'PENDING');

-- --------------------------------------------------------

--
-- Table structure for table `booking_travelers`
--

CREATE TABLE `booking_travelers` (
  `id` int(11) NOT NULL,
  `booking_id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `phone` varchar(50) NOT NULL,
  `hotel_type` varchar(50) NOT NULL,
  `flight_class` varchar(50) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `booking_travelers`
--

INSERT INTO `booking_travelers` (`id`, `booking_id`, `name`, `email`, `phone`, `hotel_type`, `flight_class`, `created_at`) VALUES
(0, 5, 'Name1', 'terst@test.com', '123456789', 'standard', 'economy', '2025-02-24 15:19:53');

-- --------------------------------------------------------

--
-- Table structure for table `cancelled_bookings`
--

CREATE TABLE `cancelled_bookings` (
  `id` int(11) NOT NULL,
  `byuser` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `country` varchar(100) NOT NULL,
  `travel_date` date NOT NULL,
  `members` int(11) NOT NULL,
  `days` int(11) NOT NULL,
  `hotel_type` varchar(50) NOT NULL,
  `flight_class` varchar(50) NOT NULL,
  `special_request` text DEFAULT NULL,
  `reason` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `cancelled_bookings`
--

INSERT INTO `cancelled_bookings` (`id`, `byuser`, `name`, `email`, `country`, `travel_date`, `members`, `days`, `hotel_type`, `flight_class`, `special_request`, `reason`) VALUES
(1, 'namal', 'Namal', 'namal@gmail.com', 'London', '2024-12-25', 5, 2, 'standard', 'economy', 'Call for seats', 'Sample reason'),
(2, 'namal', 'Namal', 'namal@gmail.com', 'London', '2024-12-25', 5, 2, 'standard', 'economy', 'Call for seats', 'Sample reason'),
(4, 'namal', 'Namal', 'namal@gmail.com', 'London', '2024-12-25', 5, 2, 'standard', 'economy', 'Call for seats', 'This is Prado 2');

-- --------------------------------------------------------

--
-- Table structure for table `custom_tours`
--

CREATE TABLE `custom_tours` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `address` text NOT NULL,
  `details` text NOT NULL,
  `status` enum('PENDING','CONFIRMED','CANCELLED','REJECTED') NOT NULL DEFAULT 'PENDING',
  `status_reason` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `custom_tours`
--

INSERT INTO `custom_tours` (`id`, `name`, `email`, `address`, `details`, `status`, `status_reason`, `created_at`) VALUES
(1, 'Booker', 'namal@gmail.com', 'Booker Address', 'Itinerary detail', 'CONFIRMED', NULL, '2025-02-23 14:38:25');

-- --------------------------------------------------------

--
-- Table structure for table `flights`
--

CREATE TABLE `flights` (
  `id` int(11) NOT NULL,
  `email` varchar(150) NOT NULL,
  `ticket_type` enum('one-way','return') NOT NULL,
  `departure_city` varchar(255) NOT NULL,
  `destination_city` varchar(255) NOT NULL,
  `departure_date` date NOT NULL,
  `return_date` date DEFAULT NULL,
  `flight_class` enum('economy','business','first-class') NOT NULL,
  `status` enum('PENDING','USER_PAYMENT','PAID','TICKET') NOT NULL DEFAULT 'PENDING',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `flights`
--

INSERT INTO `flights` (`id`, `email`, `ticket_type`, `departure_city`, `destination_city`, `departure_date`, `return_date`, `flight_class`, `status`, `created_at`) VALUES
(1, 'namal@gmail.com', 'one-way', 'Test', 'Test', '2025-02-25', NULL, 'economy', 'PENDING', '2025-02-24 10:10:36'),
(4, 'namal@gmail.com', 'one-way', 'Test', 'Test', '2025-02-25', NULL, 'economy', 'USER_PAYMENT', '2025-02-24 11:52:02'),
(5, 'namal@gmail.com', 'one-way', 'Test', 'Test', '2025-02-24', NULL, 'economy', 'PAID', '2025-02-24 11:58:54'),
(6, 'namal@gmail.com', 'one-way', 'test', 'Test', '2025-02-26', NULL, 'economy', 'TICKET', '2025-02-24 11:59:54');

-- --------------------------------------------------------

--
-- Table structure for table `flight_passengers`
--

CREATE TABLE `flight_passengers` (
  `id` int(11) NOT NULL,
  `flight_id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `contact` varchar(50) NOT NULL,
  `email` varchar(255) NOT NULL,
  `passport_number` varchar(50) NOT NULL,
  `passport_country` varchar(100) NOT NULL,
  `passport_issue` date NOT NULL,
  `passport_picture` varchar(255) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `flight_passengers`
--

INSERT INTO `flight_passengers` (`id`, `flight_id`, `name`, `contact`, `email`, `passport_number`, `passport_country`, `passport_issue`, `passport_picture`, `created_at`) VALUES
(1, 1, 'Test Name', '123456789', 'namal@gmail.com', '123456789', 'Pakistan', '2024-01-24', NULL, '2025-02-24 10:10:36'),
(2, 4, 'Test Name', '123456789', 'namal@gmail.com', '123456789', 'Pakistan', '2024-01-24', NULL, '2025-02-24 11:52:02'),
(3, 5, 'test', '1234589684', 'test@test.com', '15496451', 'Test', '2025-02-03', NULL, '2025-02-24 11:58:54'),
(4, 6, 'Test', 'Test', 'test@test.com', '15496451', 'Pakistan', '2025-02-04', NULL, '2025-02-24 11:59:54');

-- --------------------------------------------------------

--
-- Table structure for table `hotels`
--

CREATE TABLE `hotels` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `location` varchar(255) NOT NULL,
  `rating` varchar(50) NOT NULL,
  `room_types` varchar(255) NOT NULL,
  `price_per_night` decimal(10,2) NOT NULL,
  `description` text NOT NULL,
  `image` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `hotels`
--

INSERT INTO `hotels` (`id`, `name`, `location`, `rating`, `room_types`, `price_per_night`, `description`, `image`) VALUES
(1, 'Baku Hilton', 'Baku', '4', 'Double', 2000.00, 'An awesome room', 'uploads/baku-hilton-484075122_1733279321.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `packages`
--

CREATE TABLE `packages` (
  `id` int(11) NOT NULL,
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

INSERT INTO `packages` (`id`, `country`, `duration`, `person`, `price`, `description`, `image`) VALUES
(1, 'UAE', 9, 1, 290000, '8 days 9 nights stay \ntransportation included\nreturn ticket \n4 star hotel stay\ncity tours', 'images/dubai.jpg'),
(2, 'Thailand', 10, 2, 450, '5 days stay in pattaya\r\n5 days stay in phuket\r\nbeach trips\r\ncity trips\r\nreturn airticket\r\nvisa included ', 'images/Thailand_image.jpg'),
(3, 'Australia', 8, 1, 340000, '4 days stay in melbourne\r\n4 days stay in sydney\r\nreturn air ticket\r\nvisa included \r\n4 star hotel stays', 'images/australia.jpg'),
(9, 'Baku', 5, 5, 500, 'Testing Baku travel', 'images/baku-travel_1733284626.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `payments`
--

CREATE TABLE `payments` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `booking_id` int(11) NOT NULL,
  `booking_for` enum('HOTEL','FLIGHT') NOT NULL DEFAULT 'HOTEL',
  `payment_amount` varchar(50) NOT NULL,
  `payment_method` varchar(50) NOT NULL,
  `payment_status` enum('PENDING','COMPLETED','REFUNDED') NOT NULL DEFAULT 'PENDING',
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `payments`
--

INSERT INTO `payments` (`id`, `user_id`, `booking_id`, `booking_for`, `payment_amount`, `payment_method`, `payment_status`, `timestamp`) VALUES
(1, 2, 3, 'HOTEL', '600', 'CREDIT', 'PENDING', '2025-02-24 14:37:15');

-- --------------------------------------------------------

--
-- Table structure for table `tickets`
--

CREATE TABLE `tickets` (
  `id` int(11) NOT NULL,
  `name` varchar(200) NOT NULL,
  `email` varchar(200) NOT NULL,
  `package` varchar(200) NOT NULL,
  `price` int(200) NOT NULL,
  `deptr_date` date NOT NULL,
  `contact` varchar(255) NOT NULL,
  `byuser` varchar(200) NOT NULL,
  `approved` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `tickets`
--

INSERT INTO `tickets` (`id`, `name`, `email`, `package`, `price`, `deptr_date`, `contact`, `byuser`, `approved`) VALUES
(1, 'namal', 'namal@gmail.com', 'UAE', 450, '2024-12-12', 'namal@gmail.com', 'namal', 0),
(2, 'frk', 'frk@gmail.com', 'Thailand', 800, '2024-12-14', 'frk@gmail.com', 'frk', 0);

-- --------------------------------------------------------

--
-- Table structure for table `tour_destinations`
--

CREATE TABLE `tour_destinations` (
  `id` int(11) NOT NULL,
  `tour_id` int(11) NOT NULL,
  `country` varchar(255) NOT NULL,
  `start_date` date NOT NULL,
  `end_date` date NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tour_destinations`
--

INSERT INTO `tour_destinations` (`id`, `tour_id`, `country`, `start_date`, `end_date`, `created_at`) VALUES
(1, 1, 'Baku', '2025-02-24', '2025-02-26', '2025-02-23 14:38:25'),
(2, 1, 'Thailand', '2025-02-27', '2025-02-28', '2025-02-23 14:38:25');

-- --------------------------------------------------------

--
-- Table structure for table `tour_travelers`
--

CREATE TABLE `tour_travelers` (
  `id` int(11) NOT NULL,
  `tour_id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `phone` varchar(50) NOT NULL,
  `hotel_type` varchar(50) NOT NULL,
  `flight_class` varchar(50) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tour_travelers`
--

INSERT INTO `tour_travelers` (`id`, `tour_id`, `name`, `email`, `phone`, `hotel_type`, `flight_class`, `created_at`) VALUES
(1, 1, 'Test', 'namal@gmail.com', '123456789', 'standard', 'economy', '2025-02-23 14:38:25');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  `logged_in` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `name`, `email`, `password`, `logged_in`) VALUES
(1, 'namal', 'namal@gmail.com', 'namal', '2025-02-16 15:35:53'),
(2, 'frk', 'frk@gmail.com', 'frk', '2025-02-16 15:35:53');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admins`
--
ALTER TABLE `admins`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `airline_tickets`
--
ALTER TABLE `airline_tickets`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `bookings`
--
ALTER TABLE `bookings`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `booking_travelers`
--
ALTER TABLE `booking_travelers`
  ADD KEY `bookings_booking_travelers_foreign_key` (`booking_id`);

--
-- Indexes for table `cancelled_bookings`
--
ALTER TABLE `cancelled_bookings`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `custom_tours`
--
ALTER TABLE `custom_tours`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `flights`
--
ALTER TABLE `flights`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `flight_passengers`
--
ALTER TABLE `flight_passengers`
  ADD PRIMARY KEY (`id`),
  ADD KEY `flight_passenger_on_flights_foreign_key` (`flight_id`);

--
-- Indexes for table `hotels`
--
ALTER TABLE `hotels`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `packages`
--
ALTER TABLE `packages`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `payments`
--
ALTER TABLE `payments`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tickets`
--
ALTER TABLE `tickets`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tour_destinations`
--
ALTER TABLE `tour_destinations`
  ADD PRIMARY KEY (`id`),
  ADD KEY `tour_destinations_custom_tours_foreign_key` (`tour_id`);

--
-- Indexes for table `tour_travelers`
--
ALTER TABLE `tour_travelers`
  ADD PRIMARY KEY (`id`),
  ADD KEY `custom_tours_foreign_key` (`tour_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admins`
--
ALTER TABLE `admins`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `airline_tickets`
--
ALTER TABLE `airline_tickets`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `bookings`
--
ALTER TABLE `bookings`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `cancelled_bookings`
--
ALTER TABLE `cancelled_bookings`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `custom_tours`
--
ALTER TABLE `custom_tours`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `flights`
--
ALTER TABLE `flights`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `flight_passengers`
--
ALTER TABLE `flight_passengers`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `hotels`
--
ALTER TABLE `hotels`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `packages`
--
ALTER TABLE `packages`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `payments`
--
ALTER TABLE `payments`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `tickets`
--
ALTER TABLE `tickets`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `tour_destinations`
--
ALTER TABLE `tour_destinations`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `tour_travelers`
--
ALTER TABLE `tour_travelers`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `booking_travelers`
--
ALTER TABLE `booking_travelers`
  ADD CONSTRAINT `bookings_booking_travelers_foreign_key` FOREIGN KEY (`booking_id`) REFERENCES `bookings` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `flight_passengers`
--
ALTER TABLE `flight_passengers`
  ADD CONSTRAINT `flight_passenger_on_flights_foreign_key` FOREIGN KEY (`flight_id`) REFERENCES `flights` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `tour_destinations`
--
ALTER TABLE `tour_destinations`
  ADD CONSTRAINT `tour_destinations_custom_tours_foreign_key` FOREIGN KEY (`tour_id`) REFERENCES `custom_tours` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `tour_travelers`
--
ALTER TABLE `tour_travelers`
  ADD CONSTRAINT `custom_tours_foreign_key` FOREIGN KEY (`tour_id`) REFERENCES `custom_tours` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
