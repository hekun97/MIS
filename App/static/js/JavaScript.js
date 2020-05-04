// user
var user_Boolean = false;
var password_Boolean = false;
var money_Boolenan = false;
var emaile_Boolean = false;
var Mobile_Boolean = false;
// user
// 只含有汉字、数字、字母、下划线不能以下划线开头和结尾：
// ^(?!_)(?!.*?_$)[a-zA-Z0-9_\u4e00-\u9fa5]+$
$(document).ready(function () {
  $('.reg_user').blur(function () {
    if ((/^(?!_)(?!.*?_$)[a-zA-Z0-9_\u4e00-\u9fa5]+$/).test($(".reg_user").val())) {
      $('.user_hint').html("✔").css("color", "green");
      user_Boolean = true;
    } else {
      $('.user_hint').html("×").css("color", "red");
      user_Boolean = false;
    }
  });
  // password
  // 密码长度为6到16位包含数字及大小写字母和符号
  $('.reg_password').blur(function () {
    if ((/^[a-zA-Z0-9_-]{6,16}$/).test($(".reg_password").val())) {
      $('.password_hint').html("✔").css("color", "green");
      password_Boolean = true;
    } else {
      $('.password_hint').html("×").css("color", "red");
      password_Boolean = false;
    }
  });

  // money
  // 只包含数字
  $('.reg_money').blur(function () {
    if ((/^(0|[1-9][0-9]*)(\.\d+)?$/).test($(".reg_money").val())) {
      $('.money_hint').html("✔").css("color", "green");
      money_Boolean = true;
    } else {
      $('.money_hint').html("×").css("color", "red");
      money_Boolean = false;
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
      emaile_Boolean = true;
    } else {
      $('.email_hint').html("×").css("color", "red");
      emaile_Boolean = false;
    }
  });


  // Mobile
  //^1[35678]\d{9}$
  // 以1开头，第二位未3，5，6，7，8中的一位，后面9位为数字
  $('.reg_mobile').blur(function () {
    if ((/^1[35678]\d{9}$/).test($(".reg_mobile").val())) {
      $('.mobile_hint').html("✔").css("color", "green");
      Mobile_Boolean = true;
    } else {
      $('.mobile_hint').html("×").css("color", "red");
      Mobile_Boolean = false;
    }
  });


  // click
  $('.red_button').click(function () {
    if (user_Boolean && password_Boolea && money_Boolenan && emaile_Boolean && Mobile_Boolean == true) {}
    // 阻止提交表单
    else {
      $("form").submit(function (e) {
        e.preventDefault();
        alert("请按要求填写表单");
      });
    }
  });
});