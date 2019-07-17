-- phpMyAdmin SQL Dump
-- version 3.4.5
-- http://www.phpmyadmin.net
--
-- 主机: localhost
-- 生成日期: 2016 年 03 月 25 日 09:53
-- 服务器版本: 5.5.16
-- PHP 版本: 5.3.8

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- 数据库: `dutylist`
--

-- --------------------------------------------------------

-- 表的结构 `du_link`
--

CREATE TABLE IF NOT EXISTS `du_link` (
  `link_id` int(11) NOT NULL AUTO_INCREMENT,
  `link_name` varchar(64) NOT NULL,
  `link_address` varchar(64) NOT NULL,
  `link_belong_service` varchar(64) NOT NULL,
  `update_time`  varchar(256) NOT NULL,
  PRIMARY KEY (`link_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------
-- --------------------------------------------------------

-- 表的结构 `du_case`
--

CREATE TABLE IF NOT EXISTS `du_case` (
  `caseid` int(11) NOT NULL AUTO_INCREMENT,
  `casename` varchar(512) NOT NULL,
  `case_param` varchar(5000) NOT NULL,
  `case_belong_suite` varchar(64) NOT NULL,
  `create_user` varchar(64) NOT NULL,
  `create_time`  varchar(256) NOT NULL,
  `update_time`  timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`caseid`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------


--
-- 表的结构 `du_category`
--

CREATE TABLE IF NOT EXISTS `du_category` (
  `category_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL,
  PRIMARY KEY (`category_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=7 ;

-- --------------------------------------------------------

--
-- 表的结构 `du_duty`
--

CREATE TABLE IF NOT EXISTS `du_duty` (
  `duty_id` int(11) NOT NULL AUTO_INCREMENT,
  `category_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `title` varchar(1024) NOT NULL,
  `status` int(2) NOT NULL,
  `is_show` int(2) NOT NULL COMMENT '是否公开',
  `update_time`  varchar(256) NOT NULL,
  PRIMARY KEY (`duty_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=3 ;

-- --------------------------------------------------------

--
-- 表的结构 `du_user`
--

CREATE TABLE IF NOT EXISTS `du_user` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(64) NOT NULL,
  `phone` varchar(16) NOT NULL,
  `password` varchar(64) NOT NULL,
  `update_time` varchar(256) DEFAULT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=16 ;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
