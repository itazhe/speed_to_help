SET NAMES utf8;

CREATE DATABASE IF NOT EXISTS speed DEFAULT CHARACTER SET utf8;

CREATE TABLE speed.user (
    uid int unsigned AUTO_INCREMENT,
    uname varchar(20) NOT NULL UNIQUE,
    upass char(32) NOT NULL,  -- md5加密
    phone char(11) NOT NULL, 
    email varchar(320),
    reg_time datetime NOT NULL,
    last_login_time datetime NOT NULL,
    priv enum ('1', '2') NOT NULL DEFAULT '1',  -- 1表示为普通用户，2表示为后台管理员
    state enum ('0', '1', '2', '3') NOT NULL DEFAULT '1',  -- 0表示已删除，1表示正常，2表示冻结，3表示异常
    PRIMARY KEY (uid)
) ENGINE=InnoDB AUTO_INCREMENT=1001 DEFAULT CHARSET=utf8;

-- 内置管理员账户
INSERT INTO user values (DEFAULT, 'root', md5('234567890'), '13476491560', 'az@azhe.net.cn', now(), now(), 2, 1);


-- CREATE TABLE speed.ruser (
-- 	rname VARCHAR(255) NOT NULL,
-- 	passwd VARCHAR(50) NOT NULL,
-- )
-- CREATE USER 'azhe'@'127.0.0.1' IDENTIFIED BY '123456';
-- GRANT ALL ON mydb.* to 'dj'@'127.0.0.1';
-- FLUSH PRIVILEGES;
