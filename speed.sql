SET NAMES utf8;

CREATE DATABASE IF NOT EXISTS speed DEFAULT CHARACTER SET utf8;

-- 用户表
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

-- 菜单表
CREATE TABLE speed.menu (
    uid int unsigned AUTO_INCREMENT,
	fname VARCHAR(20) NOT NULL UNIQUE,
	fprice VARCHAR(50) NOT NULL,
    finfor VARCHAR(255) NOT NULL,
    picture VARCHAR(255) NOT NULL,
    PRIMARY KEY (uid)
) ENGINE=InnoDB AUTO_INCREMENT=1001 DEFAULT CHARSET=utf8;

-- 测试
-- INSERT INTO menu values (DEFAULT, "哈密瓜", "23.5", "一款赞不绝口的蛋糕", "static/img/image/1.jpg");
-- INSERT INTO menu values (DEFAULT, "西瓜", "20.0", "一款好吃的的蛋糕", "static/img/image/2.jpg");

-- CREATE USER 'azhe'@'127.0.0.1' IDENTIFIED BY '123456';
-- GRANT ALL ON mydb.* to 'dj'@'127.0.0.1';
-- FLUSH PRIVILEGES;
