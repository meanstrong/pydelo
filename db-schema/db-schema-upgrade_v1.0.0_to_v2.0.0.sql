USE pydelo;
ALTER TABLE `projects` ADD `target_dir` varchar(200) NOT NULL COMMENT '部署文件build后目标目录' AFTER `checkout_dir`;
UPDATE `projects` SET `target_dir` = `checkout_dir`;
ALTER TABLE `projects` DROP COLUMN `before_rollback`;
ALTER TABLE `projects` DROP COLUMN `after_rollback`;
ALTER TABLE `deploys` CHANGE `status` `status` int(1) unsigned NOT NULL COMMENT '0-fail;1-success;2-running;3-waiting';

ALTER TABLE `hosts` ADD `ssh_method` TINYINT(1) NOT NULL DEFAULT 0 COMMENT '0-password;1-public key' AFTER `ssh_user`;
