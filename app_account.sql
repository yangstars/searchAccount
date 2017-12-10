/*
Navicat MySQL Data Transfer

Source Server         : 本地
Source Server Version : 50720
Source Host           : localhost:3306
Source Database       : py

Target Server Type    : MYSQL
Target Server Version : 50720
File Encoding         : 65001

Date: 2017-12-10 13:30:10
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for app_account
-- ----------------------------
DROP TABLE IF EXISTS `app_account`;
CREATE TABLE `app_account` (
  `id` bigint(24) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `user_id` bigint(24) NOT NULL COMMENT '用户id',
  `app_name` varchar(24) NOT NULL COMMENT '应用名',
  `app_account` varchar(255) DEFAULT NULL COMMENT 'app账号',
  `app_pwd` varchar(255) DEFAULT NULL COMMENT '登陆密码',
  `app_mail` varchar(255) DEFAULT NULL COMMENT '注册邮箱',
  `app_phone` varchar(255) DEFAULT NULL COMMENT '手机号',
  `create_time` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `update_time` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
