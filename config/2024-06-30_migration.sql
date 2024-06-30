CREATE DATABASE IF NOT EXISTS slack_thing;

CREATE TABLE IF NOT EXISTS `commands` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `path_id` varchar(45) DEFAULT NULL,
  `command` varchar(45) DEFAULT NULL,
  `workflow_id` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;
