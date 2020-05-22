var user = 0;
var password = 0;
var money = 0;
var emaile = 0;
var Mobile = 0;
$(document).ready(function () {
  // user
  // 只含有汉字、数字、字母、下划线不能以下划线开头和结尾：
  // ^(?!_)(?!.*?_$)[a-zA-Z0-9_\u4e00-\u9fa5]+$
  // blur():失去焦点的方法
  // test() 方法用于检测一个字符串是否匹配某个模式
  // val() 方法是value的简写，拿到其值
  $('.reg_user').blur(function () {
    if ((/^(?!_)(?!.*?_$)[a-zA-Z0-9_\u4e00-\u9fa5]+$/).test($(".reg_user").val())) {
      $('.user_hint').html("✔").css("color", "green");
      user = 1;
    } else {
      $('.user_hint').html("×").css("color", "red");
      user = 0;
    }
  });
  // password
  // 密码长度为6到16位包含数字及大小写字母和符号
  $('.reg_password').blur(function () {
    if ((/^[a-zA-Z0-9_-]{6,16}$/).test($(".reg_password").val())) {
      $('.password_hint').html("✔").css("color", "green");
      password = 1;
    } else {
      $('.password_hint').html("×").css("color", "red");
      password = 0;
    }
  });

  // money
  // 只包含正数
  $('.reg_money').blur(function () {
    if ((/^(0|[1-9][0-9]*)(\.\d+)?$/).test($(".reg_money").val())) {
      $('.money_hint').html("✔").css("color", "green");
      money = 1;
    } else {
      $('.money_hint').html("×").css("color", "red");
      money = 0;
    }
  });


  // Email
  // ^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}$
  // 0到19位可包含数字和大小写字母及下划线
  // 需包含@符号
  // @符号之后的可包含数字和大小写字母
  // .符号之后的可包含com,cn,net三种域名
  $('.reg_email').blur(function () {
    if ((/^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}$/).test($(".reg_email").val())) {
      $('.email_hint').html("✔").css("color", "green");
      emaile = 1;
    } else {
      $('.email_hint').html("×").css("color", "red");
      emaile = 0;
    }
  });


  // Mobile
  //^1[35678]\d{9}$
  // 以1开头，第二位未3，5，6，7，8中的一位，后面9位为数字
  $('.reg_mobile').blur(function () {
    if ((/^1[35678]\d{9}$/).test($(".reg_mobile").val())) {
      $('.mobile_hint').html("✔").css("color", "green");
      Mobile = 1;
    } else {
      $('.mobile_hint').html("×").css("color", "red");
      Mobile = 0;
    }
  });

  // click
  $('.red_button').click(function () {
    $('form').submit(function (event) {
      if (user == password == money == emaile == Mobile == 1) {} else {
        // 阻止表单提交事件
        event.preventDefault();
        $('.missing').html('<div class="missing alert alert-danger" role="alert">请按要求填写表单</div>')

      }
    });
  });
});