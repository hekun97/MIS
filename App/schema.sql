-- 如果存在这些表就删除掉这些表格
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS team;
DROP TABLE IF EXISTS department;
DROP TABLE IF EXISTS position;
DROP TABLE IF EXISTS leave;
DROP TABLE IF EXISTS company;
DROP TABLE IF EXISTS reward;
DROP TABLE IF EXISTS punishment;
DROP TABLE IF EXISTS clock;
DROP TABLE IF EXISTS train;
-- 团队信息表
CREATE TABLE team (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  team_name TEXT UNIQUE NOT NULL,
  team_describe TEXT
);
-- 部门信息表
CREATE TABLE department (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  dp_name TEXT UNIQUE NOT NULL,
  dp_describe TEXT
);
-- 职位信息表
CREATE TABLE position (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  pt_name TEXT UNIQUE NOT NULL,
  pt_describe TEXT
);
-- 请假信息表
CREATE TABLE leave (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT NOT NULL,
  leave_name TEXT,
  begin_time TEXT,
  end_time TEXT,
  leave_time TEXT,
  leave_describe TEXT,
  allow_name TEXT DEFAULT '无',
  allow_level TEXT DEFAULT '未批复',
  not_allow_describe TEXT DEFAULT '无'
);
-- 员工信息表
CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  sex TEXT DEFAULT '男',
  email TEXT,
  tel INTEGER,
  level TEXT,
  status TEXT,
  money INTEGER,
  birthday TEXT,
  work_begin_day TEXT,
  team_id INTEGER,
  pt_id INTEGER,
  dp_id INTEGER
);
-- 奖励信息表
CREATE TABLE reward (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  rw_title TEXT,
  rw_describe TEXT,
  rw_id INTEGER
);
-- 惩罚信息表
CREATE TABLE punishment (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  pi_title TEXT,
  pi_describe TEXT,
  pi_id INTEGER
);
-- 打卡信息表
CREATE TABLE clock (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  ck_time TEXT,
  ck_place TEXT,
  ck_describe TEXT,
  ck_id INTEGER
);
-- 公司信息表
CREATE TABLE company(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  cp_title TEXT,
  cp_body TEXT,
  cp_created TEXT,
  author_id TEXT,
  cp_level TEXT DEFAULT '普通内容'
);
-- 培训信息表
CREATE TABLE train(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  train_title TEXT,
  train_body TEXT,
  train_begin_time TEXT,
  train_end_time TEXT,
  train_time TEXT,
  train_status TEXT DEFAULT '未批复',
  join_id INTEGER,
  author_id INTEGER,
  create_time TEXT
);
PRAGMA foreign_keys = ON;
INSERT INTO user (
    username,
    password,
    sex,
    email,
    tel,
    level,
    money,
    birthday,
    work_begin_day
  )
VALUES
  (
    'admin',
    'pbkdf2:sha256:150000$WJZyFqb0$672ec7509564f6ba42ea4c0dc580cf6628d96f66aa63c201595c372b980c0af9',
    '男',
    'hekun97@outlook.com',
    18883681286,
    '管理员',
    2000,
    '1997-12-12',
    '2016-09-01'
  );
INSERT INTO company (cp_title, cp_body, cp_level)
VALUES
  ('中小型人力资源管理系统', '欢迎使用中小型人力资源管理系统', '首页信息'),
  ('公司介绍', '以下内容为公司的相关介绍', '更多信息');