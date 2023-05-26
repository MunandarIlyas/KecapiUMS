-- phpMyAdmin SQL Dump
-- version 4.2.11
-- http://www.phpmyadmin.net
--
-- Host: 127.0.0.1
-- Generation Time: 10 Mar 2023 pada 17.07
-- Versi Server: 5.6.21
-- PHP Version: 5.6.3

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `kukuis`
--

-- --------------------------------------------------------

--
-- Struktur dari tabel `jawaban_peserta`
--

CREATE TABLE IF NOT EXISTS `jawaban_peserta` (
`id_jawaban` int(3) NOT NULL,
  `id_peserta` int(3) NOT NULL,
  `id_sesi` int(3) NOT NULL,
  `id_soal` int(3) NOT NULL,
  `jawaban` char(1) DEFAULT NULL,
  `waktu` int(4) DEFAULT '0',
  `score` decimal(4,3) NOT NULL DEFAULT '0.000',
  `status` int(1) NOT NULL DEFAULT '0'
) ENGINE=InnoDB AUTO_INCREMENT=270 DEFAULT CHARSET=latin1;

--
-- Dumping data untuk tabel `jawaban_peserta`
--

INSERT INTO `jawaban_peserta` (`id_jawaban`, `id_peserta`, `id_sesi`, `id_soal`, `jawaban`, `waktu`, `score`, `status`) VALUES
(226, 70, 1017, 5, 'D', 4, '0.933', 0),
(227, 69, 1017, 5, 'D', 5, '0.917', 0),
(228, 69, 1017, 6, 'B', 5, '0.917', 0),
(229, 70, 1017, 6, 'B', 9, '0.850', 0),
(230, 69, 1017, 7, 'C', 6, '0.900', 0),
(231, 70, 1017, 7, 'C', 6, '0.900', 0),
(232, 69, 1017, 10, 'A', 4, '0.933', 0),
(233, 70, 1017, 10, 'A', 4, '0.933', 0),
(234, 69, 1017, 11, 'A', 4, '0.933', 0),
(235, 70, 1017, 11, 'B', 4, '0.000', 0),
(236, 69, 1017, 13, 'D', 6, '0.900', 0),
(237, 70, 1017, 13, 'D', 7, '0.883', 0),
(238, 71, 1041, 5, 'A', 4, '0.000', 1),
(239, 71, 1041, 6, 'B', 6, '0.900', 1),
(240, 71, 1041, 7, 'D', 3, '0.000', 0),
(241, 71, 1041, 10, 'A', 2, '0.967', 1),
(242, 71, 1041, 11, 'A', 2, '0.967', 0),
(243, 71, 1041, 13, 'D', 5, '0.917', 0),
(244, 79, 1042, 5, 'A', 4, '0.000', 0),
(245, 79, 1041, 5, 'C', 59, '0.000', 1),
(246, 80, 1042, 5, 'C', 9, '0.000', 0),
(247, 80, 1042, 6, 'B', 5, '0.917', 1),
(248, 80, 1042, 7, 'C', 7, '0.883', 1),
(249, 80, 1042, 10, 'A', 2, '0.967', 1),
(250, 80, 1042, 11, 'A', 7, '0.883', 1),
(251, 80, 1042, 13, 'D', 3, '0.950', 1),
(252, 81, 1043, 5, 'D', 14, '0.767', 1),
(253, 81, 1043, 6, 'D', 58, '0.000', 0),
(254, 81, 1043, 7, 'C', 30, '0.500', 1),
(255, 81, 1043, 10, 'A', 6, '0.900', 1),
(256, 81, 1043, 11, 'A', 2, '0.967', 1),
(257, 81, 1043, 13, 'D', 2, '0.967', 1),
(258, 82, 1043, 5, 'C', 9, '0.000', 0),
(259, 82, 1043, 6, 'B', 8, '0.867', 1),
(260, 82, 1043, 7, 'C', 16, '0.733', 1),
(261, 82, 1043, 10, 'A', 3, '0.950', 1),
(262, 82, 1043, 11, 'A', 2, '0.967', 1),
(263, 82, 1043, 13, 'D', 4, '0.933', 1),
(264, 83, 1043, 5, 'D', 25, '0.583', 1),
(265, 83, 1043, 6, 'D', 2, '0.000', 0),
(266, 83, 1043, 7, 'B', 3, '0.000', 0),
(267, 83, 1043, 10, 'A', 1, '0.983', 1),
(268, 83, 1043, 11, 'C', 2, '0.000', 0),
(269, 83, 1043, 13, 'D', 5, '0.917', 1);

-- --------------------------------------------------------

--
-- Struktur dari tabel `peserta_kuis`
--

CREATE TABLE IF NOT EXISTS `peserta_kuis` (
`id_peserta` int(3) NOT NULL,
  `nama_peserta` varchar(25) NOT NULL,
  `id_sesi` int(4) NOT NULL,
  `id_status` int(1) NOT NULL DEFAULT '1',
  `score_akhir` decimal(5,3) NOT NULL DEFAULT '0.000'
) ENGINE=InnoDB AUTO_INCREMENT=84 DEFAULT CHARSET=latin1;

--
-- Dumping data untuk tabel `peserta_kuis`
--

INSERT INTO `peserta_kuis` (`id_peserta`, `nama_peserta`, `id_sesi`, `id_status`, `score_akhir`) VALUES
(69, 'PC Ilyas Munandar', 1017, 2, '5.500'),
(70, 'Mibile Ilyas Munandar', 1017, 2, '4.499'),
(71, 'User', 1041, 2, '3.751'),
(78, 'ilyas', 1041, 2, '0.000'),
(80, 'Munandar', 1042, 1, '4.600'),
(81, 'Ilyas Munandar', 1043, 2, '4.101'),
(82, 'Alex Junior', 1043, 1, '4.450'),
(83, 'Lionel Messi', 1043, 2, '2.483');

-- --------------------------------------------------------

--
-- Struktur dari tabel `sesi_kuis`
--

CREATE TABLE IF NOT EXISTS `sesi_kuis` (
`id_sesi` int(4) NOT NULL,
  `id_mapel` int(3) NOT NULL,
  `id_user` int(3) NOT NULL,
  `current_number` int(2) DEFAULT '0',
  `status` tinyint(1) DEFAULT '1'
) ENGINE=InnoDB AUTO_INCREMENT=1044 DEFAULT CHARSET=latin1;

--
-- Dumping data untuk tabel `sesi_kuis`
--

INSERT INTO `sesi_kuis` (`id_sesi`, `id_mapel`, `id_user`, `current_number`, `status`) VALUES
(1041, 2, 111, 6, 3),
(1042, 2, 111, 6, 3),
(1043, 2, 111, 6, 3);

-- --------------------------------------------------------

--
-- Struktur dari tabel `status_kuis`
--

CREATE TABLE IF NOT EXISTS `status_kuis` (
`id_status` int(1) NOT NULL,
  `status` char(12) NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

--
-- Dumping data untuk tabel `status_kuis`
--

INSERT INTO `status_kuis` (`id_status`, `status`) VALUES
(1, 'Belum Mulai'),
(2, 'Berlangsung'),
(3, 'Selesai');

-- --------------------------------------------------------

--
-- Struktur dari tabel `status_peserta`
--

CREATE TABLE IF NOT EXISTS `status_peserta` (
`id` int(1) NOT NULL,
  `status` char(10) NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

--
-- Dumping data untuk tabel `status_peserta`
--

INSERT INTO `status_peserta` (`id`, `status`) VALUES
(1, 'Belum Siap'),
(2, 'Siap'),
(3, 'Selesia');

-- --------------------------------------------------------

--
-- Struktur dari tabel `tabel_mapel`
--

CREATE TABLE IF NOT EXISTS `tabel_mapel` (
`id_mapel` int(3) NOT NULL,
  `id_user` int(3) NOT NULL,
  `nama_mapel` varchar(35) NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=latin1;

--
-- Dumping data untuk tabel `tabel_mapel`
--

INSERT INTO `tabel_mapel` (`id_mapel`, `id_user`, `nama_mapel`) VALUES
(2, 111, 'Pemrograman WEB'),
(3, 111, 'Pemrograman Berorientasi Objek'),
(4, 111, 'Pemrograman Basisdata'),
(6, 112, 'Bahasa Indonesia'),
(7, 111, 'PPKN'),
(11, 111, 'Bahasa Inggris'),
(12, 111, 'Matematika 1'),
(13, 111, 'Bahasa Indonesia'),
(14, 111, 'Matematika 2'),
(15, 112, 'Bahasa inggris');

-- --------------------------------------------------------

--
-- Struktur dari tabel `tabel_soal`
--

CREATE TABLE IF NOT EXISTS `tabel_soal` (
`id_soal` int(3) NOT NULL,
  `id_mapel` int(3) NOT NULL,
  `soal` varchar(150) NOT NULL,
  `A` varchar(100) NOT NULL,
  `B` varchar(100) NOT NULL,
  `C` varchar(100) NOT NULL,
  `D` varchar(100) NOT NULL,
  `jawaban_benar` char(1) NOT NULL,
  `waktu` int(3) NOT NULL DEFAULT '60'
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=latin1;

--
-- Dumping data untuk tabel `tabel_soal`
--

INSERT INTO `tabel_soal` (`id_soal`, `id_mapel`, `soal`, `A`, `B`, `C`, `D`, `jawaban_benar`, `waktu`) VALUES
(2, 3, 'Objek adalah', 'objek', 'objek ya objek', 'objekkk', 'object', 'A', 60),
(5, 2, 'Berikut ini yang bukan Bahasa Pemrograman yang digunakan dalam pemrograman website adalah......', 'JavaScript', 'PHP', 'HTML', 'Fotran', 'D', 60),
(6, 2, 'Berikut yang bukan aplikasi dari Web Browser adala', 'Internet Explorer', 'Window Explorer', 'Mozila Firefox', 'Chrome', 'B', 60),
(7, 2, '<head> merupakan tag pada bahasa pemrograman..........', 'PHP', 'CPP', 'HTML', 'JavaScript', 'C', 60),
(8, 6, 'Siapa nama presiden pertama indonesia', 'Sukarno', 'Suharto', 'Megawati', 'Jokowi', 'A', 60),
(9, 6, 'Dimanakah ibukota jawa tengah.....', 'Semarang', 'Bali', 'Jakatta', 'Bandung', 'A', 60),
(10, 2, 'WWW singkatan dari......', 'World Wide Web', 'Wasalamualaikum Warahmatullahi Wabarakatu', 'Wide World Web', 'World War Web', 'A', 60),
(11, 2, 'Php kepanjangan dari.....', 'Hyperlink Protocol', 'Pemberi Harapan Palsu', 'Pemberi Hyperlink Protocol', 'Profeisonal Hyperlink Protocol', 'A', 60),
(12, 15, 'What is she doing?', 'She is dancing', 'He is dancing', 'She is singing', 'He is swimming', 'B', 60),
(13, 2, 'Array adalah........?', 'Data dengan tipe data yang sama', 'Kumpulan data ', 'Kumpulan pemuda', 'Kumpulan data dengan tipe data yang berbeda- beda', 'D', 60);

-- --------------------------------------------------------

--
-- Struktur dari tabel `user`
--

CREATE TABLE IF NOT EXISTS `user` (
`id` int(3) NOT NULL,
  `username` varchar(27) NOT NULL,
  `password` varchar(20) NOT NULL,
  `nickname` varchar(27) NOT NULL,
  `level` char(8) NOT NULL DEFAULT 'Pengajar'
) ENGINE=InnoDB AUTO_INCREMENT=114 DEFAULT CHARSET=latin1;

--
-- Dumping data untuk tabel `user`
--

INSERT INTO `user` (`id`, `username`, `password`, `nickname`, `level`) VALUES
(111, 'ilyas', '123', 'Ilyas Munandar', 'Pengajar'),
(112, 'guru', 'guru', 'Guru', 'Pengajar'),
(113, 'admin', 'admin', 'admin', 'Admin');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `jawaban_peserta`
--
ALTER TABLE `jawaban_peserta`
 ADD PRIMARY KEY (`id_jawaban`);

--
-- Indexes for table `peserta_kuis`
--
ALTER TABLE `peserta_kuis`
 ADD PRIMARY KEY (`id_peserta`);

--
-- Indexes for table `sesi_kuis`
--
ALTER TABLE `sesi_kuis`
 ADD PRIMARY KEY (`id_sesi`);

--
-- Indexes for table `status_kuis`
--
ALTER TABLE `status_kuis`
 ADD PRIMARY KEY (`id_status`);

--
-- Indexes for table `status_peserta`
--
ALTER TABLE `status_peserta`
 ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tabel_mapel`
--
ALTER TABLE `tabel_mapel`
 ADD PRIMARY KEY (`id_mapel`);

--
-- Indexes for table `tabel_soal`
--
ALTER TABLE `tabel_soal`
 ADD PRIMARY KEY (`id_soal`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
 ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `jawaban_peserta`
--
ALTER TABLE `jawaban_peserta`
MODIFY `id_jawaban` int(3) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=270;
--
-- AUTO_INCREMENT for table `peserta_kuis`
--
ALTER TABLE `peserta_kuis`
MODIFY `id_peserta` int(3) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=84;
--
-- AUTO_INCREMENT for table `sesi_kuis`
--
ALTER TABLE `sesi_kuis`
MODIFY `id_sesi` int(4) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=1044;
--
-- AUTO_INCREMENT for table `status_kuis`
--
ALTER TABLE `status_kuis`
MODIFY `id_status` int(1) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=4;
--
-- AUTO_INCREMENT for table `status_peserta`
--
ALTER TABLE `status_peserta`
MODIFY `id` int(1) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=4;
--
-- AUTO_INCREMENT for table `tabel_mapel`
--
ALTER TABLE `tabel_mapel`
MODIFY `id_mapel` int(3) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=16;
--
-- AUTO_INCREMENT for table `tabel_soal`
--
ALTER TABLE `tabel_soal`
MODIFY `id_soal` int(3) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=14;
--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
MODIFY `id` int(3) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=114;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
