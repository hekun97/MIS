-- 如果存在这些表就删除掉这些表格
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS team;
DROP TABLE IF EXISTS department;
DROP TABLE IF EXISTS position;
DROP TABLE IF EXISTS leave;
DROP TABLE IF EXISTS company;

-- 员工信息表
CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  sex TEXT DEFAULT '男',
  email TEXT NOT NULL,
  tel INTEGER NOT NULL,
  level TEXT NOT NULL,
  money INTEGER NOT NULL,
  birthday TEXT NOT NULL,
  work_begin_day TEXT NOT NULL,
  team_id INTEGER,
  pt_id INTEGER,
  dp_id INTEGER
);

-- 团队信息表
CREATE TABLE team (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  team_name TEXT UNIQUE NOT NULL,
  team_describe TEXT NOT NULL
);
-- 部门信息表
CREATE TABLE department (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  dp_name TEXT UNIQUE NOT NULL,
  dp_describe TEXT NOT NULL
);
-- 职位信息表
CREATE TABLE position (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  pt_name TEXT UNIQUE NOT NULL,
  pt_describe TEXT NOT NULL
);
-- 请假信息表
CREATE TABLE leave (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT NOT NULL,
  leave_name TEXT NOT NULL,
  begin_time TEXT NOT NULL,
  end_time TEXT NOT NULL,
  leave_time TEXT NOT NULL,
  leave_describe TEXT NOT NULL,
  allow_name TEXT DEFAULT '无',
  allow_level TEXT DEFAULT '未批复',
  not_allow_describe TEXT DEFAULT '无'
);

-- 公司信息表
CREATE TABLE company(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  cp_title TEXT NOT NULL,
  cp_body TEXT NOT NULL,
  cp_created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  author_id INTEGER,
  cp_level TEXT DEFAULT '普通内容'
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
  (
    '中小型人力资源管理系统',
    '欢迎使用中小型人力资源管理系统',
    '首页信息'
  ),
  ('公司介绍', '以下内容为公司的相关介绍', '更多信息');