CREATE DATABASE IF NOT EXISTS slack_thing;

CREATE TABLE IF NOT EXISTS `commands` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `path_id` varchar(45) DEFAULT NULL,
  `command` varchar(45) DEFAULT NULL,
  `workflow_id` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;

CREATE TABLE IF NOT EXISTS `users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `slack_user_id` VARCHAR(45) NULL,
  `slack_team_id` VARCHAR(45) NULL,
  `email` VARCHAR(45) NULL,
  `name` VARCHAR(45) NULL,
  `profile_img` VARCHAR(45) NULL,
  `access_token` VARCHAR(45) NULL,
  PRIMARY KEY (`id`));

CREATE TABLE IF NOT EXISTS `workflows` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `workflow_id` varchar(45) DEFAULT NULL,
  `trigger_id` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;

CREATE TABLE IF NOT EXISTS `wf_steps` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `wf_id` varchar(45) DEFAULT NULL,
  `step_id` varchar(45) DEFAULT NULL,
  `action` varchar(45) DEFAULT NULL,
  `message` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;

CREATE TABLE IF NOT EXISTS `wf_branches` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `step_id` varchar(45) DEFAULT NULL,
  `action_id` varchar(45) DEFAULT NULL,
  `next_step_id` varchar(45) DEFAULT NULL,
  `text` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;

CREATE TABLE IF NOT EXISTS `wf_options` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `step_id` varchar(45) DEFAULT NULL,
  `name` varchar(45) DEFAULT NULL,
  `value` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;
