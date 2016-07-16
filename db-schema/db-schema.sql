DROP DATABASE if exists pydelo;
create database pydelo;
use pydelo;
set names utf8;

DROP TABLE if exists `sessions`;
CREATE TABLE `sessions` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int(10) unsigned NOT NULL,
  `session` varchar(32) NOT NULL,
  `expired` TIMESTAMP NOT NULL COMMENT 'expired time',
  `created_at` datetime NOT NULL COMMENT 'create time',
  `updated_at` datetime NOT NULL COMMENT 'update time',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE if exists `users`;
CREATE TABLE `users` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(32) NOT NULL,
  `password` varchar(64) NOT NULL,
  `role` int(10) unsigned DEFAULT NULL,
  `email` varchar(64) DEFAULT '',
  `phone` varchar(16) DEFAULT '',
  `apikey` varchar(64) NOT NULL,
  `created_at` datetime NOT NULL COMMENT 'create time',
  `updated_at` datetime NOT NULL COMMENT 'update time',
  PRIMARY KEY (`id`),
  UNIQUE KEY `name_key` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE if exists `projects`;
CREATE TABLE `projects` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL COMMENT '项目名称',
  `repo_url` varchar(200) NOT NULL COMMENT '项目git库地址',
  `checkout_dir` varchar(200) NOT NULL COMMENT '源代码检出目录',
  `target_dir` varchar(200) NOT NULL COMMENT '部署文件存放目录',
  `deploy_dir` varchar(200) NOT NULL COMMENT '部署机器上的目标目录',
  `deploy_history_dir` varchar(200) NOT NULL COMMENT '部署机器上的历史版本目录',
  `before_checkout` text ,
  `after_checkout` text ,
  `before_deploy` text ,
  `after_deploy` text ,
  `before_rollback` text,
  `after_rollback` text,
  `created_at` datetime NOT NULL COMMENT 'create time',
  `updated_at` datetime NOT NULL COMMENT 'update time',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE if exists `hosts`;
CREATE TABLE `hosts` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL,
  `ssh_host` varchar(32) NOT NULL,
  `ssh_port` int(10) unsigned NOT NULL,
  `ssh_user` varchar(64) NOT NULL,
  `ssh_pass` varchar(100) NOT NULL,
  `created_at` datetime NOT NULL COMMENT 'create time',
  `updated_at` datetime NOT NULL COMMENT 'update time',
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE if exists `rel_user_project`;
CREATE TABLE `rel_user_project` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int(10) unsigned NOT NULL,
  `project_id` int(10) unsigned NOT NULL,
  `created_at` datetime NOT NULL COMMENT 'create time',
  `updated_at` datetime NOT NULL COMMENT 'update time',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE if exists `rel_user_host`;
CREATE TABLE `rel_user_host` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int(10) unsigned NOT NULL,
  `host_id` int(10) unsigned NOT NULL,
  `created_at` datetime NOT NULL COMMENT 'create time',
  `updated_at` datetime NOT NULL COMMENT 'update time',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE if exists `deploys`;
CREATE TABLE `deploys` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int(10) unsigned NOT NULL,
  `project_id` int(10) unsigned NOT NULL,
  `host_id` int(10) unsigned NOT NULL,
  `mode` int(10) unsigned NOT NULL COMMENT '0:branch;1:tag;2:rollback',
  `branch` varchar(32) NOT NULL,
  `version` varchar(32) NOT NULL,
  `progress` int(10) unsigned NOT NULL COMMENT '',
  `status` int(1) unsigned NOT NULL COMMENT '0:fail, 1:success, 2:running',
  `softln_filename` varchar(64) NOT NULL,
  `comment` text ,
  `created_at` datetime NOT NULL COMMENT 'create time',
  `updated_at` datetime NOT NULL COMMENT 'update time',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
