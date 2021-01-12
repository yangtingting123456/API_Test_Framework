/*
Navicat MySQL Data Transfer

Source Server         : 127.0.0.1
Source Server Version : 80022
Source Host           : 127.0.0.1:3306
Source Database       : interface_test_db

Target Server Type    : MYSQL
Target Server Version : 80022
File Encoding         : 65001

Date: 2021-01-12 16:51:12
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for case_info
-- ----------------------------
DROP TABLE IF EXISTS `case_info`;
CREATE TABLE `case_info` (
  `case_id` varchar(20) NOT NULL,
  `case_name` varchar(1000) NOT NULL,
  `is_run` varchar(4) NOT NULL DEFAULT '是',
  PRIMARY KEY (`case_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of case_info
-- ----------------------------
INSERT INTO `case_info` VALUES ('api_case_01', '获取access_token接口', '是');
INSERT INTO `case_info` VALUES ('api_case_02', '创建标签接口', '是');
INSERT INTO `case_info` VALUES ('api_case_03', '删除标签接口', '是');

-- ----------------------------
-- Table structure for case_step_info
-- ----------------------------
DROP TABLE IF EXISTS `case_step_info`;
CREATE TABLE `case_step_info` (
  `case_id` varchar(20) NOT NULL,
  `case_step_id` varchar(20) DEFAULT NULL,
  `requests_id` varchar(20) DEFAULT NULL,
  `get_value_type` varchar(20) DEFAULT NULL,
  `get_value_code` varchar(1000) DEFAULT NULL,
  `get_value_variable` varchar(20) DEFAULT NULL,
  `excepted_result_type` varchar(20) DEFAULT NULL,
  `excepted_result` varchar(1000) DEFAULT NULL,
  KEY `fk_case` (`case_id`),
  CONSTRAINT `fk_case` FOREIGN KEY (`case_id`) REFERENCES `case_info` (`case_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of case_step_info
-- ----------------------------
INSERT INTO `case_step_info` VALUES ('api_case_01', 'step_id_01', 'api_001', '无', '', '', 'body_regexp', '\"access_token\":\"(.+?)\"');
INSERT INTO `case_step_info` VALUES ('api_case_02', 'step_id_01', 'api_001', '正则取值', '\"access_token\":\"(.+?)\"', 'token', 'json_key_value', '{\"expires_in\":7200}');
INSERT INTO `case_step_info` VALUES ('api_case_02', 'step_id_02', 'api_002', '无', '', '', 'json_key', 'tag');
INSERT INTO `case_step_info` VALUES ('api_case_03', 'step_id_01', 'api_001', 'jsonpath取值', '$.access_token', 'token', 'json_key', 'access_token');
INSERT INTO `case_step_info` VALUES ('api_case_03', 'step_id_02', 'api_002', '正则取值', '\"id\":(.+?),', 'tag_id', 'json_key', 'tag');
INSERT INTO `case_step_info` VALUES ('api_case_03', 'step_id_03', 'api_003', '无', '', '', 'json_key_value', '{\"errcode\":0}');

-- ----------------------------
-- Table structure for requests_info
-- ----------------------------
DROP TABLE IF EXISTS `requests_info`;
CREATE TABLE `requests_info` (
  `requests_id` varchar(20) NOT NULL,
  `requests_name` varchar(200) NOT NULL,
  `requests_type` varchar(20) NOT NULL,
  `requests_header` varchar(1000) DEFAULT NULL,
  `requests_url` varchar(250) NOT NULL,
  `requests_url_params` varchar(1000) DEFAULT NULL,
  `requests_post_data` varchar(1000) DEFAULT NULL,
  PRIMARY KEY (`requests_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of requests_info
-- ----------------------------
INSERT INTO `requests_info` VALUES ('api_001', '获取access_token接口测试', 'get', '', '/cgi-bin/token', '{\"grant_type\":\"client_credential\",\"appid\":\"wxf26ad2ae7497289a\",\"secret\":\"177931a321a1f39a47a1ef202d8a3497\"}', '');
INSERT INTO `requests_info` VALUES ('api_002', '创建标签接口测试', 'post', '', '/cgi-bin/tags/create', '{\"access_token\":${token}}', '{\"tag\":{\"name\" :\"33ff6f\"}}');
INSERT INTO `requests_info` VALUES ('api_003', '删除标签接口测试', 'post', '', '/cgi-bin/tags/delete', '{\"access_token\":${token}}', '{\"tag\":{ \"id\":${tag_id}}}');
