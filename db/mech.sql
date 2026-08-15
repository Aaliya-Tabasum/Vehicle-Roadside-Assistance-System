-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               5.0.17-nt - MySQL Community Edition (GPL)
-- Server OS:                    Win32
-- HeidiSQL Version:             9.4.0.5174
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


-- Dumping database structure for mech
CREATE DATABASE IF NOT EXISTS `mech` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `mech`;

-- Dumping structure for table mech.admin
CREATE TABLE IF NOT EXISTS `admin` (
  `id` int(11) NOT NULL auto_increment,
  `email` varchar(150) NOT NULL default '0',
  `pass` varchar(150) NOT NULL default '0',
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Data exporting was unselected.
-- Dumping structure for table mech.assirequests
CREATE TABLE IF NOT EXISTS `assirequests` (
  `id` int(11) NOT NULL auto_increment,
  `uid` int(11) NOT NULL default '0',
  `mid` int(11) NOT NULL default '0',
  `tid` int(11) NOT NULL default '0',
  `status` varchar(50) NOT NULL default '0',
  PRIMARY KEY  (`id`),
  KEY `FK_assirequests_users` (`uid`),
  KEY `FK_assirequests_mechanic` (`mid`),
  KEY `FK_assirequests_travels` (`tid`),
  CONSTRAINT `FK_assirequests_mechanic` FOREIGN KEY (`mid`) REFERENCES `mechanic` (`id`),
  CONSTRAINT `FK_assirequests_travels` FOREIGN KEY (`tid`) REFERENCES `travels` (`id`),
  CONSTRAINT `FK_assirequests_users` FOREIGN KEY (`uid`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Data exporting was unselected.
-- Dumping structure for table mech.feedbacks
CREATE TABLE IF NOT EXISTS `feedbacks` (
  `id` int(11) NOT NULL auto_increment,
  `rating` int(11) NOT NULL default '0',
  `description` varchar(500) NOT NULL default '0',
  `uid` int(11) NOT NULL default '0',
  `mid` int(11) NOT NULL default '0',
  PRIMARY KEY  (`id`),
  KEY `FK_feedbacks_users` (`uid`),
  KEY `FK_feedbacks_mechanic` (`mid`),
  CONSTRAINT `FK_feedbacks_mechanic` FOREIGN KEY (`mid`) REFERENCES `mechanic` (`id`),
  CONSTRAINT `FK_feedbacks_users` FOREIGN KEY (`uid`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Data exporting was unselected.
-- Dumping structure for table mech.mechanic
CREATE TABLE IF NOT EXISTS `mechanic` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(150) NOT NULL default '0',
  `phone` varchar(150) NOT NULL default '0',
  `sname` varchar(150) NOT NULL default '0',
  `saddress` varchar(500) NOT NULL default '0',
  `altphone` varchar(500) NOT NULL default '0',
  `mimage` varchar(500) NOT NULL default '0',
  `certi` varchar(500) NOT NULL default '0',
  `haddress` varchar(500) NOT NULL default '0',
  `pass` varchar(500) NOT NULL default '0',
  `status` varchar(500) NOT NULL default '0',
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Data exporting was unselected.
-- Dumping structure for table mech.travels
CREATE TABLE IF NOT EXISTS `travels` (
  `id` int(11) NOT NULL auto_increment,
  `source` varchar(150) NOT NULL default '0',
  `dest` varchar(150) NOT NULL default '0',
  `tdate` varchar(150) NOT NULL default '0',
  `ttime` varchar(150) NOT NULL default '0',
  `uid` int(11) NOT NULL default '0',
  PRIMARY KEY  (`id`),
  KEY `FK_travels_users` (`uid`),
  CONSTRAINT `FK_travels_users` FOREIGN KEY (`uid`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Data exporting was unselected.
-- Dumping structure for table mech.troubleshoot
CREATE TABLE IF NOT EXISTS `troubleshoot` (
  `id` int(11) NOT NULL auto_increment,
  `vehicle_type` varchar(30) default NULL,
  `category` varchar(100) default NULL,
  `problem` varchar(300) default NULL,
  `solution` text,
  `tools_required` varchar(300) default NULL,
  `difficulty` varchar(20) default NULL,
  `warning` varchar(500) default NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Data exporting was unselected.
-- Dumping structure for table mech.users
CREATE TABLE IF NOT EXISTS `users` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(150) NOT NULL default '0',
  `email` varchar(150) NOT NULL default '0',
  `phone` varchar(150) NOT NULL default '0',
  `gender` varchar(150) NOT NULL default '0',
  `address` varchar(150) NOT NULL default '0',
  `carnum` varchar(150) NOT NULL default '0',
  `bikenum` varchar(150) NOT NULL default '0',
  `policenum` varchar(150) NOT NULL default '0',
  `gnum` varchar(150) NOT NULL default '0',
  `dlimage` varchar(150) NOT NULL default '0',
  `pass` varchar(150) NOT NULL default '0',
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Data exporting was unselected.
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
