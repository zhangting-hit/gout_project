/*
 Navicat Premium Data Transfer

 Source Server         : localhost_3306
 Source Server Type    : MySQL
 Source Server Version : 80030
 Source Host           : localhost:3306
 Source Schema         : graduation_project

 Target Server Type    : MySQL
 Target Server Version : 80030
 File Encoding         : 65001

 Date: 26/05/2024 20:59:21
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for image
-- ----------------------------
DROP TABLE IF EXISTS `image`;
CREATE TABLE `image`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `upload_time` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `imagePath` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `patient_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `location` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `dzghs` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `hmzh` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `tfsxc` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `gzph` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `gjjy` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `sgz` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 8161 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of image
-- ----------------------------
INSERT INTO `image` VALUES (8041, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/10283674_GOUT_1_0_12.png', '10283674', '0', '1', '1', '0', '0', '0', '0');
INSERT INTO `image` VALUES (8042, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/10283674_GOUT_3_0_0.png', '10283674', '0', '0', '0', '0', '0', '0', '0');
INSERT INTO `image` VALUES (8043, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/10283674_GOUT_4_0_12.png', '10283674', '0', '1', '1', '0', '0', '0', '0');
INSERT INTO `image` VALUES (8044, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/10283674_GOUT_5_0_2.png', '10283674', '0', '0', '1', '0', '0', '0', '0');
INSERT INTO `image` VALUES (8045, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/10283674_GOUT_6_0_0.png', '10283674', '0', '0', '0', '0', '0', '0', '0');
INSERT INTO `image` VALUES (8046, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/10283674_GOUT_7_1_3.png', '10283674', '1', '0', '0', '1', '0', '0', '0');
INSERT INTO `image` VALUES (8047, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/10283674_GOUT_8_1_3.png', '10283674', '1', '0', '0', '1', '0', '0', '0');
INSERT INTO `image` VALUES (8048, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/10283674_GOUT_9_1_3.png', '10283674', '1', '0', '0', '1', '0', '0', '0');
INSERT INTO `image` VALUES (8049, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/10283674_GOUT_10_1_3.png', '10283674', '1', '0', '0', '1', '0', '0', '0');
INSERT INTO `image` VALUES (8050, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/10283674_GOUT_11_2_0.png', '10283674', '2', '0', '0', '0', '0', '0', '0');
INSERT INTO `image` VALUES (8051, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/10283674_GOUT_12_2_0.png', '10283674', '2', '0', '0', '0', '0', '0', '0');
INSERT INTO `image` VALUES (8052, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/10283674_GOUT_13_2_0.png', '10283674', '2', '0', '0', '0', '0', '0', '0');
INSERT INTO `image` VALUES (8053, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/10283674_GOUT_14_2_6.png', '10283674', '2', '0', '0', '0', '0', '0', '1');
INSERT INTO `image` VALUES (8054, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/1847410_GOUT_1_0_0.png', '1847410', '0', '0', '0', '0', '0', '0', '0');
INSERT INTO `image` VALUES (8055, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/1847410_GOUT_2_0_0.png', '1847410', '0', '0', '0', '0', '0', '0', '0');
INSERT INTO `image` VALUES (8056, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/1847410_GOUT_3_0_0.png', '1847410', '0', '0', '0', '0', '0', '0', '0');
INSERT INTO `image` VALUES (8057, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/1847410_GOUT_4_1_134.png', '1847410', '1', '1', '0', '1', '1', '0', '0');
INSERT INTO `image` VALUES (8058, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/1847410_GOUT_5_1_134.png', '1847410', '1', '1', '0', '1', '1', '0', '0');
INSERT INTO `image` VALUES (8059, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/1847410_GOUT_6_1_134.png', '1847410', '1', '1', '0', '1', '1', '0', '0');
INSERT INTO `image` VALUES (8060, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/1847410_GOUT_7_1_134.png', '1847410', '1', '1', '0', '1', '1', '0', '0');
INSERT INTO `image` VALUES (8061, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/1847410_GOUT_8_1_134.png', '1847410', '1', '1', '0', '1', '1', '0', '0');
INSERT INTO `image` VALUES (8062, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/1847410_GOUT_9_2_0.png', '1847410', '2', '0', '0', '0', '0', '0', '0');
INSERT INTO `image` VALUES (8063, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/1847410_GOUT_10_2_0.png', '1847410', '2', '0', '0', '0', '0', '0', '0');
INSERT INTO `image` VALUES (8064, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/1847410_GOUT_11_2_0.png', '1847410', '2', '0', '0', '0', '0', '0', '0');
INSERT INTO `image` VALUES (8065, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/1847410_GOUT_12_2_0.png', '1847410', '2', '0', '0', '0', '0', '0', '0');
INSERT INTO `image` VALUES (8066, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/299281_GOUT_1_0_2.png', '299281', '0', '0', '1', '0', '0', '0', '0');
INSERT INTO `image` VALUES (8067, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/299281_GOUT_2_0_2.png', '299281', '0', '0', '1', '0', '0', '0', '0');
INSERT INTO `image` VALUES (8068, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/299281_GOUT_3_0_2.png', '299281', '0', '0', '1', '0', '0', '0', '0');
INSERT INTO `image` VALUES (8069, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/299281_GOUT_4_0_2.png', '299281', '0', '0', '1', '0', '0', '0', '0');
INSERT INTO `image` VALUES (8070, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/299281_GOUT_5_0_2.png', '299281', '0', '0', '1', '0', '0', '0', '0');
INSERT INTO `image` VALUES (8071, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/299281_GOUT_6_0_2.png', '299281', '0', '0', '1', '0', '0', '0', '0');
INSERT INTO `image` VALUES (8072, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/299281_GOUT_7_1_134.png', '299281', '1', '1', '0', '1', '1', '0', '0');
INSERT INTO `image` VALUES (8073, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/299281_GOUT_8_1_134.png', '299281', '1', '1', '0', '1', '1', '0', '0');
INSERT INTO `image` VALUES (8074, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/299281_GOUT_9_1_134.png', '299281', '1', '1', '0', '1', '1', '0', '0');
INSERT INTO `image` VALUES (8075, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/299281_GOUT_10_1_134.png', '299281', '1', '1', '0', '1', '1', '0', '0');
INSERT INTO `image` VALUES (8076, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/299281_GOUT_11_1_134.png', '299281', '1', '1', '0', '1', '1', '0', '0');
INSERT INTO `image` VALUES (8077, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/299281_GOUT_12_2_6.png', '299281', '2', '0', '0', '0', '0', '0', '1');
INSERT INTO `image` VALUES (8078, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/299281_GOUT_13_2_6.png', '299281', '2', '0', '0', '0', '0', '0', '1');
INSERT INTO `image` VALUES (8079, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/299281_GOUT_14_2_6.png', '299281', '2', '0', '0', '0', '0', '0', '1');
INSERT INTO `image` VALUES (8080, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/299281_GOUT_15_2_6.png', '299281', '2', '0', '0', '0', '0', '0', '1');
INSERT INTO `image` VALUES (8081, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/299281_GOUT_16_1_13.png', '299281', '1', '1', '0', '1', '0', '0', '0');
INSERT INTO `image` VALUES (8082, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/299281_GOUT_17_1_13.png', '299281', '1', '1', '0', '1', '0', '0', '0');
INSERT INTO `image` VALUES (8083, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/299281_GOUT_19_1_13.png', '299281', '1', '1', '0', '1', '0', '0', '0');
INSERT INTO `image` VALUES (8084, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/3644351_GOUT_1_0_12.png', '3644351', '0', '1', '1', '0', '0', '0', '0');
INSERT INTO `image` VALUES (8085, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/3644351_GOUT_2_0_12.png', '3644351', '0', '1', '1', '0', '0', '0', '0');
INSERT INTO `image` VALUES (8086, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/3644351_GOUT_3_0_12.png', '3644351', '0', '1', '1', '0', '0', '0', '0');
INSERT INTO `image` VALUES (8087, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/3644351_GOUT_4_0_12.png', '3644351', '0', '1', '1', '0', '0', '0', '0');
INSERT INTO `image` VALUES (8088, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/3644351_GOUT_5_1_134.png', '3644351', '1', '1', '0', '1', '1', '0', '0');
INSERT INTO `image` VALUES (8089, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/3644351_GOUT_6_1_14.png', '3644351', '1', '1', '0', '0', '1', '0', '0');
INSERT INTO `image` VALUES (8090, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/3644351_GOUT_7_1_134.png', '3644351', '1', '1', '0', '1', '1', '0', '0');
INSERT INTO `image` VALUES (8091, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/3644351_GOUT_8_1_146.png', '3644351', '1', '1', '0', '0', '1', '0', '1');
INSERT INTO `image` VALUES (8092, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/3644351_GOUT_9_2_0.png', '3644351', '2', '0', '0', '0', '0', '0', '0');
INSERT INTO `image` VALUES (8093, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/3644351_GOUT_10_2_0.png', '3644351', '2', '0', '0', '0', '0', '0', '0');
INSERT INTO `image` VALUES (8094, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/3644351_GOUT_11_2_0.png', '3644351', '2', '0', '0', '0', '0', '0', '0');
INSERT INTO `image` VALUES (8095, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/3644351_GOUT_13_1_134.png', '3644351', '1', '1', '0', '1', '1', '0', '0');
INSERT INTO `image` VALUES (8096, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/5319536_GOUT_11_2_6.png', '5319536', '2', '0', '0', '0', '0', '0', '1');
INSERT INTO `image` VALUES (8097, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/6812838_GOUT_1_0_2.png', '6812838', '0', '0', '1', '0', '0', '0', '0');
INSERT INTO `image` VALUES (8098, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/6812838_GOUT_2_0_2.png', '6812838', '0', '0', '1', '0', '0', '0', '0');
INSERT INTO `image` VALUES (8099, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/6812838_GOUT_3_0_2.png', '6812838', '0', '0', '1', '0', '0', '0', '0');
INSERT INTO `image` VALUES (8100, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/6812838_GOUT_4_0_12.png', '6812838', '0', '1', '1', '0', '0', '0', '0');
INSERT INTO `image` VALUES (8101, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/6812838_GOUT_5_1_1346.png', '6812838', '1', '1', '0', '1', '1', '0', '1');
INSERT INTO `image` VALUES (8102, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/6812838_GOUT_6_1_1346.png', '6812838', '1', '1', '0', '1', '1', '0', '1');
INSERT INTO `image` VALUES (8103, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/6812838_GOUT_7_1_136.png', '6812838', '1', '1', '0', '1', '0', '0', '1');
INSERT INTO `image` VALUES (8104, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/6812838_GOUT_8_1_16.png', '6812838', '1', '1', '0', '0', '0', '0', '1');
INSERT INTO `image` VALUES (8105, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/6812838_GOUT_9_1_13.png', '6812838', '1', '1', '0', '1', '0', '0', '0');
INSERT INTO `image` VALUES (8106, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/6812838_GOUT_10_1_14.png', '6812838', '1', '1', '0', '0', '1', '0', '0');
INSERT INTO `image` VALUES (8107, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/6812838_GOUT_11_1_14.png', '6812838', '1', '1', '0', '0', '1', '0', '0');
INSERT INTO `image` VALUES (8108, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/6812838_GOUT_12_2_0.png', '6812838', '2', '0', '0', '0', '0', '0', '0');
INSERT INTO `image` VALUES (8109, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/6812838_GOUT_13_2_0.png', '6812838', '2', '0', '0', '0', '0', '0', '0');
INSERT INTO `image` VALUES (8110, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/6812838_GOUT_14_2_0.png', '6812838', '2', '0', '0', '0', '0', '0', '0');
INSERT INTO `image` VALUES (8111, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/6812838_GOUT_15_2_0.png', '6812838', '2', '0', '0', '0', '0', '0', '0');
INSERT INTO `image` VALUES (8112, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/10223296_GOUT_1_0_0.png', '10223296', '0', '0', '0', '0', '0', '0', '0');
INSERT INTO `image` VALUES (8113, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/10223296_GOUT_2_0_0.png', '10223296', '0', '0', '0', '0', '0', '0', '0');
INSERT INTO `image` VALUES (8114, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/10223296_GOUT_3_0_0.png', '10223296', '0', '0', '0', '0', '0', '0', '0');
INSERT INTO `image` VALUES (8115, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/10223296_GOUT_4_0_0.png', '10223296', '0', '0', '0', '0', '0', '0', '0');
INSERT INTO `image` VALUES (8116, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/10223296_GOUT_5_1_0.png', '10223296', '1', '0', '0', '0', '0', '0', '0');
INSERT INTO `image` VALUES (8117, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/10223296_GOUT_6_1_0.png', '10223296', '1', '0', '0', '0', '0', '0', '0');
INSERT INTO `image` VALUES (8118, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/10223296_GOUT_7_1_0.png', '10223296', '1', '0', '0', '0', '0', '0', '0');
INSERT INTO `image` VALUES (8119, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/10223296_GOUT_8_1_0.png', '10223296', '1', '0', '0', '0', '0', '0', '0');
INSERT INTO `image` VALUES (8120, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/10223296_GOUT_9_1_0.png', '10223296', '1', '0', '0', '0', '0', '0', '0');
INSERT INTO `image` VALUES (8121, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/10223296_GOUT_10_1_0.png', '10223296', '1', '0', '0', '0', '0', '0', '0');
INSERT INTO `image` VALUES (8122, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/10223296_GOUT_11_1_0.png', '10223296', '1', '0', '0', '0', '0', '0', '0');
INSERT INTO `image` VALUES (8123, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/10223296_GOUT_12_2_6.png', '10223296', '2', '0', '0', '0', '0', '0', '1');
INSERT INTO `image` VALUES (8124, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/10223296_GOUT_13_2_0.png', '10223296', '2', '0', '0', '0', '0', '0', '0');
INSERT INTO `image` VALUES (8125, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/10223296_GOUT_14_2_0.png', '10223296', '2', '0', '0', '0', '0', '0', '0');
INSERT INTO `image` VALUES (8126, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/10223296_GOUT_15_2_6.png', '10223296', '2', '0', '0', '0', '0', '0', '1');
INSERT INTO `image` VALUES (8127, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/10223296_GOUT_16_1_0.png', '10223296', '1', '0', '0', '0', '0', '0', '0');
INSERT INTO `image` VALUES (8128, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/10223296_GOUT_17_0_0.png', '10223296', '0', '0', '0', '0', '0', '0', '0');
INSERT INTO `image` VALUES (8129, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/1847410_OB_1_0_0.png', '1847410', '0', '0', '0', '0', '0', '0', '0');
INSERT INTO `image` VALUES (8130, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/1847410_OB_2_0_0.png', '1847410', '0', '0', '0', '0', '0', '0', '0');
INSERT INTO `image` VALUES (8131, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/1847410_OB_3_0_0.png', '1847410', '0', '0', '0', '0', '0', '0', '0');
INSERT INTO `image` VALUES (8132, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/1847410_OB_4_0_0.png', '1847410', '0', '0', '0', '0', '0', '0', '0');
INSERT INTO `image` VALUES (8133, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/1847410_OB_5_1_0.png', '1847410', '1', '0', '0', '0', '0', '0', '0');
INSERT INTO `image` VALUES (8134, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/1847410_OB_6_1_0.png', '1847410', '1', '0', '0', '0', '0', '0', '0');
INSERT INTO `image` VALUES (8135, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/1847410_OB_7_1_0.png', '1847410', '1', '0', '0', '0', '0', '0', '0');
INSERT INTO `image` VALUES (8136, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/1847410_OB_8_1_0.png', '1847410', '1', '0', '0', '0', '0', '0', '0');
INSERT INTO `image` VALUES (8137, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/1847410_OB_9_2_0.png', '1847410', '2', '0', '0', '0', '0', '0', '0');
INSERT INTO `image` VALUES (8138, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/1847410_OB_10_2_0.png', '1847410', '2', '0', '0', '0', '0', '0', '0');
INSERT INTO `image` VALUES (8139, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/1847410_OB_11_2_0.png', '1847410', '2', '0', '0', '0', '0', '0', '0');
INSERT INTO `image` VALUES (8140, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/1847410_OB_12_2_0.png', '1847410', '2', '0', '0', '0', '0', '0', '0');
INSERT INTO `image` VALUES (8141, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/9233702_GOUT_1_0_1.png', '9233702', '0', '1', '0', '0', '0', '0', '0');
INSERT INTO `image` VALUES (8142, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/9233702_GOUT_2_0_1.png', '9233702', '0', '1', '0', '0', '0', '0', '0');
INSERT INTO `image` VALUES (8143, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/9233702_GOUT_3_0_0.png', '9233702', '0', '0', '0', '0', '0', '0', '0');
INSERT INTO `image` VALUES (8144, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/9233702_GOUT_4_0_1.png', '9233702', '0', '1', '0', '0', '0', '0', '0');
INSERT INTO `image` VALUES (8145, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/9233702_GOUT_5_1_1.png', '9233702', '1', '1', '0', '0', '0', '0', '0');
INSERT INTO `image` VALUES (8146, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/9233702_GOUT_6_1_0.png', '9233702', '1', '0', '0', '0', '0', '0', '0');
INSERT INTO `image` VALUES (8147, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/9233702_GOUT_7_1_0.png', '9233702', '1', '0', '0', '0', '0', '0', '0');
INSERT INTO `image` VALUES (8148, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/9233702_GOUT_8_1_13.png', '9233702', '1', '1', '0', '1', '0', '0', '0');
INSERT INTO `image` VALUES (8149, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/9233702_GOUT_9_1_13.png', '9233702', '1', '1', '0', '1', '0', '0', '0');
INSERT INTO `image` VALUES (8150, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/9233702_GOUT_10_2_0.png', '9233702', '2', '0', '0', '0', '0', '0', '0');
INSERT INTO `image` VALUES (8151, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/9233702_GOUT_11_2_0.png', '9233702', '2', '0', '0', '0', '0', '0', '0');
INSERT INTO `image` VALUES (8152, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/9233702_GOUT_12_2_0.png', '9233702', '2', '0', '0', '0', '0', '0', '0');
INSERT INTO `image` VALUES (8153, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/9233702_GOUT_13_1_13.png', '9233702', '1', '1', '0', '1', '0', '0', '0');
INSERT INTO `image` VALUES (8154, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/9233702_GOUT_14_1_13.png', '9233702', '1', '1', '0', '1', '0', '0', '0');
INSERT INTO `image` VALUES (8155, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/9233702_GOUT_15_1_3.png', '9233702', '1', '0', '0', '1', '0', '0', '0');
INSERT INTO `image` VALUES (8156, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/9233702_GOUT_16_1_13.png', '9233702', '1', '1', '0', '1', '0', '0', '0');
INSERT INTO `image` VALUES (8157, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/9233702_GOUT_17_2_0.png', '9233702', '2', '0', '0', '0', '0', '0', '0');
INSERT INTO `image` VALUES (8158, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/9233702_GOUT_18_2_0.png', '9233702', '2', '0', '0', '0', '0', '0', '0');
INSERT INTO `image` VALUES (8159, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/9233702_GOUT_19_1_13.png', '9233702', '1', '1', '0', '1', '0', '0', '0');
INSERT INTO `image` VALUES (8160, '2024-05-19', 'http://localhost:5000/static/images/DICOMDIR 5.26-6.1/9233702_GOUT_20_1_13.png', '9233702', '1', '1', '0', '1', '0', '0', '0');

-- ----------------------------
-- Table structure for menu
-- ----------------------------
DROP TABLE IF EXISTS `menu`;
CREATE TABLE `menu`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT 'id',
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '名称',
  `path` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '路径',
  `icon` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '图标',
  `description` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '描述',
  `pid` int NULL DEFAULT NULL COMMENT '父级id',
  `sort_num` int NULL DEFAULT NULL COMMENT '排序',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 49 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of menu
-- ----------------------------
INSERT INTO `menu` VALUES (1, '超声影像管理', NULL, 'el-icon-s-marketing', '11', NULL, 100);
INSERT INTO `menu` VALUES (2, '影像上传', '/home/upload', 'el-icon-upload', 'None', 1, 301);
INSERT INTO `menu` VALUES (3, '影像概况', '/home/imageBoard', 'el-icon-s-grid', 'No', 1, 300);
INSERT INTO `menu` VALUES (4, '病人概况', '/home/PatientBoard', 'el-icon-school', 'None', 1, NULL);
INSERT INTO `menu` VALUES (5, '影像查看', '/home/image', 'el-icon-picture', 'None', 1, 302);
INSERT INTO `menu` VALUES (6, '超声影像处理', NULL, 'el-icon-mouse', 'None', NULL, 303);
INSERT INTO `menu` VALUES (7, '影像检测', '/home/imageCheck', 'el-icon-view', 'None', 6, 304);
INSERT INTO `menu` VALUES (8, '影像分割', '/home/imageSegment', 'el-icon-crop', 'None', 6, 0);
INSERT INTO `menu` VALUES (9, '影像标注', '/home/imageLabel', 'el-icon-edit', 'None', 6, 201);
INSERT INTO `menu` VALUES (10, '系统设置', NULL, 'el-icon-setting', NULL, NULL, NULL);
INSERT INTO `menu` VALUES (11, '用户管理', '/home/user', 'el-icon-user', 'None', 10, 999);
INSERT INTO `menu` VALUES (12, '角色管理', '/home/role', 'el-icon-s-custom', 'None', 10, 999);
INSERT INTO `menu` VALUES (13, '菜单管理', '/home/menu', 'el-icon-menu', NULL, 10, 999);
INSERT INTO `menu` VALUES (14, '公告发布', '/home/notice', 'el-icon-position', 'None', 10, NULL);
INSERT INTO `menu` VALUES (15, '公告查看', '/home/noticeShow', 'el-icon-message', 'None', 10, NULL);
INSERT INTO `menu` VALUES (16, '模型管理', '/home/modelShow', 'el-icon-postcard', 'None', 10, NULL);

-- ----------------------------
-- Table structure for model
-- ----------------------------
DROP TABLE IF EXISTS `model`;
CREATE TABLE `model`  (
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `path` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `upload_time` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `upload_user` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `description` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `params` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `FPS` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `IOU` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `F1_value` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`name`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of model
-- ----------------------------
INSERT INTO `model` VALUES ('多分类模型', 'http://localhost:5000/static/64.03654485049834MLCepoch-180.pth', '2024-03-13', 'zt', '可一次识别多种病症', NULL, NULL, NULL, NULL);

-- ----------------------------
-- Table structure for notice
-- ----------------------------
DROP TABLE IF EXISTS `notice`;
CREATE TABLE `notice`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `content` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `author` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `created_at` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of notice
-- ----------------------------
INSERT INTO `notice` VALUES (1, 'unet模型已经更新', 'zt', '2024-03-20');
INSERT INTO `notice` VALUES (2, '检测模型更新', 'zt', '2024-03-21');

-- ----------------------------
-- Table structure for patient
-- ----------------------------
DROP TABLE IF EXISTS `patient`;
CREATE TABLE `patient`  (
  `patient_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`patient_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of patient
-- ----------------------------
INSERT INTO `patient` VALUES ('10223296');
INSERT INTO `patient` VALUES ('10283674');
INSERT INTO `patient` VALUES ('1847410');
INSERT INTO `patient` VALUES ('299281');
INSERT INTO `patient` VALUES ('3644351');
INSERT INTO `patient` VALUES ('5319536');
INSERT INTO `patient` VALUES ('6812838');
INSERT INTO `patient` VALUES ('9233702');

-- ----------------------------
-- Table structure for role
-- ----------------------------
DROP TABLE IF EXISTS `role`;
CREATE TABLE `role`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of role
-- ----------------------------
INSERT INTO `role` VALUES (1, 'admin');
INSERT INTO `role` VALUES (2, 'technician');
INSERT INTO `role` VALUES (3, 'medicine');
INSERT INTO `role` VALUES (4, 'user');

-- ----------------------------
-- Table structure for role_menu
-- ----------------------------
DROP TABLE IF EXISTS `role_menu`;
CREATE TABLE `role_menu`  (
  `role_id` int NOT NULL COMMENT '角色id',
  `menu_id` int NOT NULL COMMENT '菜单id',
  PRIMARY KEY (`role_id`, `menu_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '角色菜单关系表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of role_menu
-- ----------------------------
INSERT INTO `role_menu` VALUES (1, 1);
INSERT INTO `role_menu` VALUES (1, 2);
INSERT INTO `role_menu` VALUES (1, 3);
INSERT INTO `role_menu` VALUES (1, 4);
INSERT INTO `role_menu` VALUES (1, 5);
INSERT INTO `role_menu` VALUES (1, 6);
INSERT INTO `role_menu` VALUES (1, 7);
INSERT INTO `role_menu` VALUES (1, 8);
INSERT INTO `role_menu` VALUES (1, 9);
INSERT INTO `role_menu` VALUES (1, 10);
INSERT INTO `role_menu` VALUES (1, 11);
INSERT INTO `role_menu` VALUES (1, 12);
INSERT INTO `role_menu` VALUES (1, 13);
INSERT INTO `role_menu` VALUES (1, 14);
INSERT INTO `role_menu` VALUES (1, 15);
INSERT INTO `role_menu` VALUES (1, 16);
INSERT INTO `role_menu` VALUES (2, 1);
INSERT INTO `role_menu` VALUES (2, 2);
INSERT INTO `role_menu` VALUES (2, 3);
INSERT INTO `role_menu` VALUES (2, 4);
INSERT INTO `role_menu` VALUES (2, 5);
INSERT INTO `role_menu` VALUES (2, 6);
INSERT INTO `role_menu` VALUES (2, 7);
INSERT INTO `role_menu` VALUES (2, 8);
INSERT INTO `role_menu` VALUES (2, 9);
INSERT INTO `role_menu` VALUES (2, 10);
INSERT INTO `role_menu` VALUES (2, 14);
INSERT INTO `role_menu` VALUES (2, 15);
INSERT INTO `role_menu` VALUES (2, 16);
INSERT INTO `role_menu` VALUES (3, 1);
INSERT INTO `role_menu` VALUES (3, 2);
INSERT INTO `role_menu` VALUES (3, 3);
INSERT INTO `role_menu` VALUES (3, 4);
INSERT INTO `role_menu` VALUES (3, 5);
INSERT INTO `role_menu` VALUES (3, 6);
INSERT INTO `role_menu` VALUES (3, 7);
INSERT INTO `role_menu` VALUES (3, 8);
INSERT INTO `role_menu` VALUES (3, 9);
INSERT INTO `role_menu` VALUES (3, 10);
INSERT INTO `role_menu` VALUES (3, 15);

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `role` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `phone` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `avatarUrl` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 7 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` VALUES (1, 'zt', '123456', '1', '110', 'http://localhost:5000/static/Duola.png');
INSERT INTO `user` VALUES (2, 'zt1', '123456', '3', '111', 'http://localhost:5000/static/Duola.png');
INSERT INTO `user` VALUES (3, 'ztzt', '123456', NULL, '111', 'http://localhost:5000/static/Duola.png');
INSERT INTO `user` VALUES (4, 'tech1', '123456', 'None', '111', 'http://localhost:5000/static/Duola.png');
INSERT INTO `user` VALUES (5, 'admin', 'admin', 'None', '111', 'http://localhost:5000/static/Duola.png');
INSERT INTO `user` VALUES (6, 'admin', 'admin', '1', '111', 'http://localhost:5000/static/Duola.png');

SET FOREIGN_KEY_CHECKS = 1;
