
--
-- Current Database: `userinfo`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `userinfo` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `userinfo`;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `name` varchar(20) DEFAULT NULL,
  `phone` varchar(22) NOT NULL,
  `address` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`phone`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
-- Dump completed on 2018-03-31  0:17:20
