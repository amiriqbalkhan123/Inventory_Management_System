CREATE DATABASE  IF NOT EXISTS `inventory_management_system` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `inventory_management_system`;
-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: inventory_management_system
-- ------------------------------------------------------
-- Server version	8.0.40

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `category_data`
--

DROP TABLE IF EXISTS `category_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `category_data` (
  `id` int NOT NULL,
  `name` varchar(30) DEFAULT NULL,
  `description` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `category_data`
--

LOCK TABLES `category_data` WRITE;
/*!40000 ALTER TABLE `category_data` DISABLE KEYS */;
INSERT INTO `category_data` VALUES (2,'Electronics','Contains every type of electronics'),(3,'Motorcycles','Contains Baby Motorcycles Toys'),(4,'Grocery','Contains any type of groceries in the shop'),(7,'Snacks','All snacks stored in this category'),(10,'Alokozay Beverages','Energy Drinks and Purified Drinking Water'),(11,'Medicine','All Medicine in this category'),(12,'Ginseng Energy Drink','Just this type of category'),(15,'Chairs','General Purpose / Office Use / Gaming Chairs'),(16,'Building','all buildings here'),(20,'Medicine','All medicine stored in this category'),(21,'Ahmad gul','the best one'),(44,'Nestle Juices','The best juices in the area'),(113,'Shahid Brand','Shahid Brand Category'),(199,'Jamal Tissus','All tissues of jamal company'),(220,'Ahmad gul','the best one'),(255,'melon juice','juices category'),(505,'Alokozay','THE BEST CATEGORY IN THE MARKET'),(677,'Jamal Energy Drinks','all energy drinks regarding jamal company will be stored in this category'),(1011,'LCD Screen','The best screen in the market'),(4561,'Alokozay Teas','THE BEST TEA IN THE MARKET'),(112121,'Ciproflaxacin','The best medicine');
/*!40000 ALTER TABLE `category_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `credentials`
--

DROP TABLE IF EXISTS `credentials`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `credentials` (
  `username` varchar(50) DEFAULT NULL,
  `password` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `credentials`
--

LOCK TABLES `credentials` WRITE;
/*!40000 ALTER TABLE `credentials` DISABLE KEYS */;
INSERT INTO `credentials` VALUES ('nabi gul','ngul'),('amir','amir123');
/*!40000 ALTER TABLE `credentials` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customer_data`
--

DROP TABLE IF EXISTS `customer_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customer_data` (
  `customer_id` int NOT NULL,
  `customer_name` varchar(100) DEFAULT NULL,
  `customer_contact` varchar(100) DEFAULT NULL,
  `customer_address` varchar(100) DEFAULT NULL,
  `customer_type` varchar(100) DEFAULT NULL,
  `additional_notes` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`customer_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer_data`
--

LOCK TABLES `customer_data` WRITE;
/*!40000 ALTER TABLE `customer_data` DISABLE KEYS */;
INSERT INTO `customer_data` VALUES (1,'Amir Iqbal Khan','0784745712','Kabul, Afghanistan','VIP','The best customer in the area\n'),(2,'Ahsanullah Khan','786613810','Nangarhar, Afghanistan','Regular','The best one in kabul afghanistan\n	\n'),(3,'Hashim Khan','784545454','Kabul, Afghanistan','Wholesale','The customer has mental health problems, take care and meanwhile he is a good person\n\n\n'),(4,'Ahmad Javed Jaihoon','0799412662','Kabul, Afghanistan','VIP','The best customer ever\n'),(5,'mahmood kahn','078454545','kabul, afghanistan','VIP','the best customer in the area\n\n'),(6,'Kardan Customer','7845545454','kabul, afghanistan','VIP','the best customer ever visited this inventory\n\n\n'),(7,'Abdul Karim','0784545454','Kabul, Afghanistan','Wholesale','The best customer of the inventory\n'),(8,'Abdul Jameel','07845454545','Nangarhar, Afghanistan','VIP','The angry one\n\n'),(9,'Abdul Kamal','07854546521','Badakhshan, Afghanistan','Regular','most visiting one\n'),(10,'Ahmad Jamal','03030303030','Islamabad, Pakistan','Wholesale','the best one ever\n'),(11,'Ahmad Mubashir','033344554477','Lahore, Pakistan','VIP','The best\n'),(12,'Salaam','0784598585','Rawalpindi, Pakistan','Wholesale','Not the best\n'),(13,'Mohammad Kamal','078454565665','Herat, Afghanistan','VIP','The best customer\n'),(14,'Ahmad Javed','07855988565','Faryab, Afghanistan','Wholesale','The best one ever\n'),(15,'Fareed','07845121452','Bamyaan, Afghanistan','VIP','He is selling too much\n'),(16,'Krishma','075845456544','Helmand, Afghanistan','Wholesale','The best one\n'),(17,'Jabar','0784541245','Kunar, Afghanistan','VIP','The best\n'),(18,'Nader Khan','078456+98525','Kunduz, Afghanistan','Wholesale','The best\n'),(19,'Nazeer Ahmad','0785454545','Paktika, Afghanistan','VIP','Not too good\n'),(20,'Ahmad Khan','0785451144','Kabul, Afghanistan','Wholesale','The best customer ever');
/*!40000 ALTER TABLE `customer_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `employee_data`
--

DROP TABLE IF EXISTS `employee_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `employee_data` (
  `empid` int NOT NULL,
  `name` varchar(200) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `gender` varchar(50) DEFAULT NULL,
  `dob` varchar(30) DEFAULT NULL,
  `contact` varchar(30) DEFAULT NULL,
  `employment_type` varchar(50) DEFAULT NULL,
  `education` varchar(30) DEFAULT NULL,
  `work_shift` varchar(50) DEFAULT NULL,
  `address` varchar(100) DEFAULT NULL,
  `doj` varchar(30) DEFAULT NULL,
  `salary` varchar(50) DEFAULT NULL,
  `usertype` varchar(50) DEFAULT NULL,
  `password` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`empid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employee_data`
--

LOCK TABLES `employee_data` WRITE;
/*!40000 ALTER TABLE `employee_data` DISABLE KEYS */;
INSERT INTO `employee_data` VALUES (2,'Mohammad','afzal@gmail.com','Male','26/06/2025','78454545','Part Time','B.Com','Evening','kabul, afghanistan','26/06/2025','45000','Employee','afghan123'),(4,'Zia Ur Rehman','zia@gmail.com','Male','29/06/2025','0785101010','Part Time','B.Sc','Morning','kandahar, afghanistan','09/06/2022','48000','Employee','afghan@123'),(5,'Mohammad Afzal','afzal@gmail.com','Male','29/06/2025','785101010','Full Time','B.Sc','Morning','kandahar, afghanistan','09/06/2022','48000','Employee','afghan@123'),(6,'Abasin Atalzai','abasinatalzai@gmail.com','Male','29/06/2025','0785656565','Part Time','BBA','Evening','nangarhar, afghanistan','11/06/2024','14500','Employee','Afghan@12345'),(7,'Noor Rahman','noor@gmail.com','Male','29/06/2025','784545454','Part Time','M.Tech','Night','kandahar, afghanistan','07/06/2024','15800','Employee','Afghanistan@123'),(8,'Ilham Jan','ilham@gmail.com','Male','29/06/2025','07854545454','Part Time','B.Sc','Evening','Taimani, Afghanistan','08/06/2023','14500','Employee','Afghanistan@12345'),(9,'Ahmad Kamal','kamal@gmail.com','Male','29/06/2025','0785654125','Contract','BBA','Morning','Logar, Afghanistan','10/09/2024','18500','Employee','Afghanistan@123456'),(10,'Mustafa Khan','mustafa@gmail.com','Male','29/06/2025','0784126545','Intern','LLB','Evening','Kunduz, Afghanistan','10/09/2024','19000','Employee','Afg@123@123'),(11,'Fareshta Jan Khan','fareshta@gmail.com','Female','29/06/2025','7854545454','Full Time','MBA','Night','Kandahar, Afghanistan','15/04/2025','35000','Employee','Afghanistan@123@123'),(12,'Madina','madina@gmail.com','Female','29/06/2025','075451212112','Part Time','B.Sc','Evening','Kabul, Afghanistan','15/04/2025','38000','Employee','AfghanAfghan@123123'),(13,'Jamal','jamal@gmail.com','Male','29/06/2025','7854545454','Full Time','MBA','Night','Faryab, Afghanistan','15/04/2025','410000','Employee','Afghan@123@123'),(14,'Azmatullah Khan','azmatullah@hotmail.com','Male','29/06/2025','78525654','Part Time','LLM','Night','Farah, Afghanistan','15/04/2025','350000','Employee','Kabul@123123'),(15,'Ahsanullah Khan','ahsanullah@gmail.com','Male','29/06/2025','786613810','Full Time','M.Arch','Morning','Paktia, Afghanistan','15/04/2025','1452000','Employee','Kabul123'),(16,'Bilal Khan','Bilalkhan@gmail.com','Male','06/07/2025','07845121187','Full Time','M.Tech','Evening','Kabul Afghanistan','06/07/2025','45000','Employee','Afghanistan@123'),(17,'Ahmad','iqbal@gmail.com','Male','06/07/2025','7844544','Casual','B.Com','Evening','Kabul, afghanistan','06/07/2025','458000','Employee','Afghanistan@123'),(18,'Ehteshamulhaq','ehtesham@gmail.com','Male','09/07/2014','079585858585','Part Time','B.Sc','Night','Kabul, Afghanistan','11/09/2024','48000','Employee','Afghanistan@123'),(19,'Ahmad','ahmadullah@gmail.com','Male','07/07/2025','7854541254','Casual','M.Tech','Night','Kabul, afghanistan','14/07/2022','48000','Employee','Afghanistan@123'),(20,'Mustafa','mustafa@gmail.com','Male','07/07/2025','07854545454','Part Time','B.Sc','Night','Kabul, afghanistan','10/07/2024','48000','Employee','afghanistan@123'),(21,'Zia Hamzakhil','zia@gmail.com','Male','09/07/2025','078545454545','Part Time','B.Sc','Evening','kabul, afghanistan','09/07/2021','48000','Employee','123123'),(22,'Hilal Khan','hilal@gmail.com','Male','10/07/2025','07581235456','Part Time','B.Com','Evening','Kabul, afghanistan','10/07/2025','48000','Employee','123'),(23,'Shahidullah Khan','shahidkhan@gmail.com','Male','12/07/2025','78541254','Contract','M.Sc','Morning','Kabul Airport','11/07/2024','48000','Employee','Afghanistan@123'),(24,'Jamal ud Din','jamal@gmail.com','Male','11/08/2025','0785412541','Part Time','MBA','Evening','Nangarhar, Afghanistan','11/08/2022','45000','Employee','Afghan@12345'),(25,'Abdul Wahid','abdulwahid@gmail.com','Male','10/08/2016','07854125412','Part Time','B.Sc','Morning','Logar, Afghanistan (Altamoor)','10/08/2023','45000','Employee','Afghanistan'),(26,'Amir','amiriqbalkhan@gmail.com','Male','29/08/2025','0785454545454','Part Time','B.Com','Evening','kabul, afghanistan','29/08/2025','450000','Employee','Afghanistan'),(27,'Saleem','saleem@gmail.com','Male','25/09/2025','078541254545','Part Time','B.Sc','Evening','Kabul afghanistan','25/09/2025','450000','Employee','afghanistan');
/*!40000 ALTER TABLE `employee_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product_data`
--

DROP TABLE IF EXISTS `product_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `product_data` (
  `id` int NOT NULL AUTO_INCREMENT,
  `category` varchar(100) DEFAULT NULL,
  `supplier` varchar(100) DEFAULT NULL,
  `name` varchar(100) DEFAULT NULL,
  `price` decimal(10,2) DEFAULT NULL,
  `discount` int DEFAULT NULL,
  `discounted_price` decimal(10,2) DEFAULT NULL,
  `quantity` int DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=49 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product_data`
--

LOCK TABLES `product_data` WRITE;
/*!40000 ALTER TABLE `product_data` DISABLE KEYS */;
INSERT INTO `product_data` VALUES (8,'alokozay energy drinks','amir iqbal','magic',100.00,NULL,NULL,47,'Active'),(10,'alokozay energy drinks','zia ur rahman','energy123',44.00,NULL,NULL,40,'Select Status'),(11,'Alokozay Beverages','Mohammad Aziz','Magic',1200.00,7,1116.00,20,'Inactive'),(14,'Electronics','Navid Khan','Socket',2500.00,1,2475.00,1000,'Select Status'),(17,'Musical Instruments','Irfan Sahak','Harmonium',45000.00,3,43650.00,70,'Active'),(18,'Snacks','Latif Ahmadi','Nestle',100.00,2,98.00,100,'Select Status'),(21,'Snacks','Ahmad Zia Zazai','Lays Chips',30.00,1,29.70,100,'Active'),(24,'Snacks','zia ur rahman','juice',100.00,2,98.00,100,'Active'),(25,'Snacks','Latif Ahmadi','Potato Chips',35.00,1,34.65,100,'Inactive'),(26,'Motorcycles','jan agha','sadf',324234.00,3,314506.98,100,'Active'),(28,'Snacks','mohammad jan','Lollipop no1',10.00,1,9.90,12000,'Inactive'),(29,'Ginseng Energy Drink','Abasin','Ginseng Energy',880.00,0,880.00,3200,'Active'),(30,'Medicine','Amir Iqbal Khan','Amoxicillin',180.00,3,174.60,10,'Active'),(31,'Grocery','Latif Ahmadi','Lays',30.00,4,28.80,100,'Select Status'),(32,'Medicine','Abasin','Ginseng Energy',880.00,4,844.80,3200,'Inactive'),(33,'Ginseng Energy Drink','Abasin','Ginseng Energy 1',880.00,0,880.00,3200,'Inactive'),(34,'Motorcycles','Mohammad Dawood','Taktaaz Motorcycles',45000.00,2,44100.00,10,'Active'),(35,'Chairs','Jan Agha Mohammadi','Office Chairs',12000.00,2,11760.00,100,'Active'),(36,'Alokozay Beverages','Farhan Mohammad','WOW',20.00,1,19.80,100,'Active'),(37,'Teas','Mohammad Dawood','Haji Gul Tea',220.00,1,217.80,80,'Active'),(38,'Snacks','Latif Ahmadi','Snicker Chocalate Bar',30.00,1,29.70,500,'Active'),(39,'Alokozay Beverages','Navid Khan','Magic ',40.00,3,38.80,120,'Active'),(40,'Alokozay','Farhan Mohammad','Magic',20.00,2,19.60,1050,'Active'),(41,'LCD Screen','Mustafa Hashemi','LCD 42 Inch Screen',145000.00,2,142100.00,12,'Active'),(43,'Shahid Brand','Jan Agha Mohammadi','Shampoo',120.00,1,118.80,1500,'Active'),(44,'Alokozay Beverages','mustafa','Magic',20.00,0,20.00,1600,'Active'),(45,'Shahid Brand','Mohammad Dawood','Soap',120.00,1,118.80,100,'Active'),(46,'Ciproflaxacin','Latif Ahmadi','Cipro 100 mg',120.00,1,118.80,1200,'Active'),(47,'Jamal Tissus','Farhan Mohammad','Small Tissue',120.00,1,118.80,100,'Active'),(48,'Jamal Energy Drinks','Navid Khan','Jamal Magic',120.00,2,117.60,100,'Active');
/*!40000 ALTER TABLE `product_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `registration_credentials`
--

DROP TABLE IF EXISTS `registration_credentials`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `registration_credentials` (
  `id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(100) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(64) NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `registration_credentials`
--

LOCK TABLES `registration_credentials` WRITE;
/*!40000 ALTER TABLE `registration_credentials` DISABLE KEYS */;
INSERT INTO `registration_credentials` VALUES (1,'iqbalnabizada2015@gmail.com','iqbalnabizada','Amir@12345','2025-06-25 22:37:45'),(2,'iqbalnabizada2017@gmail.com','amir','11fd7274c1dbaeec873c9c896ada7d226f8222b1040c0bf91cf895c016b9ae04','2025-06-25 22:43:46'),(3,'iqbalnabizada2018@gmail.com','a','0c83d2754d83f3f29e35ff2ca70c387209ec01e3af5d392665c322a0a8d27ccc','2025-06-25 22:50:58'),(4,'mustafaarman05@gmail.com','mustafa','4627b5e8a301ba8fadc607ba587deeaf0bdfc3f5cd2957004b23be4fd391f082','2025-06-25 22:52:16'),(5,'ishahidullah010@gmail.com','shahid','8e62760ae968dbc18c8edc6d4b9f86fb1a151f90fd079f1ef6d7bccc5b1784a2','2025-07-12 17:46:57'),(6,'miryahyamohammadi@gmail.com','miryahya','60bf4abbf34e9598ba191c860d17987827bfc8b1b8b4fa5e579918d8a02dff02','2025-10-28 00:27:54');
/*!40000 ALTER TABLE `registration_credentials` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sales_data`
--

DROP TABLE IF EXISTS `sales_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sales_data` (
  `product_id` int NOT NULL,
  `product_name` varchar(50) DEFAULT NULL,
  `category` varchar(50) DEFAULT NULL,
  `unit_of_measure` varchar(50) DEFAULT NULL,
  `price_per_unit` varchar(100) DEFAULT NULL,
  `purchase_price` varchar(100) DEFAULT NULL,
  `selling_price` varchar(100) DEFAULT NULL,
  `quantity` varchar(200) DEFAULT NULL,
  `expiry_date` varchar(30) DEFAULT NULL,
  `discount` varchar(30) DEFAULT NULL,
  `tax` varchar(30) DEFAULT NULL,
  `sub_total` varchar(100) DEFAULT NULL,
  `notes` varchar(300) DEFAULT NULL,
  `sales_id` int NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`sales_id`)
) ENGINE=InnoDB AUTO_INCREMENT=44 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sales_data`
--

LOCK TABLES `sales_data` WRITE;
/*!40000 ALTER TABLE `sales_data` DISABLE KEYS */;
INSERT INTO `sales_data` VALUES (101,'Lays Chips','Snacks','packs','30','28','30','120','30/05/2025','1','1','100','Available in the Inventory\n\n\n',4),(10,'energy123','alokozay energy drinks','cm','100','44.00','200','1000','09/06/2025','10','10','200000.00','neslte melon juice\n\n\n\n',13),(10,'energy123','alokozay energy drinks','cm','100','44.00','200','1000','09/06/2025','100','100','200000.00','neslte melon juice\n\n\n\n\n',14),(10,'energy123','alokozay energy drinks','cm','100','44.00','200','1000','09/06/2025','1000','1000','200000.00','neslte melon juice\n\n\n\n\n\n',15),(10,'energy123','alokozay energy drinks','mL','100','44.00','100','120','12/06/2025','0','0','12000.00','the best\n',16),(10,'energy123','alokozay energy drinks','mL','100','44.00','100','1231','12/06/2025','0','0','123100.00','the best\n',17),(10,'energy123','alokozay energy drinks','cm','100','44.00','200','1000','09/06/2025','100','100','200000.00','neslte melon juice\n\n\n\n\n',18),(10,'energy123','alokozay energy drinks','mL','100','44.00','100','120','16/06/2025','7','10','12276.00','THE BEST ONE HERE IN THIS AREA\n',22),(34,'Taktaaz Motorcycles','Motorcycles','mL','52000','45000.00','52000','12','16/06/2028','5','10','652080.00','the best one in kabul  afghanistan\n',23),(33,'Ginseng Energy 1','Ginseng Energy Drink','packs','900','880.00','900','120','08/06/2025','5','7','109782.00','energy drinks\n',24),(10,'energy123','alokozay energy drinks','mL','100','44.00','100','1000','22/06/2025','1','2','100980.00','the best\n',25),(10,'energy123','alokozay energy drinks','mL','20','20','25','19','29/06/2025','1','5','493.76','This product is also available in the second stock inventory\n',26),(37,'Haji Gul Tea','Teas','packs','230','220.00','230','190','29/06/2025','2','1','43254.26','The best tea in the area\n',27),(37,'Haji Gul Tea','Teas','packs','230','220.00','230','10','29/06/2025','2','1','2276.54','The best tea in the area\n',28),(37,'Haji Gul Tea','Teas','packs','230','220.00','230','1','29/06/2025','2','1','227.65','The best tea in the area\n',29),(37,'Haji Gul Tea','Teas','packs','230','220.00','230','3','29/06/2025','2','1','682.96','The best tea in the area\n',30),(37,'Haji Gul Tea','Teas','packs','230','220.00','230','8','29/06/2025','2','1','1821.23','The best tea in the area\n',31),(37,'Haji Gul Tea','Teas','packs','270','220.00','270','2560','29/06/2025','1','20','821145.60','Sold successfully\n',32),(10,'energy123','alokozay energy drinks','mL','44','44.00','50','10000','30/06/2025','3','4','504400.00','selt successfully\n',34),(10,'energy123','alokozay energy drinks','packs','50','44.00','50','1200','06/07/2025','3','10','64020.00','The best\n',35),(41,'LCD 42 Inch Screen','LCD Screen','Feet','148000','145000.00','148000','12','07/07/2025','2','5','1827504.00','SOLD TO AMIR\n',36),(37,'Haji Gul Tea','Teas','mL','240','220.00','240','1000','10/07/2025','1','3','244728.00','sold\n',38),(43,'Shampoo','Shahid Brand','mL','30','120.00','150','400','12/07/2025','3','10','64020.00','sold to mr amir iqbal khan\n',39),(37,'Haji Gul Tea','Teas','kg','60','220.00','270','100','12/07/2025','1','1','26997.30','sold\n',40),(37,'Haji Gul Tea','Teas','kg','60','220.00','270','5000','12/07/2025','10','10','1336500.00','sold\n\n',41),(47,'Small Tissue','Jamal Tissus','inches','110','120.00','120','10','11/08/2025','1','5','1247.40','Sold\n',42),(48,'Jamal Magic','Jamal Energy Drinks','mL','130','120.00','130','100','06/10/2025','3','10','13871.00','sold\n',43);
/*!40000 ALTER TABLE `sales_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sales_master`
--

DROP TABLE IF EXISTS `sales_master`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sales_master` (
  `sales_id` int NOT NULL,
  `customer_id` int DEFAULT NULL,
  `transaction_id` int DEFAULT NULL,
  PRIMARY KEY (`sales_id`),
  KEY `customer_id` (`customer_id`),
  KEY `transaction_id` (`transaction_id`),
  CONSTRAINT `sales_master_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customer_data` (`customer_id`),
  CONSTRAINT `sales_master_ibfk_2` FOREIGN KEY (`transaction_id`) REFERENCES `transaction_data` (`transaction_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sales_master`
--

LOCK TABLES `sales_master` WRITE;
/*!40000 ALTER TABLE `sales_master` DISABLE KEYS */;
/*!40000 ALTER TABLE `sales_master` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `supplier_data`
--

DROP TABLE IF EXISTS `supplier_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `supplier_data` (
  `invoice` int NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `contact` varchar(100) DEFAULT NULL,
  `description` text,
  PRIMARY KEY (`invoice`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `supplier_data`
--

LOCK TABLES `supplier_data` WRITE;
/*!40000 ALTER TABLE `supplier_data` DISABLE KEYS */;
INSERT INTO `supplier_data` VALUES (1,'Farhan Mohammad','0784664466','Alcoholic Beverages Dealer Located in DHA - III'),(2,'Ahmad Zia Zazai','0799415522','Energy Drinks Supplier'),(3,'Jan Agha Mohammadi','0784545454','Medicine Supplier'),(4,'Latif Ahmadi','0785412544','Snacks Supplier'),(5,'Navid Khan','0744112255','Electronics Supplier'),(7,'zia ur rahman','0788445533','skin care supplier'),(8,'mohammad','38383838','kabul'),(11,'zia ur rahman','788445533','skin care supplier'),(16,'mustafa','38484848','logar'),(17,'Abasin','78555555','The best supplier in the area'),(19,'Abasin','78555555','The best supplier in the area'),(20,'Amir Iqbal Khan','0744545454','the best supplier in the area'),(21,'Amir Iqbal Khan','07845645454','The best one ever'),(22,'Abasin','078544546545','THE BEST SUPPLIER IN THE ZONE'),(38,'Abasin','0784545454','THE BEST ONE IN THE AREA'),(39,'Abasin','078454545','Testing the supplier for the next time'),(101,'Mahmood Jan','29393939','the best one'),(111,'zia ur rahman jaU','788445533','skin care supplier'),(113,'Shahid Khan','078541254','The best Supplier'),(120,'Farhan Mohammad','0729393939','the best one here'),(191,'Abasin','0784545454','THE BEST'),(300,'Mohammad Dawood','0788338833','Supplies Books'),(452,'Jamal','07841254512','THE BEST'),(489,'Hilal Khan','0784112554','The best one'),(548,'Amir Iqbal Khan','7884488484','THE BEST'),(1002,'AHMADULLAH','078454545454','THE BEST ONE IN THE AREA'),(1011,'Mohammad Afzal Niazi','07895522555','Located in kulola pushta'),(1024,'Mustafa Hashemi','07854125454','The best one'),(1145,'Mustafa Hashemi','078545454554','THE BEST ONE IN THE AREA'),(1254,'Shahid Khan','07845121544','the best'),(1545,'Abasin','0784546652','THE BEST ONE'),(1929,'Abasin','07846545121','The best supplier'),(3000,'Sajad','07854545454','The best supplier in the area'),(10012,'mohammad','38383838','kabul'),(12311,'Amir Iqbal Khan','07884488484','THE BEST'),(12335,'Jabar Khan','078412544125','The best one'),(14521,'Hilal Khan','0784122545','The best supplier in the market'),(14587,'Hilal Khan','0784122545','The best supplier in the market'),(45687,'Mahmood','078412541554','the best one'),(54545,'Abasin','07854545454','the best'),(54899,'ahmadjan gul','97373737373','kabul afghanistanA'),(123212,'Zia','07855441254','the best one'),(145874,'Hilal Khan','0784122545','The best supplier in the market'),(878754,'Amir Iqbal Khan','07884488484','THE BEST'),(1223123,'Zia','078541254','the best supplier in the area');
/*!40000 ALTER TABLE `supplier_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tax_table`
--

DROP TABLE IF EXISTS `tax_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tax_table` (
  `id` int NOT NULL,
  `tax` decimal(5,2) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tax_table`
--

LOCK TABLES `tax_table` WRITE;
/*!40000 ALTER TABLE `tax_table` DISABLE KEYS */;
INSERT INTO `tax_table` VALUES (1,3.00);
/*!40000 ALTER TABLE `tax_table` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `transaction_data`
--

DROP TABLE IF EXISTS `transaction_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `transaction_data` (
  `transaction_id` int NOT NULL,
  `transaction_date` varchar(100) DEFAULT NULL,
  `transaction_time` varchar(100) DEFAULT NULL,
  `payment_type` varchar(100) DEFAULT NULL,
  `payment_status` varchar(100) DEFAULT NULL,
  `total_amount` varchar(100) DEFAULT NULL,
  `handled_by` varchar(100) DEFAULT NULL,
  `notes` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`transaction_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transaction_data`
--

LOCK TABLES `transaction_data` WRITE;
/*!40000 ALTER TABLE `transaction_data` DISABLE KEYS */;
INSERT INTO `transaction_data` VALUES (1,'29/06/2025','02:44:26 PM','Debit Card','Completed','12000','Amir Iqbal Khan','transaction successfully done\n'),(2,'29/06/2025','02:44:37 PM','Debit Card','Pending','18000','Amir Iqbal Khan','Done Successfully\n'),(3,'29/06/2025','02:44:58 PM','Master Card','In Progress','220000','Ahmad','Done Successfully\n'),(4,'29/06/2025','02:45:18 PM','Paypal','Pending','12200','Javed','Pending Transaction\n'),(5,'29/06/2025','02:45:37 PM','Debit Card','Failed','1100','Ahmad Zubair','Failed due to Connection\n'),(6,'29/06/2025','02:45:49 PM','Paypal','Pending','18000','Riaz','Failed due to Connection\n'),(7,'29/06/2025','02:46:05 PM','Paypal','Completed','18000','Mohammad','Done Successfully\n'),(8,'29/06/2025','02:46:13 PM','Paypal','Completed','18000','Baktash','Done Successfully\n'),(9,'29/06/2025','02:46:27 PM','COD','Completed','120000','Ahmad Javed','Done Successfully\n'),(10,'29/06/2025','02:46:46 PM','Master Card','Pending','19000','Ahmad Mubashir','Transaction is pending\n'),(11,'29/06/2025','02:47:03 PM','Paypal','In Progress','17000','Ahmad Jan','Transaction is in progress\n'),(12,'15/06/2022','02:47:31 PM','Debit Card','Failed','145000','Haji Muhammad','Transaction Failed due to Connection\n'),(13,'15/06/2022','02:47:54 PM','Debit Card','Pending','185000','Awal Gul','Transaction Is Pending\n'),(14,'15/06/2022','02:48:14 PM','Paypal','In Progress','16000','Atequllah','Transaction is in progress\n'),(15,'15/06/2022','02:48:35 PM','COD','Refunded','18000','Goodar','Transcation Refunded Successfully\n'),(16,'25/06/2025','02:48:56 PM','COD','Refunded','210000','Jabar Khan','Transaction Refunded Successfully\n'),(17,'25/06/2025','02:49:19 PM','Master Card','Completed','152000','Jamal ud Din','Transaction Completed\n'),(18,'25/06/2025','02:49:31 PM','Paypal','Failed','14000','Jamal','Failed\n'),(19,'25/06/2025','02:49:49 PM','Cash','Completed','15400','Azmatullah','Received\n'),(20,'25/06/2025','02:50:06 PM','Paypal','Failed','14000','Abdul Naser','Failed due to connection\n'),(21,'25/06/2025','02:50:30 PM','Cash','Completed','18000','Ahsanullah','Cash Received\n'),(22,'25/06/2025','02:50:49 PM','Paypal','Failed','21000','Eimal Khan','Not Recieved (Failed)\n'),(23,'25/06/2025','02:51:06 PM','COD','Refunded','185400','Ajmal Khan','Refunded Successfully\n'),(24,'25/06/2025','02:51:22 PM','Paypal','Pending','154200','Omid Khan','Transaction on Pending\n'),(25,'25/06/2025','02:51:40 PM','Paypal','In Progress','1754100','Abdul Jamil','Transaction in Progress\n'),(26,'25/06/2025','02:52:11 PM','COD','Completed','195000','Abdul Karim','Transaction Completed Successfully\n\n'),(27,'30/06/2025','04:50:22 PM','Master Card','Completed','12000','Amir iqbal khan','completed successfully\n'),(28,'15/07/2025','01:02:39 AM','Master Card','Completed','12000','Amir Iqbal Khan','Transaction Completed');
/*!40000 ALTER TABLE `transaction_data` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-12-02  0:41:03
