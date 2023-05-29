CREATE TABLE `nftrecord` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nftTimeStamp` varchar(255) NOT NULL,
  `buyer` varchar(100) NOT NULL,
  `seller` varchar(100) NOT NULL,
  `currentOwner` varchar(100) NOT NULL,
  `cost` varchar(100) NOT NULL,
  `imageID` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;