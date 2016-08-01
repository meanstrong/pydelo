USE pydelo;
ALTER TABLE `projects` ADD `target_dir` varchar(200) NOT NULL COMMENT '部署文件build后目标目录' AFTER `checkout_dir`;
UPDATE `projects` SET `target_dir` = `checkout_dir`;
ALTER TABLE `projects` DROP COLUMN `before_rollback`;
ALTER TABLE `projects` DROP COLUMN `after_rollback`;
