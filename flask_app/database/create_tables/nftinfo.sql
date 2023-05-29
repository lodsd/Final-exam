CREATE TABLE `nftinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `description` varchar(255) NOT NULL,
  `token` varchar(100) NOT NULL,
  `path` varchar(100) NOT NULL,
  `ownerID` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;