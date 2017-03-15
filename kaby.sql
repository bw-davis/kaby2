-- MySQL dump 10.13  Distrib 5.7.17, for Linux (x86_64)
--
-- Host: ix-xenial    Database: kaby
-- ------------------------------------------------------
-- Server version	5.6.33

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Current Database: `kaby`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `kaby` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `kaby`;

--
-- Table structure for table `dates_times`
--

DROP TABLE IF EXISTS `dates_times`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dates_times` (
  `dt_id` int(11) NOT NULL AUTO_INCREMENT,
  `meeting_id` int(11) DEFAULT NULL,
  `start_time` time DEFAULT NULL,
  `end_time` time DEFAULT NULL,
  `meeting_date` date DEFAULT NULL,
  PRIMARY KEY (`dt_id`)
) ENGINE=InnoDB AUTO_INCREMENT=147 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dates_times`
--

LOCK TABLES `dates_times` WRITE;
/*!40000 ALTER TABLE `dates_times` DISABLE KEYS */;
INSERT INTO `dates_times` VALUES (1,1,'08:00:00','08:15:00','2017-03-15'),(2,1,'08:15:00','08:30:00','2017-03-15'),(3,1,'08:30:00','08:45:00','2017-03-15'),(4,1,'08:45:00','09:00:00','2017-03-15'),(5,1,'08:00:00','08:15:00','2017-03-16'),(6,1,'08:15:00','08:30:00','2017-03-16'),(7,1,'08:30:00','08:45:00','2017-03-16'),(8,1,'08:45:00','09:00:00','2017-03-16'),(9,2,'10:00:00','10:15:00','2017-03-15'),(10,2,'10:15:00','10:30:00','2017-03-15'),(11,2,'10:30:00','10:45:00','2017-03-15'),(12,2,'10:45:00','11:00:00','2017-03-15'),(13,2,'11:00:00','11:15:00','2017-03-15'),(14,2,'11:15:00','11:30:00','2017-03-15'),(15,2,'11:30:00','11:45:00','2017-03-15'),(16,2,'11:45:00','12:00:00','2017-03-15'),(17,2,'12:00:00','12:15:00','2017-03-15'),(18,2,'12:15:00','12:30:00','2017-03-15'),(19,2,'12:30:00','12:45:00','2017-03-15'),(20,2,'12:45:00','13:00:00','2017-03-15'),(21,2,'13:00:00','13:15:00','2017-03-15'),(22,2,'13:15:00','13:30:00','2017-03-15'),(23,2,'13:30:00','13:45:00','2017-03-15'),(24,2,'13:45:00','14:00:00','2017-03-15'),(25,2,'09:00:00','09:15:00','2017-03-16'),(26,2,'09:15:00','09:30:00','2017-03-16'),(27,2,'09:30:00','09:45:00','2017-03-16'),(28,2,'09:45:00','10:00:00','2017-03-16'),(29,2,'10:00:00','10:15:00','2017-03-16'),(30,2,'10:15:00','10:30:00','2017-03-16'),(31,2,'10:30:00','10:45:00','2017-03-16'),(32,2,'10:45:00','11:00:00','2017-03-16'),(33,2,'11:00:00','11:15:00','2017-03-16'),(34,2,'11:15:00','11:30:00','2017-03-16'),(35,2,'11:30:00','11:45:00','2017-03-16'),(36,2,'11:45:00','12:00:00','2017-03-16'),(37,2,'12:00:00','12:15:00','2017-03-16'),(38,2,'12:15:00','12:30:00','2017-03-16'),(39,2,'12:30:00','12:45:00','2017-03-16'),(40,2,'12:45:00','13:00:00','2017-03-16'),(41,3,'13:00:00','13:15:00','2017-03-15'),(42,3,'13:15:00','13:30:00','2017-03-15'),(43,3,'13:30:00','13:45:00','2017-03-15'),(44,3,'13:45:00','14:00:00','2017-03-15'),(45,3,'14:00:00','14:15:00','2017-03-15'),(46,3,'14:15:00','14:30:00','2017-03-15'),(47,3,'08:00:00','08:15:00','2017-03-16'),(48,3,'08:15:00','08:30:00','2017-03-16'),(49,3,'08:30:00','08:45:00','2017-03-16'),(50,3,'08:45:00','09:00:00','2017-03-16'),(51,4,'13:00:00','13:15:00','2017-03-16'),(52,4,'13:15:00','13:30:00','2017-03-16'),(53,4,'13:30:00','13:45:00','2017-03-16'),(54,4,'13:45:00','14:00:00','2017-03-16'),(55,4,'14:00:00','14:15:00','2017-03-16'),(56,4,'14:15:00','14:30:00','2017-03-16'),(57,4,'13:00:00','13:15:00','2017-03-15'),(58,4,'13:15:00','13:30:00','2017-03-15'),(59,4,'13:30:00','13:45:00','2017-03-15'),(60,4,'13:45:00','14:00:00','2017-03-15'),(61,4,'14:00:00','14:15:00','2017-03-15'),(62,4,'14:15:00','14:30:00','2017-03-15'),(63,5,'08:00:00','08:08:00','2017-02-08'),(64,5,'08:08:00','08:16:00','2017-02-08'),(65,5,'08:16:00','08:24:00','2017-02-08'),(66,5,'08:24:00','08:32:00','2017-02-08'),(67,5,'08:32:00','08:40:00','2017-02-08'),(68,5,'08:40:00','08:48:00','2017-02-08'),(69,4,'13:00:00','13:15:00','2017-03-16'),(70,4,'13:15:00','13:30:00','2017-03-16'),(71,4,'13:30:00','13:45:00','2017-03-16'),(72,4,'13:45:00','14:00:00','2017-03-16'),(73,4,'14:00:00','14:15:00','2017-03-16'),(74,4,'14:15:00','14:30:00','2017-03-16'),(75,4,'13:00:00','13:15:00','2017-03-15'),(76,4,'13:15:00','13:30:00','2017-03-15'),(77,4,'13:30:00','13:45:00','2017-03-15'),(78,4,'13:45:00','14:00:00','2017-03-15'),(79,4,'14:00:00','14:15:00','2017-03-15'),(80,4,'14:15:00','14:30:00','2017-03-15'),(81,6,'08:00:00','08:15:00','2017-03-15'),(82,6,'08:15:00','08:30:00','2017-03-15'),(83,6,'08:30:00','08:45:00','2017-03-15'),(84,6,'08:45:00','09:00:00','2017-03-15'),(85,6,'08:00:00','08:15:00','2017-03-15'),(86,6,'08:15:00','08:30:00','2017-03-15'),(87,6,'08:30:00','08:45:00','2017-03-15'),(88,6,'08:45:00','09:00:00','2017-03-15'),(89,6,'12:00:00','12:15:00','2017-03-15'),(90,6,'12:15:00','12:30:00','2017-03-15'),(91,6,'12:30:00','12:45:00','2017-03-15'),(92,6,'12:45:00','13:00:00','2017-03-15'),(93,6,'08:00:00','08:15:00','2017-03-15'),(94,6,'08:15:00','08:30:00','2017-03-15'),(95,6,'08:30:00','08:45:00','2017-03-15'),(96,6,'08:45:00','09:00:00','2017-03-15'),(97,6,'12:00:00','12:15:00','2017-03-15'),(98,6,'12:15:00','12:30:00','2017-03-15'),(99,6,'12:30:00','12:45:00','2017-03-15'),(100,6,'12:45:00','13:00:00','2017-03-15'),(101,8,'08:00:00','08:15:00','2017-03-15'),(102,8,'08:15:00','08:30:00','2017-03-15'),(103,8,'08:30:00','08:45:00','2017-03-15'),(104,8,'08:45:00','09:00:00','2017-03-15'),(105,8,'10:00:00','10:15:00','2017-03-15'),(106,8,'10:15:00','10:30:00','2017-03-15'),(107,8,'10:30:00','10:45:00','2017-03-15'),(108,8,'10:45:00','11:00:00','2017-03-15'),(109,8,'11:00:00','11:15:00','2017-03-15'),(110,8,'11:15:00','11:30:00','2017-03-15'),(111,8,'11:30:00','11:45:00','2017-03-15'),(112,8,'11:45:00','12:00:00','2017-03-15'),(113,8,'12:00:00','12:15:00','2017-03-15'),(114,8,'12:15:00','12:30:00','2017-03-15'),(115,8,'12:30:00','12:45:00','2017-03-15'),(116,8,'12:45:00','13:00:00','2017-03-15'),(117,8,'10:00:00','10:15:00','2017-03-16'),(118,8,'10:15:00','10:30:00','2017-03-16'),(119,8,'10:30:00','10:45:00','2017-03-16'),(120,8,'10:45:00','11:00:00','2017-03-16'),(121,8,'11:00:00','11:15:00','2017-03-16'),(122,8,'11:15:00','11:30:00','2017-03-16'),(123,8,'11:30:00','11:45:00','2017-03-16'),(124,8,'11:45:00','12:00:00','2017-03-16'),(125,8,'14:00:00','14:15:00','2017-03-16'),(126,8,'14:15:00','14:30:00','2017-03-16'),(127,8,'14:30:00','14:45:00','2017-03-16'),(128,8,'14:45:00','15:00:00','2017-03-16'),(129,8,'15:00:00','15:15:00','2017-03-16'),(130,8,'15:15:00','15:30:00','2017-03-16'),(131,8,'15:30:00','15:45:00','2017-03-16'),(132,8,'15:45:00','16:00:00','2017-03-16'),(133,8,'16:00:00','16:15:00','2017-03-16'),(134,8,'16:15:00','16:30:00','2017-03-16'),(135,9,'08:00:00','08:15:00','2017-03-15'),(136,9,'08:15:00','08:30:00','2017-03-15'),(137,9,'08:30:00','08:45:00','2017-03-15'),(138,9,'08:45:00','09:00:00','2017-03-15'),(139,9,'09:00:00','09:15:00','2017-03-15'),(140,9,'09:15:00','09:30:00','2017-03-15'),(141,9,'09:30:00','09:45:00','2017-03-15'),(142,9,'09:45:00','10:00:00','2017-03-15'),(143,9,'10:00:00','10:15:00','2017-03-15'),(144,9,'10:15:00','10:30:00','2017-03-15'),(145,9,'10:30:00','10:45:00','2017-03-15'),(146,9,'10:45:00','11:00:00','2017-03-15');
/*!40000 ALTER TABLE `dates_times` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `group_leader`
--

DROP TABLE IF EXISTS `group_leader`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `group_leader` (
  `group_leader_id` int(11) NOT NULL AUTO_INCREMENT,
  `group_leader_email` varchar(45) NOT NULL,
  `group_name` varchar(45) NOT NULL,
  PRIMARY KEY (`group_leader_id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `group_leader`
--

LOCK TABLES `group_leader` WRITE;
/*!40000 ALTER TABLE `group_leader` DISABLE KEYS */;
INSERT INTO `group_leader` VALUES (1,'ahill7@uoregon.edu','Andrew'),(4,'bwd@uoregon.edu','The Best'),(13,'Aowen@uoregon.edu','Alex'),(14,'werwer','wrewer'),(23,'bwdavis11@gmail.com','Second Best'),(24,'yuboz@uoregon.edu','Yubo');
/*!40000 ALTER TABLE `group_leader` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `meetings`
--

DROP TABLE IF EXISTS `meetings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `meetings` (
  `meeting_id` int(11) NOT NULL AUTO_INCREMENT,
  `location` char(25) DEFAULT NULL,
  `description` char(100) DEFAULT NULL,
  `length` int(11) DEFAULT NULL,
  `uuid` char(36) DEFAULT NULL,
  `meeting_name` varchar(15) DEFAULT NULL,
  `creator_email` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`meeting_id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `meetings`
--

LOCK TABLES `meetings` WRITE;
/*!40000 ALTER TABLE `meetings` DISABLE KEYS */;
INSERT INTO `meetings` VALUES (1,'office','Meet with groups to discuss Architecture requirements',15,'98e6d9bd-fe69-4719-9edb-f5949598a873','SRS specificati','ahill7@uoregon.edu'),(2,'class room','Final review session',15,'c97d121e-6a5c-4f68-a560-8c6cc23b08a7','reivew sessions','ahill7@uoregon.edu'),(4,'class room','Final presentations',15,'51277624-be32-4715-8795-adc55e08f2e9','Final presentat','ahill7@uoregon.edu'),(5,'class room','Project 1 presentations',8,'98e6d9bd-fe69-47AB-9edb-f5949598a873','Project 1 press','ahill7@uoregon.edu'),(6,'here','test meeting',15,'66a47573-6613-4b91-ae9e-a50994772e87','test meeting','ahill7@uoregon.edu'),(7,'here','test meeting2',15,'6660a3dd-17dd-4727-9df9-c191ef0dca22','test meeting 2','ahill7@uoregon.edu'),(8,'science library','Multiple Contacts Meeting Example',15,'339f1667-9b69-4cda-b2de-1cbfdf9d36b7','Multiple Contac','ahill7@uoregon.edu'),(9,'home','Test meeting to show two contacts, one who has responded and one who has not',15,'ee8a163e-146f-4f20-9668-55e90566a690','test example wi','ahill7@uoregon.edu');
/*!40000 ALTER TABLE `meetings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `respond_meeting`
--

DROP TABLE IF EXISTS `respond_meeting`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `respond_meeting` (
  `issue_ID` int(11) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `respond_meeting`
--

LOCK TABLES `respond_meeting` WRITE;
/*!40000 ALTER TABLE `respond_meeting` DISABLE KEYS */;
INSERT INTO `respond_meeting` VALUES (1,1),(1,6),(2,1),(3,1),(3,6),(3,8),(3,9),(4,1),(4,6),(4,8),(4,9),(6,1),(7,1),(8,1),(8,4),(8,13),(8,23),(8,24),(9,1),(9,24);
/*!40000 ALTER TABLE `respond_meeting` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `response`
--

DROP TABLE IF EXISTS `response`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `response` (
  `dt_id` int(11) DEFAULT NULL,
  `start_time` time DEFAULT NULL,
  `end_time` time DEFAULT NULL,
  `group_leader_id` int(11) DEFAULT NULL,
  `checked` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `response`
--

LOCK TABLES `response` WRITE;
/*!40000 ALTER TABLE `response` DISABLE KEYS */;
INSERT INTO `response` VALUES (8,'08:00:00','08:15:00',1,0),(8,'08:15:00','08:30:00',1,0),(8,'08:45:00','09:00:00',1,0),(8,'10:30:00','10:45:00',1,0),(8,'10:45:00','11:00:00',1,0),(8,'11:15:00','11:30:00',1,0),(8,'14:15:00','14:30:00',1,0),(8,'14:30:00','14:45:00',1,0),(8,'08:00:00','08:15:00',13,0),(8,'08:15:00','08:30:00',13,0),(8,'11:00:00','11:15:00',13,0),(8,'11:15:00','11:30:00',13,0),(8,'11:30:00','11:45:00',13,0),(8,'11:45:00','12:00:00',13,0),(8,'12:00:00','12:15:00',13,0),(8,'12:15:00','12:30:00',13,0),(8,'12:30:00','12:45:00',13,0),(8,'16:15:00','16:30:00',13,0),(8,'08:00:00','08:15:00',24,0),(8,'12:45:00','13:00:00',24,0),(8,'10:00:00','10:15:00',24,0),(8,'10:15:00','10:30:00',24,0),(9,'08:00:00','08:15:00',1,0),(9,'08:30:00','08:45:00',1,0),(9,'10:30:00','10:45:00',1,0),(8,'08:15:00','08:30:00',4,0),(8,'10:45:00','11:00:00',4,0),(8,'12:15:00','12:30:00',4,0),(8,'11:00:00','11:15:00',4,0),(8,'14:30:00','14:45:00',4,0),(8,'15:30:00','15:45:00',4,0);
/*!40000 ALTER TABLE `response` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `fname` char(25) DEFAULT NULL,
  `lname` char(25) DEFAULT NULL,
  `password` char(25) NOT NULL,
  `email` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'Stuart','Faulk','password',NULL),(2,'kaby','','kaby',NULL),(3,'Yuboz',NULL,'','yuboz@uoregon.edu'),(4,'Andrew','Hill','helios','ahill7@uoregon.edu'),(5,'Brain','Davis','','bwd@uoregon.edu'),(6,'Andrew',NULL,'','andrew.s.hill6@gmail.com'),(7,NULL,NULL,'',NULL);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_meeting_bridge`
--

DROP TABLE IF EXISTS `user_meeting_bridge`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_meeting_bridge` (
  `user_id` int(11) NOT NULL,
  `meeting_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_meeting_bridge`
--

LOCK TABLES `user_meeting_bridge` WRITE;
/*!40000 ALTER TABLE `user_meeting_bridge` DISABLE KEYS */;
INSERT INTO `user_meeting_bridge` VALUES (1,1);
/*!40000 ALTER TABLE `user_meeting_bridge` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-03-14 18:03:34
