-- 创建数据库
-- CREATE DATABASE interface_test_db;

-- 使用数据库
-- USER interface_test_db;

-- 创建接口信息表
--  CREATE TABLE requests_info(
--  requests_id VARCHAR(20),
--  requests_name VARCHAR(200) NOT NULL,
--  requests_type VARCHAR(20) NOT NULL,
--  requests_header VARCHAR(1000),
--  requests_url VARCHAR(250) NOT NULL,
--  requests_url_params VARCHAR(1000),
--  requests_post_data VARCHAR(1000),
--  PRIMARY KEY(requests_id)
--  )DEFAULT CHARSET = 'utf8';

-- 创建测试用例表
-- CREATE TABLE case_info(
--  case_id VARCHAR(20),
--  case_name VARCHAR(1000) NOT NULL,
-- is_run VARCHAR(4) NOT NULL DEFAULT '是',
--  PRIMARY KEY(case_id)
-- )DEFAULT CHARSET = 'utf8';

-- 创建测试用例步骤表
-- CREATE TABLE case_step_info(
-- case_id VARCHAR(20) NOT NULL,
-- case_step_id VARCHAR(20),
-- requests_id VARCHAR(20),
-- get_value_type VARCHAR(20),
-- get_value_code VARCHAR(1000),
-- get_value_variable VARCHAR(20),
-- excepted_result_type VARCHAR(20),
-- excepted_result VARCHAR(1000),
-- CONSTRAINT fk_case FOREIGN KEY(case_id) REFERENCES case_info(case_id)
-- )DEFAULT CHARSET = 'utf8';

-- case_info 表中插入数据
-- INSERT INTO case_info VALUES('api_case_01','获取access_token接口测试','是');
-- INSERT INTO case_info VALUES('api_case_02','创建标签接口测试','是');
-- INSERT INTO case_info VALUES('api_case_03','删除标签接口测试','是');

-- requests_info 表中插入数据
-- INSERT INTO requests_info VALUES('api_001','获取access_token接口测试','get','','/cgi-bin/token','{"grant_type":"client_credential","appid":"wxf26ad2ae7497289a","secret":"177931a321a1f39a47a1ef202d8a3497"}','');
-- INSERT INTO requests_info VALUES('api_002','创建标签接口测试','post','','/cgi-bin/tags/create','{"access_token":${token}','{"tag":{"name":"dfgdfg"}}');
-- INSERT INTO requests_info VALUES('api_003','删除标签接口测试','post','','/cgi-bin/token','{"access_token":${token}','{"tag":{ "id":${tag_id}}}');

-- case_step_info 表中插入数据

-- INSERT INTO case_step_info VALUES('api_case_01','step_id_01','api_001','无','','','body_regexp','"access_token":"(.+?)"');
-- 
-- INSERT INTO case_step_info VALUES('api_case_02','step_id_01','api_001','正则取值','"access_token":"(.+?)"','token','json_key_value','{"expires_in":7200}');
-- INSERT INTO case_step_info VALUES('api_case_02','step_id_02','api_002','无','','','json_key','tag');
-- 
-- INSERT INTO case_step_info VALUES('api_case_03','step_id_01','api_001','jsonpath取值','$.access_token','token','json_key','access_token');
-- INSERT INTO case_step_info VALUES('api_case_03','step_id_02','api_002','正则取值','"id":(.+?)','tag_id','json_key','');
-- INSERT INTO case_step_info VALUES('api_case_03','step_id_03','api_003','无','','','json_key_value','{"errcode":0}');

-- 三张表联查
-- select * from case_info,case_step_info,requests_info
-- where case_info.case_id = case_step_info.case_id and case_step_info.requests_id = requests_info.requests_id and case_info.is_run = '是'
-- order by case_info.case_id,case_step_info.case_step_id;