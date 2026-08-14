-- ========================================================
-- Exported from SQLite to MySQL Workbench (With Foreign Keys)
-- Database: mine_inventory
-- ========================================================

SET FOREIGN_KEY_CHECKS = 0;
SET NAMES utf8mb4;
SET TIME_ZONE = '+00:00';

CREATE DATABASE IF NOT EXISTS `mine_inventory` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE `mine_inventory`;

-- --------------------------------------------------------
-- Table structure for `django_migrations`
-- --------------------------------------------------------
DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE `django_migrations` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `app` VARCHAR(255) NOT NULL,
  `name` VARCHAR(255) NOT NULL,
  `applied` DATETIME NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Data for `django_migrations` (26 rows)
INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
  (1, 'contenttypes', '0001_initial', '2026-08-14 15:16:34.660474'),
  (2, 'auth', '0001_initial', '2026-08-14 15:16:34.677428'),
  (3, 'admin', '0001_initial', '2026-08-14 15:16:34.692839'),
  (4, 'admin', '0002_logentry_remove_auto_add', '2026-08-14 15:16:34.708523'),
  (5, 'admin', '0003_logentry_add_action_flag_choices', '2026-08-14 15:16:34.716825'),
  (6, 'almacenamiento', '0001_initial', '2026-08-14 15:16:34.731615'),
  (7, 'contenttypes', '0002_remove_content_type_name', '2026-08-14 15:16:34.748571'),
  (8, 'auth', '0002_alter_permission_name_max_length', '2026-08-14 15:16:34.760699'),
  (9, 'auth', '0003_alter_user_email_max_length', '2026-08-14 15:16:34.771543'),
  (10, 'auth', '0004_alter_user_username_opts', '2026-08-14 15:16:34.782537'),
  (11, 'auth', '0005_alter_user_last_login_null', '2026-08-14 15:16:34.794990'),
  (12, 'auth', '0006_require_contenttypes_0002', '2026-08-14 15:16:34.799575'),
  (13, 'auth', '0007_alter_validators_add_error_messages', '2026-08-14 15:16:34.809060'),
  (14, 'auth', '0008_alter_user_username_max_length', '2026-08-14 15:16:34.821837'),
  (15, 'auth', '0009_alter_user_last_name_max_length', '2026-08-14 15:16:34.833165'),
  (16, 'auth', '0010_alter_group_name_max_length', '2026-08-14 15:16:34.846857'),
  (17, 'auth', '0011_update_proxy_permissions', '2026-08-14 15:16:34.857695'),
  (18, 'auth', '0012_alter_user_first_name_max_length', '2026-08-14 15:16:34.869790'),
  (19, 'configuracion', '0001_initial', '2026-08-14 15:16:34.877120'),
  (20, 'usuario', '0001_initial', '2026-08-14 15:16:34.884083'),
  (21, 'inventario', '0001_initial', '2026-08-14 15:16:34.908446'),
  (22, 'prestamo', '0001_initial', '2026-08-14 15:16:34.924829'),
  (23, 'devoluciones', '0001_initial', '2026-08-14 15:16:34.941406'),
  (24, 'mantenimiento', '0001_initial', '2026-08-14 15:16:34.976064'),
  (25, 'reportes', '0001_initial', '2026-08-14 15:16:34.984101'),
  (26, 'sessions', '0001_initial', '2026-08-14 15:16:34.996439');

-- --------------------------------------------------------
-- Table structure for `auth_group_permissions`
-- --------------------------------------------------------
DROP TABLE IF EXISTS `auth_group_permissions`;
CREATE TABLE `auth_group_permissions` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `group_id` INT NOT NULL,
  `permission_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `fk_auth_group_permissions_permission_id_1` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_auth_group_permissions_group_id_2` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------
-- Table structure for `auth_user_groups`
-- --------------------------------------------------------
DROP TABLE IF EXISTS `auth_user_groups`;
CREATE TABLE `auth_user_groups` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `user_id` INT NOT NULL,
  `group_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `fk_auth_user_groups_group_id_1` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_auth_user_groups_user_id_2` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------
-- Table structure for `auth_user_user_permissions`
-- --------------------------------------------------------
DROP TABLE IF EXISTS `auth_user_user_permissions`;
CREATE TABLE `auth_user_user_permissions` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `user_id` INT NOT NULL,
  `permission_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `fk_auth_user_user_permissions_permission_id_1` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_auth_user_user_permissions_user_id_2` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------
-- Table structure for `django_admin_log`
-- --------------------------------------------------------
DROP TABLE IF EXISTS `django_admin_log`;
CREATE TABLE `django_admin_log` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `object_id` TEXT,
  `object_repr` VARCHAR(200) NOT NULL,
  `action_flag` INT NOT NULL,
  `change_message` TEXT NOT NULL,
  `content_type_id` INT,
  `user_id` INT NOT NULL,
  `action_time` DATETIME NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `fk_django_admin_log_user_id_1` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_django_admin_log_content_type_id_2` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------
-- Table structure for `almacen`
-- --------------------------------------------------------
DROP TABLE IF EXISTS `almacen`;
CREATE TABLE `almacen` (
  `codigo_almacen` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(100) NOT NULL,
  `dimensiones` VARCHAR(100),
  `ubicacion` VARCHAR(255),
  PRIMARY KEY (`codigo_almacen`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------
-- Table structure for `estante`
-- --------------------------------------------------------
DROP TABLE IF EXISTS `estante`;
CREATE TABLE `estante` (
  `num_estante` INT NOT NULL AUTO_INCREMENT,
  `codigo` VARCHAR(50) NOT NULL,
  `dimensiones` VARCHAR(100),
  `codigo_almacen` INT NOT NULL,
  PRIMARY KEY (`num_estante`),
  CONSTRAINT `fk_estante_codigo_almacen_1` FOREIGN KEY (`codigo_almacen`) REFERENCES `almacen` (`codigo_almacen`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------
-- Table structure for `existencia`
-- --------------------------------------------------------
DROP TABLE IF EXISTS `existencia`;
CREATE TABLE `existencia` (
  `codigo_existencias` INT NOT NULL AUTO_INCREMENT,
  `cantidad` INT NOT NULL,
  `responsable` VARCHAR(100),
  `fecha_creacion` DATE,
  `observaciones` TEXT,
  `num_estante` INT NOT NULL,
  PRIMARY KEY (`codigo_existencias`),
  CONSTRAINT `fk_existencia_num_estante_1` FOREIGN KEY (`num_estante`) REFERENCES `estante` (`num_estante`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------
-- Table structure for `django_content_type`
-- --------------------------------------------------------
DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE `django_content_type` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `app_label` VARCHAR(100) NOT NULL,
  `model` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Data for `django_content_type` (27 rows)
INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
  (1, 'admin', 'logentry'),
  (2, 'auth', 'group'),
  (3, 'auth', 'permission'),
  (4, 'auth', 'user'),
  (5, 'contenttypes', 'contenttype'),
  (6, 'sessions', 'session'),
  (7, 'devoluciones', 'devolucionherramienta'),
  (8, 'usuario', 'usuario'),
  (9, 'prestamo', 'detalleprestamo'),
  (10, 'prestamo', 'prestamo'),
  (11, 'inventario', 'categoriaherramienta'),
  (12, 'inventario', 'detalletraslado'),
  (13, 'inventario', 'herramienta'),
  (14, 'inventario', 'proveedor'),
  (15, 'inventario', 'suministro'),
  (16, 'inventario', 'traslado'),
  (17, 'almacenamiento', 'almacen'),
  (18, 'almacenamiento', 'estante'),
  (19, 'almacenamiento', 'existencia'),
  (20, 'mantenimiento', 'bitacoraestado'),
  (21, 'mantenimiento', 'detallemantenimiento'),
  (22, 'mantenimiento', 'mantenimiento'),
  (23, 'mantenimiento', 'mantenimientocambio'),
  (24, 'mantenimiento', 'tipoestado'),
  (25, 'mantenimiento', 'tipomantenimiento'),
  (26, 'reportes', 'reportehistorial'),
  (27, 'configuracion', 'configuracionsistema');

-- --------------------------------------------------------
-- Table structure for `auth_permission`
-- --------------------------------------------------------
DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE `auth_permission` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `content_type_id` INT NOT NULL,
  `codename` VARCHAR(100) NOT NULL,
  `name` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `fk_auth_permission_content_type_id_1` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Data for `auth_permission` (108 rows)
INSERT INTO `auth_permission` (`id`, `content_type_id`, `codename`, `name`) VALUES
  (1, 1, 'add_logentry', 'Can add log entry'),
  (2, 1, 'change_logentry', 'Can change log entry'),
  (3, 1, 'delete_logentry', 'Can delete log entry'),
  (4, 1, 'view_logentry', 'Can view log entry'),
  (5, 3, 'add_permission', 'Can add permission'),
  (6, 3, 'change_permission', 'Can change permission'),
  (7, 3, 'delete_permission', 'Can delete permission'),
  (8, 3, 'view_permission', 'Can view permission'),
  (9, 2, 'add_group', 'Can add group'),
  (10, 2, 'change_group', 'Can change group'),
  (11, 2, 'delete_group', 'Can delete group'),
  (12, 2, 'view_group', 'Can view group'),
  (13, 4, 'add_user', 'Can add user'),
  (14, 4, 'change_user', 'Can change user'),
  (15, 4, 'delete_user', 'Can delete user'),
  (16, 4, 'view_user', 'Can view user'),
  (17, 5, 'add_contenttype', 'Can add content type'),
  (18, 5, 'change_contenttype', 'Can change content type'),
  (19, 5, 'delete_contenttype', 'Can delete content type'),
  (20, 5, 'view_contenttype', 'Can view content type'),
  (21, 6, 'add_session', 'Can add session'),
  (22, 6, 'change_session', 'Can change session'),
  (23, 6, 'delete_session', 'Can delete session'),
  (24, 6, 'view_session', 'Can view session'),
  (25, 7, 'add_devolucionherramienta', 'Can add Devolución de Herramienta'),
  (26, 7, 'change_devolucionherramienta', 'Can change Devolución de Herramienta'),
  (27, 7, 'delete_devolucionherramienta', 'Can delete Devolución de Herramienta'),
  (28, 7, 'view_devolucionherramienta', 'Can view Devolución de Herramienta'),
  (29, 8, 'add_usuario', 'Can add Usuario'),
  (30, 8, 'change_usuario', 'Can change Usuario'),
  (31, 8, 'delete_usuario', 'Can delete Usuario'),
  (32, 8, 'view_usuario', 'Can view Usuario'),
  (33, 10, 'add_prestamo', 'Can add Préstamo'),
  (34, 10, 'change_prestamo', 'Can change Préstamo'),
  (35, 10, 'delete_prestamo', 'Can delete Préstamo'),
  (36, 10, 'view_prestamo', 'Can view Préstamo'),
  (37, 9, 'add_detalleprestamo', 'Can add Detalle de préstamo'),
  (38, 9, 'change_detalleprestamo', 'Can change Detalle de préstamo'),
  (39, 9, 'delete_detalleprestamo', 'Can delete Detalle de préstamo'),
  (40, 9, 'view_detalleprestamo', 'Can view Detalle de préstamo'),
  (41, 11, 'add_categoriaherramienta', 'Can add Categoría de Herramienta'),
  (42, 11, 'change_categoriaherramienta', 'Can change Categoría de Herramienta'),
  (43, 11, 'delete_categoriaherramienta', 'Can delete Categoría de Herramienta'),
  (44, 11, 'view_categoriaherramienta', 'Can view Categoría de Herramienta'),
  (45, 14, 'add_proveedor', 'Can add Proveedor'),
  (46, 14, 'change_proveedor', 'Can change Proveedor'),
  (47, 14, 'delete_proveedor', 'Can delete Proveedor'),
  (48, 14, 'view_proveedor', 'Can view Proveedor'),
  (49, 13, 'add_herramienta', 'Can add Herramienta'),
  (50, 13, 'change_herramienta', 'Can change Herramienta'),
  (51, 13, 'delete_herramienta', 'Can delete Herramienta'),
  (52, 13, 'view_herramienta', 'Can view Herramienta'),
  (53, 15, 'add_suministro', 'Can add Suministro'),
  (54, 15, 'change_suministro', 'Can change Suministro'),
  (55, 15, 'delete_suministro', 'Can delete Suministro'),
  (56, 15, 'view_suministro', 'Can view Suministro'),
  (57, 16, 'add_traslado', 'Can add Traslado'),
  (58, 16, 'change_traslado', 'Can change Traslado'),
  (59, 16, 'delete_traslado', 'Can delete Traslado'),
  (60, 16, 'view_traslado', 'Can view Traslado'),
  (61, 12, 'add_detalletraslado', 'Can add Detalle de Traslado'),
  (62, 12, 'change_detalletraslado', 'Can change Detalle de Traslado'),
  (63, 12, 'delete_detalletraslado', 'Can delete Detalle de Traslado'),
  (64, 12, 'view_detalletraslado', 'Can view Detalle de Traslado'),
  (65, 17, 'add_almacen', 'Can add Almacén'),
  (66, 17, 'change_almacen', 'Can change Almacén'),
  (67, 17, 'delete_almacen', 'Can delete Almacén'),
  (68, 17, 'view_almacen', 'Can view Almacén'),
  (69, 18, 'add_estante', 'Can add Estante'),
  (70, 18, 'change_estante', 'Can change Estante'),
  (71, 18, 'delete_estante', 'Can delete Estante'),
  (72, 18, 'view_estante', 'Can view Estante'),
  (73, 19, 'add_existencia', 'Can add Existencia'),
  (74, 19, 'change_existencia', 'Can change Existencia'),
  (75, 19, 'delete_existencia', 'Can delete Existencia'),
  (76, 19, 'view_existencia', 'Can view Existencia'),
  (77, 23, 'add_mantenimientocambio', 'Can add mantenimiento cambio'),
  (78, 23, 'change_mantenimientocambio', 'Can change mantenimiento cambio'),
  (79, 23, 'delete_mantenimientocambio', 'Can delete mantenimiento cambio'),
  (80, 23, 'view_mantenimientocambio', 'Can view mantenimiento cambio'),
  (81, 24, 'add_tipoestado', 'Can add tipo estado'),
  (82, 24, 'change_tipoestado', 'Can change tipo estado'),
  (83, 24, 'delete_tipoestado', 'Can delete tipo estado'),
  (84, 24, 'view_tipoestado', 'Can view tipo estado'),
  (85, 25, 'add_tipomantenimiento', 'Can add tipo mantenimiento'),
  (86, 25, 'change_tipomantenimiento', 'Can change tipo mantenimiento'),
  (87, 25, 'delete_tipomantenimiento', 'Can delete tipo mantenimiento'),
  (88, 25, 'view_tipomantenimiento', 'Can view tipo mantenimiento'),
  (89, 22, 'add_mantenimiento', 'Can add Mantenimiento'),
  (90, 22, 'change_mantenimiento', 'Can change Mantenimiento'),
  (91, 22, 'delete_mantenimiento', 'Can delete Mantenimiento'),
  (92, 22, 'view_mantenimiento', 'Can view Mantenimiento'),
  (93, 21, 'add_detallemantenimiento', 'Can add Detalle de Mantenimiento'),
  (94, 21, 'change_detallemantenimiento', 'Can change Detalle de Mantenimiento'),
  (95, 21, 'delete_detallemantenimiento', 'Can delete Detalle de Mantenimiento'),
  (96, 21, 'view_detallemantenimiento', 'Can view Detalle de Mantenimiento'),
  (97, 20, 'add_bitacoraestado', 'Can add Bitácora de Estado'),
  (98, 20, 'change_bitacoraestado', 'Can change Bitácora de Estado'),
  (99, 20, 'delete_bitacoraestado', 'Can delete Bitácora de Estado'),
  (100, 20, 'view_bitacoraestado', 'Can view Bitácora de Estado');
INSERT INTO `auth_permission` (`id`, `content_type_id`, `codename`, `name`) VALUES
  (101, 26, 'add_reportehistorial', 'Can add Historial de Reporte'),
  (102, 26, 'change_reportehistorial', 'Can change Historial de Reporte'),
  (103, 26, 'delete_reportehistorial', 'Can delete Historial de Reporte'),
  (104, 26, 'view_reportehistorial', 'Can view Historial de Reporte'),
  (105, 27, 'add_configuracionsistema', 'Can add Configuración del sistema'),
  (106, 27, 'change_configuracionsistema', 'Can change Configuración del sistema'),
  (107, 27, 'delete_configuracionsistema', 'Can delete Configuración del sistema'),
  (108, 27, 'view_configuracionsistema', 'Can view Configuración del sistema');

-- --------------------------------------------------------
-- Table structure for `auth_group`
-- --------------------------------------------------------
DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE `auth_group` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(150) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------
-- Table structure for `auth_user`
-- --------------------------------------------------------
DROP TABLE IF EXISTS `auth_user`;
CREATE TABLE `auth_user` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `password` VARCHAR(128) NOT NULL,
  `last_login` DATETIME,
  `is_superuser` TINYINT(1) NOT NULL,
  `username` VARCHAR(150) NOT NULL,
  `last_name` VARCHAR(150) NOT NULL,
  `email` VARCHAR(254) NOT NULL,
  `is_staff` TINYINT(1) NOT NULL,
  `is_active` TINYINT(1) NOT NULL,
  `date_joined` DATETIME NOT NULL,
  `first_name` VARCHAR(150) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------
-- Table structure for `configuracion_configuracionsistema`
-- --------------------------------------------------------
DROP TABLE IF EXISTS `configuracion_configuracionsistema`;
CREATE TABLE `configuracion_configuracionsistema` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `almacenamiento` VARCHAR(10) NOT NULL,
  `database_url` TEXT NOT NULL,
  `actualizado_en` DATETIME NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------
-- Table structure for `usuario`
-- --------------------------------------------------------
DROP TABLE IF EXISTS `usuario`;
CREATE TABLE `usuario` (
  `documento` VARCHAR(20) NOT NULL,
  `primer_nombre` VARCHAR(50) NOT NULL,
  `segundo_nombre` VARCHAR(50),
  `primer_apellido` VARCHAR(50) NOT NULL,
  `segundo_apellido` VARCHAR(50),
  `correo_personal` VARCHAR(100),
  `telefono` VARCHAR(20),
  `tipo_documento` VARCHAR(30),
  `programa` VARCHAR(100),
  `ficha` VARCHAR(50),
  PRIMARY KEY (`documento`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------
-- Table structure for `categoria_herramienta`
-- --------------------------------------------------------
DROP TABLE IF EXISTS `categoria_herramienta`;
CREATE TABLE `categoria_herramienta` (
  `codigo_categoria` INT NOT NULL AUTO_INCREMENT,
  `tipo_herramienta` VARCHAR(100),
  `nombre_categoria` VARCHAR(100) NOT NULL,
  `descripcion` TEXT,
  PRIMARY KEY (`codigo_categoria`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------
-- Table structure for `proveedor`
-- --------------------------------------------------------
DROP TABLE IF EXISTS `proveedor`;
CREATE TABLE `proveedor` (
  `codigo_proveedor` INT NOT NULL AUTO_INCREMENT,
  `nit_proveedor` VARCHAR(50),
  `telefono_contacto` VARCHAR(20),
  `correo_proveedor` VARCHAR(100),
  `descripcion` TEXT,
  PRIMARY KEY (`codigo_proveedor`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------
-- Table structure for `herramienta`
-- --------------------------------------------------------
DROP TABLE IF EXISTS `herramienta`;
CREATE TABLE `herramienta` (
  `codigo_herramienta` INT NOT NULL AUTO_INCREMENT,
  `codigo_SKU` VARCHAR(50),
  `nombre_herramienta` VARCHAR(100) NOT NULL,
  `descripcion` TEXT,
  `disponibilidad` VARCHAR(50),
  `fecha_ingreso` DATE,
  `codigo_categoria` INT NOT NULL,
  PRIMARY KEY (`codigo_herramienta`),
  CONSTRAINT `fk_herramienta_codigo_categoria_1` FOREIGN KEY (`codigo_categoria`) REFERENCES `categoria_herramienta` (`codigo_categoria`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------
-- Table structure for `suministro`
-- --------------------------------------------------------
DROP TABLE IF EXISTS `suministro`;
CREATE TABLE `suministro` (
  `codigo_suministro` INT NOT NULL AUTO_INCREMENT,
  `fecha` DATE NOT NULL,
  `cantidad` INT NOT NULL,
  `observaciones` TEXT,
  `codigo_herramienta` INT NOT NULL,
  `codigo_inventario` INT,
  `codigo_proveedor` INT NOT NULL,
  PRIMARY KEY (`codigo_suministro`),
  CONSTRAINT `fk_suministro_codigo_proveedor_1` FOREIGN KEY (`codigo_proveedor`) REFERENCES `proveedor` (`codigo_proveedor`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_suministro_codigo_inventario_2` FOREIGN KEY (`codigo_inventario`) REFERENCES `existencia` (`codigo_existencias`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_suministro_codigo_herramienta_3` FOREIGN KEY (`codigo_herramienta`) REFERENCES `herramienta` (`codigo_herramienta`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------
-- Table structure for `traslado`
-- --------------------------------------------------------
DROP TABLE IF EXISTS `traslado`;
CREATE TABLE `traslado` (
  `codigo_traslado` INT NOT NULL AUTO_INCREMENT,
  `cantidad_total` INT NOT NULL,
  `tipo_movimiento` VARCHAR(50),
  `fecha_movimiento` DATE NOT NULL,
  `observaciones` TEXT,
  `codigo_inventario` INT,
  PRIMARY KEY (`codigo_traslado`),
  CONSTRAINT `fk_traslado_codigo_inventario_1` FOREIGN KEY (`codigo_inventario`) REFERENCES `existencia` (`codigo_existencias`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------
-- Table structure for `detalle_traslado`
-- --------------------------------------------------------
DROP TABLE IF EXISTS `detalle_traslado`;
CREATE TABLE `detalle_traslado` (
  `codigo_detalle` INT NOT NULL AUTO_INCREMENT,
  `cantidad` INT NOT NULL,
  `observaciones` TEXT,
  `codigo_herramienta` INT NOT NULL,
  `codigo_traslado` INT NOT NULL,
  PRIMARY KEY (`codigo_detalle`),
  CONSTRAINT `fk_detalle_traslado_codigo_traslado_1` FOREIGN KEY (`codigo_traslado`) REFERENCES `traslado` (`codigo_traslado`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_detalle_traslado_codigo_herramienta_2` FOREIGN KEY (`codigo_herramienta`) REFERENCES `herramienta` (`codigo_herramienta`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------
-- Table structure for `prestamo`
-- --------------------------------------------------------
DROP TABLE IF EXISTS `prestamo`;
CREATE TABLE `prestamo` (
  `codigo_prestamo` INT NOT NULL AUTO_INCREMENT,
  `observaciones` TEXT,
  `estado` VARCHAR(50),
  `fecha` DATE NOT NULL,
  `documento` VARCHAR(20) NOT NULL,
  PRIMARY KEY (`codigo_prestamo`),
  CONSTRAINT `fk_prestamo_documento_1` FOREIGN KEY (`documento`) REFERENCES `usuario` (`documento`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------
-- Table structure for `detalle_prestamo`
-- --------------------------------------------------------
DROP TABLE IF EXISTS `detalle_prestamo`;
CREATE TABLE `detalle_prestamo` (
  `numero_detalle` INT NOT NULL AUTO_INCREMENT,
  `observaciones` TEXT,
  `cantidad` INT NOT NULL,
  `codigo_herramienta` INT NOT NULL,
  `codigo_prestamo` INT NOT NULL,
  PRIMARY KEY (`numero_detalle`),
  CONSTRAINT `fk_detalle_prestamo_codigo_prestamo_1` FOREIGN KEY (`codigo_prestamo`) REFERENCES `prestamo` (`codigo_prestamo`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_detalle_prestamo_codigo_herramienta_2` FOREIGN KEY (`codigo_herramienta`) REFERENCES `herramienta` (`codigo_herramienta`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------
-- Table structure for `devolucion_herramientas`
-- --------------------------------------------------------
DROP TABLE IF EXISTS `devolucion_herramientas`;
CREATE TABLE `devolucion_herramientas` (
  `codigo_devolucion` INT NOT NULL AUTO_INCREMENT,
  `observaciones` TEXT,
  `fecha` DATE NOT NULL,
  `codigo_prestamo` INT NOT NULL,
  `codigo_recibe` VARCHAR(20) NOT NULL,
  PRIMARY KEY (`codigo_devolucion`),
  CONSTRAINT `fk_devolucion_herramientas_codigo_recibe_1` FOREIGN KEY (`codigo_recibe`) REFERENCES `usuario` (`documento`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_devolucion_herramientas_codigo_prestamo_2` FOREIGN KEY (`codigo_prestamo`) REFERENCES `prestamo` (`codigo_prestamo`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------
-- Table structure for `mantenimiento`
-- --------------------------------------------------------
DROP TABLE IF EXISTS `mantenimiento`;
CREATE TABLE `mantenimiento` (
  `num_mantenimiento` INT NOT NULL AUTO_INCREMENT,
  `tipo_mantenimiento` VARCHAR(50),
  `fecha_ingreso` DATE NOT NULL,
  `fecha_salida` DATE,
  `observaciones` TEXT,
  `codigo_herramienta` INT NOT NULL,
  PRIMARY KEY (`num_mantenimiento`),
  CONSTRAINT `fk_mantenimiento_codigo_herramienta_1` FOREIGN KEY (`codigo_herramienta`) REFERENCES `herramienta` (`codigo_herramienta`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------
-- Table structure for `detalle_mantenimiento`
-- --------------------------------------------------------
DROP TABLE IF EXISTS `detalle_mantenimiento`;
CREATE TABLE `detalle_mantenimiento` (
  `detalle_mantenimiento` INT NOT NULL AUTO_INCREMENT,
  `accion_realizada` TEXT,
  `materiales_usados` TEXT,
  `fecha_mantenimiento` DATE NOT NULL,
  `observacion` TEXT,
  `num_mantenimiento` INT NOT NULL,
  PRIMARY KEY (`detalle_mantenimiento`),
  CONSTRAINT `fk_detalle_mantenimiento_num_mantenimiento_1` FOREIGN KEY (`num_mantenimiento`) REFERENCES `mantenimiento` (`num_mantenimiento`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------
-- Table structure for `bitacora_estado`
-- --------------------------------------------------------
DROP TABLE IF EXISTS `bitacora_estado`;
CREATE TABLE `bitacora_estado` (
  `codigo_bitacora` INT NOT NULL AUTO_INCREMENT,
  `descripcion` TEXT,
  `estado` VARCHAR(50),
  `nivel_estado` VARCHAR(50),
  `num_mantenimiento` INT NOT NULL,
  PRIMARY KEY (`codigo_bitacora`),
  CONSTRAINT `fk_bitacora_estado_num_mantenimiento_1` FOREIGN KEY (`num_mantenimiento`) REFERENCES `mantenimiento` (`num_mantenimiento`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------
-- Table structure for `reportes_reportehistorial`
-- --------------------------------------------------------
DROP TABLE IF EXISTS `reportes_reportehistorial`;
CREATE TABLE `reportes_reportehistorial` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `modulo` VARCHAR(30) NOT NULL,
  `formato` VARCHAR(10) NOT NULL,
  `nombre_archivo` VARCHAR(255) NOT NULL,
  `generado_por` VARCHAR(150) NOT NULL,
  `fecha_generado` DATETIME NOT NULL,
  `total_registros` INT NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------
-- Table structure for `django_session`
-- --------------------------------------------------------
DROP TABLE IF EXISTS `django_session`;
CREATE TABLE `django_session` (
  `session_key` VARCHAR(40) NOT NULL,
  `session_data` TEXT NOT NULL,
  `expire_date` DATETIME NOT NULL,
  PRIMARY KEY (`session_key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

SET FOREIGN_KEY_CHECKS = 1;
