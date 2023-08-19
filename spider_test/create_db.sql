CREATE DATABASE IF NOT EXISTS `spider_db`;

CREATE USER 'spider' IDENTIFIED BY 'spider';
GRANT ALL ON *.* TO 'spider';
