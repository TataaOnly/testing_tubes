-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 06, 2026 at 10:43 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `simrs`
--

-- --------------------------------------------------------

--
-- Table structure for table `appointments`
--

CREATE TABLE `appointments` (
  `id_appointment` int(11) NOT NULL,
  `id_patient` int(11) NOT NULL,
  `id_doctor` int(11) NOT NULL,
  `jadwal` datetime NOT NULL,
  `status_antrean` enum('Menunggu','Selesai','Batal') DEFAULT 'Menunggu'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `appointments`
--

INSERT INTO `appointments` (`id_appointment`, `id_patient`, `id_doctor`, `jadwal`, `status_antrean`) VALUES
(1, 1, 1, '2026-05-06 21:27:38', 'Selesai'),
(2, 2, 2, '2026-05-06 21:38:03', 'Selesai'),
(3, 3, 3, '2026-05-06 21:38:03', 'Selesai'),
(4, 1, 2, '2026-05-06 21:38:03', 'Batal'),
(5, 4, 2, '2022-02-02 12:30:00', 'Menunggu'),
(6, 12, 2, '2005-04-03 12:12:00', 'Menunggu');

-- --------------------------------------------------------

--
-- Table structure for table `doctors`
--

CREATE TABLE `doctors` (
  `id_doctor` int(11) NOT NULL,
  `nama_dokter` varchar(100) NOT NULL,
  `spesialisasi` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `doctors`
--

INSERT INTO `doctors` (`id_doctor`, `nama_dokter`, `spesialisasi`) VALUES
(1, 'Dr. Adhyo', 'Spesialis Jantung'),
(2, 'Dr. Sarah', 'Spesialis Penyakit Dalam'),
(3, 'Dr. Budi', 'Spesialis Anak');

-- --------------------------------------------------------

--
-- Table structure for table `invoices`
--

CREATE TABLE `invoices` (
  `id_invoice` int(11) NOT NULL,
  `id_patient` int(11) NOT NULL,
  `id_appointment` int(11) NOT NULL,
  `grand_total` decimal(15,2) DEFAULT 0.00,
  `tgl_tagihan` timestamp NOT NULL DEFAULT current_timestamp(),
  `status_bayar` enum('Belum Bayar','Lunas') DEFAULT 'Belum Bayar'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `invoices`
--

INSERT INTO `invoices` (`id_invoice`, `id_patient`, `id_appointment`, `grand_total`, `tgl_tagihan`, `status_bayar`) VALUES
(1, 1, 1, 1550000.00, '2026-05-06 14:28:21', 'Belum Bayar'),
(2, 1, 1, 1550000.00, '2026-05-06 14:49:33', 'Belum Bayar'),
(3, 2, 2, 0.00, '2026-05-06 14:49:33', 'Belum Bayar'),
(4, 1, 1, 1550000.00, '2026-05-06 15:13:46', 'Belum Bayar'),
(5, 2, 2, 0.00, '2026-05-06 15:14:12', 'Belum Bayar'),
(6, 1, 1, 1550000.00, '2026-05-06 15:26:23', 'Belum Bayar'),
(7, 2, 2, 0.00, '2026-05-06 15:26:35', 'Belum Bayar'),
(8, 1, 1, 1550000.00, '2026-05-06 18:17:15', 'Belum Bayar'),
(9, 1, 1, 1550000.00, '2026-05-06 19:05:31', 'Belum Bayar'),
(10, 4, 5, 1500000.00, '2026-05-06 19:32:49', 'Lunas'),
(11, 1, 1, 1550000.00, '2026-05-06 20:08:07', 'Belum Bayar'),
(12, 1, 1, 1550000.00, '2026-05-06 20:09:36', 'Belum Bayar'),
(13, 1, 1, 1550000.00, '2026-05-06 20:11:10', 'Belum Bayar'),
(14, 1, 1, 1550000.00, '2026-05-06 20:21:02', 'Belum Bayar'),
(15, 1, 1, 1550000.00, '2026-05-06 20:27:11', 'Belum Bayar'),
(16, 12, 6, 1500000.00, '2026-05-06 20:31:57', 'Lunas'),
(17, 1, 1, 1550000.00, '2026-05-06 20:38:22', 'Belum Bayar'),
(18, 1, 1, 1550000.00, '2026-05-06 20:41:33', 'Belum Bayar');

-- --------------------------------------------------------

--
-- Table structure for table `invoice_items`
--

CREATE TABLE `invoice_items` (
  `id_item` int(11) NOT NULL,
  `id_invoice` int(11) NOT NULL,
  `item_name` varchar(100) NOT NULL,
  `qty` int(11) NOT NULL,
  `harga_satuan` decimal(12,2) NOT NULL,
  `subtotal` decimal(15,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `invoice_items`
--

INSERT INTO `invoice_items` (`id_item`, `id_invoice`, `item_name`, `qty`, `harga_satuan`, `subtotal`) VALUES
(1, 1, 'Kamar VIP', 1, 1500000.00, 1500000.00),
(2, 1, 'Amoxicillin', 2, 25000.00, 50000.00),
(3, 2, 'Kamar VIP', 1, 1500000.00, 1500000.00),
(4, 2, 'Amoxicillin', 2, 25000.00, 50000.00),
(5, 3, 'Kamar VIP', 1, 1500000.00, 1500000.00),
(6, 3, 'Ibuprofen', 1, 15000.00, 15000.00),
(7, 3, 'Vitamin C', 10, 5000.00, 50000.00),
(8, 4, 'Kamar VIP', 1, 1500000.00, 1500000.00),
(9, 4, 'Amoxicillin', 2, 25000.00, 50000.00),
(10, 5, 'Kamar VIP', 1, 1500000.00, 1500000.00),
(11, 5, 'Ibuprofen', 1, 15000.00, 15000.00),
(12, 5, 'Vitamin C', 10, 5000.00, 50000.00),
(13, 6, 'Kamar VIP', 1, 1500000.00, 1500000.00),
(14, 6, 'Amoxicillin', 2, 25000.00, 50000.00),
(15, 7, 'Kamar VIP', 1, 1500000.00, 1500000.00),
(16, 7, 'Ibuprofen', 1, 15000.00, 15000.00),
(17, 7, 'Vitamin C', 10, 5000.00, 50000.00),
(18, 8, 'Kamar VIP', 1, 1500000.00, 1500000.00),
(19, 8, 'Amoxicillin', 2, 25000.00, 50000.00),
(20, 9, 'Kamar VIP', 1, 1500000.00, 1500000.00),
(21, 9, 'Amoxicillin', 2, 25000.00, 50000.00),
(22, 10, 'Kamar VIP', 1, 1500000.00, 1500000.00),
(23, 11, 'Kamar VIP', 1, 1500000.00, 1500000.00),
(24, 11, 'Amoxicillin', 2, 25000.00, 50000.00),
(25, 12, 'Kamar VIP', 1, 1500000.00, 1500000.00),
(26, 12, 'Amoxicillin', 2, 25000.00, 50000.00),
(27, 13, 'Kamar VIP', 1, 1500000.00, 1500000.00),
(28, 13, 'Amoxicillin', 2, 25000.00, 50000.00),
(29, 14, 'Kamar VIP', 1, 1500000.00, 1500000.00),
(30, 14, 'Amoxicillin', 2, 25000.00, 50000.00),
(31, 15, 'Kamar VIP', 1, 1500000.00, 1500000.00),
(32, 15, 'Amoxicillin', 2, 25000.00, 50000.00),
(33, 16, 'Kamar VIP', 1, 1500000.00, 1500000.00),
(34, 17, 'Kamar VIP', 1, 1500000.00, 1500000.00),
(35, 17, 'Amoxicillin', 2, 25000.00, 50000.00),
(36, 18, 'Kamar VIP', 1, 1500000.00, 1500000.00),
(37, 18, 'Amoxicillin', 2, 25000.00, 50000.00);

-- --------------------------------------------------------

--
-- Table structure for table `medical_records`
--

CREATE TABLE `medical_records` (
  `id_record` int(11) NOT NULL,
  `id_patient` int(11) NOT NULL,
  `id_doctor` int(11) NOT NULL,
  `id_appointment` int(11) NOT NULL,
  `diagnosa` text DEFAULT NULL,
  `tindakan` text DEFAULT NULL,
  `tgl_periksa` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `medical_records`
--

INSERT INTO `medical_records` (`id_record`, `id_patient`, `id_doctor`, `id_appointment`, `diagnosa`, `tindakan`, `tgl_periksa`) VALUES
(1, 1, 1, 1, 'Gejala Kelelahan', 'Rawat Inap', '2026-05-06 14:27:38'),
(2, 2, 2, 2, 'Flu Berat', 'Rawat Inap Standar', '2026-05-06 14:38:03'),
(3, 3, 3, 3, 'Pemeriksaan Rutin', 'Rawat Jalan', '2026-05-06 14:38:03'),
(4, 4, 2, 5, 'Sakit Jiwa', 'Terapi', '2026-05-06 19:31:21'),
(5, 1, 1, 1, 'Flu', 'Istirahat', '2026-05-06 20:01:21'),
(6, 1, 1, 1, 'Flu', 'Istirahat', '2026-05-06 20:03:09'),
(7, 1, 1, 1, 'Flu', 'Istirahat', '2026-05-06 20:08:07'),
(8, 1, 1, 1, 'Flu', 'Istirahat', '2026-05-06 20:09:36'),
(9, 1, 1, 1, 'Flu', 'Istirahat', '2026-05-06 20:11:10'),
(10, 1, 1, 1, 'Flu', 'Istirahat', '2026-05-06 20:21:02'),
(11, 1, 1, 1, 'Flu', 'Istirahat', '2026-05-06 20:27:11'),
(13, 12, 1, 6, 'Sakit Jiwa', 'Terapi', '2026-05-06 20:30:54');

-- --------------------------------------------------------

--
-- Table structure for table `medicines`
--

CREATE TABLE `medicines` (
  `id_obat` int(11) NOT NULL,
  `nama_obat` varchar(100) NOT NULL,
  `stok` int(11) DEFAULT 0,
  `harga` decimal(12,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `medicines`
--

INSERT INTO `medicines` (`id_obat`, `nama_obat`, `stok`, `harga`) VALUES
(1, 'Amoxicillin', 100, 25000.00),
(2, 'Paracetamol', 200, 10000.00),
(3, 'Ibuprofen', 50, 15000.00),
(4, 'Vitamin C', 150, 5000.00),
(5, 'Sirup Batuk', 30, 35000.00),
(6, '', 0, 0.00);

-- --------------------------------------------------------

--
-- Table structure for table `patients`
--

CREATE TABLE `patients` (
  `id_patient` int(11) NOT NULL,
  `nik` char(16) NOT NULL,
  `nama` varchar(100) NOT NULL,
  `alamat` text DEFAULT NULL,
  `tgl_lahir` date DEFAULT NULL,
  `jenis_pembayaran` enum('Umum','BPJS','Asuransi Swasta') DEFAULT 'Umum',
  `nomor_asuransi` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `patients`
--

INSERT INTO `patients` (`id_patient`, `nik`, `nama`, `alamat`, `tgl_lahir`, `jenis_pembayaran`, `nomor_asuransi`) VALUES
(1, '3273000000000001', 'Prabhaseta', 'Bandung', '2004-01-01', 'Umum', NULL),
(2, '3273000000000002', 'Budi Santoso', 'Sleman', '1995-05-10', 'BPJS', '000123456789'),
(3, '3273000000000003', 'Siti Aminah', 'Bantul', '1988-11-22', 'Umum', NULL),
(4, '3273000000000223', 'Prabhaseta', 'Bandung', '2001-03-03', 'Umum', NULL),
(5, '1234567890', 'Test Patient', '123 Test St', '2000-01-01', 'Umum', NULL),
(12, '3273000000000224', 'kuso', 'Bandung', '2002-02-02', 'Umum', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `prescriptions`
--

CREATE TABLE `prescriptions` (
  `id_prescription` int(11) NOT NULL,
  `id_record` int(11) NOT NULL,
  `id_obat` int(11) NOT NULL,
  `jumlah` int(11) NOT NULL,
  `status_diambil` tinyint(1) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `prescriptions`
--

INSERT INTO `prescriptions` (`id_prescription`, `id_record`, `id_obat`, `jumlah`, `status_diambil`) VALUES
(1, 1, 1, 2, 1),
(2, 2, 3, 1, 1),
(3, 2, 4, 10, 1),
(4, 4, 1, 2, 0),
(5, 13, 3, 1, 0);

-- --------------------------------------------------------

--
-- Table structure for table `rooms`
--

CREATE TABLE `rooms` (
  `id_kamar` int(11) NOT NULL,
  `tipe_kamar` enum('VIP','Standar') NOT NULL,
  `status_tersedia` tinyint(1) DEFAULT 1,
  `tarif_per_malam` decimal(12,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `rooms`
--

INSERT INTO `rooms` (`id_kamar`, `tipe_kamar`, `status_tersedia`, `tarif_per_malam`) VALUES
(1, 'VIP', 1, 1500000.00),
(2, 'Standar', 1, 500000.00);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id_user` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` enum('Admin','Dokter','Apoteker','Resepsionis','Kasir') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id_user`, `username`, `password`, `role`) VALUES
(1, 'admin_simrs', 'password123', 'Admin'),
(2, 'new_user', 'password123', 'Kasir'),
(3, 'doc1', 'test1', 'Dokter'),
(4, 'Kas1', 'kas1', 'Dokter'),
(5, 'testuser', 'password', 'Admin');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `appointments`
--
ALTER TABLE `appointments`
  ADD PRIMARY KEY (`id_appointment`),
  ADD KEY `id_patient` (`id_patient`),
  ADD KEY `id_doctor` (`id_doctor`);

--
-- Indexes for table `doctors`
--
ALTER TABLE `doctors`
  ADD PRIMARY KEY (`id_doctor`);

--
-- Indexes for table `invoices`
--
ALTER TABLE `invoices`
  ADD PRIMARY KEY (`id_invoice`),
  ADD KEY `id_patient` (`id_patient`),
  ADD KEY `id_appointment` (`id_appointment`);

--
-- Indexes for table `invoice_items`
--
ALTER TABLE `invoice_items`
  ADD PRIMARY KEY (`id_item`),
  ADD KEY `id_invoice` (`id_invoice`);

--
-- Indexes for table `medical_records`
--
ALTER TABLE `medical_records`
  ADD PRIMARY KEY (`id_record`),
  ADD KEY `id_patient` (`id_patient`),
  ADD KEY `id_doctor` (`id_doctor`),
  ADD KEY `id_appointment` (`id_appointment`);

--
-- Indexes for table `medicines`
--
ALTER TABLE `medicines`
  ADD PRIMARY KEY (`id_obat`);

--
-- Indexes for table `patients`
--
ALTER TABLE `patients`
  ADD PRIMARY KEY (`id_patient`),
  ADD UNIQUE KEY `nik` (`nik`);

--
-- Indexes for table `prescriptions`
--
ALTER TABLE `prescriptions`
  ADD PRIMARY KEY (`id_prescription`),
  ADD KEY `id_record` (`id_record`),
  ADD KEY `id_obat` (`id_obat`);

--
-- Indexes for table `rooms`
--
ALTER TABLE `rooms`
  ADD PRIMARY KEY (`id_kamar`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id_user`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `appointments`
--
ALTER TABLE `appointments`
  MODIFY `id_appointment` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `doctors`
--
ALTER TABLE `doctors`
  MODIFY `id_doctor` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `invoices`
--
ALTER TABLE `invoices`
  MODIFY `id_invoice` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- AUTO_INCREMENT for table `invoice_items`
--
ALTER TABLE `invoice_items`
  MODIFY `id_item` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=38;

--
-- AUTO_INCREMENT for table `medical_records`
--
ALTER TABLE `medical_records`
  MODIFY `id_record` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT for table `medicines`
--
ALTER TABLE `medicines`
  MODIFY `id_obat` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `patients`
--
ALTER TABLE `patients`
  MODIFY `id_patient` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `prescriptions`
--
ALTER TABLE `prescriptions`
  MODIFY `id_prescription` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `rooms`
--
ALTER TABLE `rooms`
  MODIFY `id_kamar` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id_user` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `appointments`
--
ALTER TABLE `appointments`
  ADD CONSTRAINT `appointments_ibfk_1` FOREIGN KEY (`id_patient`) REFERENCES `patients` (`id_patient`),
  ADD CONSTRAINT `appointments_ibfk_2` FOREIGN KEY (`id_doctor`) REFERENCES `doctors` (`id_doctor`);

--
-- Constraints for table `invoices`
--
ALTER TABLE `invoices`
  ADD CONSTRAINT `invoices_ibfk_1` FOREIGN KEY (`id_patient`) REFERENCES `patients` (`id_patient`),
  ADD CONSTRAINT `invoices_ibfk_2` FOREIGN KEY (`id_appointment`) REFERENCES `appointments` (`id_appointment`);

--
-- Constraints for table `invoice_items`
--
ALTER TABLE `invoice_items`
  ADD CONSTRAINT `invoice_items_ibfk_1` FOREIGN KEY (`id_invoice`) REFERENCES `invoices` (`id_invoice`);

--
-- Constraints for table `medical_records`
--
ALTER TABLE `medical_records`
  ADD CONSTRAINT `medical_records_ibfk_1` FOREIGN KEY (`id_patient`) REFERENCES `patients` (`id_patient`),
  ADD CONSTRAINT `medical_records_ibfk_2` FOREIGN KEY (`id_doctor`) REFERENCES `doctors` (`id_doctor`),
  ADD CONSTRAINT `medical_records_ibfk_3` FOREIGN KEY (`id_appointment`) REFERENCES `appointments` (`id_appointment`);

--
-- Constraints for table `prescriptions`
--
ALTER TABLE `prescriptions`
  ADD CONSTRAINT `prescriptions_ibfk_1` FOREIGN KEY (`id_record`) REFERENCES `medical_records` (`id_record`),
  ADD CONSTRAINT `prescriptions_ibfk_2` FOREIGN KEY (`id_obat`) REFERENCES `medicines` (`id_obat`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
