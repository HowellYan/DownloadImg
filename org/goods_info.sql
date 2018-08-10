/*
 Navicat Premium Data Transfer

 Source Server         : rm-wz9w6sgg78t2319s5mo.mysql.rds.aliyuncs.com
 Source Server Type    : MySQL
 Source Server Version : 50720
 Source Host           : rm-wz9w6sgg78t2319s5mo.mysql.rds.aliyuncs.com:3306
 Source Schema         : luckwine-goods

 Target Server Type    : MySQL
 Target Server Version : 50720
 File Encoding         : 65001

 Date: 10/08/2018 20:16:00
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for goods_info
-- ----------------------------
DROP TABLE IF EXISTS `goods_info`;
CREATE TABLE `goods_info` (
  `id` bigint(20) NOT NULL COMMENT '商品id',
  `goods_name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '商品名称',
  `sub_title` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '副标题',
  `goods_type` varchar(3) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '商品分类',
  `place_origin` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '产地',
  `price` decimal(12,2) NOT NULL DEFAULT '0.00' COMMENT '价格',
  `cover` varchar(1500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '封面',
  `ingesting time` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '醒酒时间',
  `bottle_stopper` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '瓶塞',
  `scent` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '香味',
  `grape_variety` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '葡萄品种',
  `collocation_food` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '搭配美食',
  `storage_conditions` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '储藏条件',
  `taste` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '口感',
  `net_content` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '净含量',
  `color` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '色泽',
  `carton_size` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '箱规',
  `introduce` longtext COLLATE utf8mb4_unicode_ci COMMENT '介绍',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

SET FOREIGN_KEY_CHECKS = 1;
