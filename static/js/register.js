/*
$(function () { ... }) 的含义
这是 jQuery 的文档就绪函数（document ready）的简写形式，完整写法是 $(document).ready(function(){...})。它的作用是：
    - 等待 DOM 完全加载：确保页面所有 HTML 元素都加载完成后再执行内部的 JavaScript 代码
    - 避免操作未加载的元素：防止脚本在 DOM 元素尚未存在时就尝试操作它们
    - 相当于原生 JS 的：window.onload = function(){...}，但 jQuery 的版本更高效
*/
$(function () {
    // 定义一个绑定函数
    function bindCaptchaBtnClick() {
        /*
        关于 $("#captcha-btn").click(function (event) { ... }) 的执行机制：
            - 绑定阶段（立即执行）
                - 当代码运行到 $("#captcha-btn").click(...) 时，
                    jQuery 会立即绑定点击事件处理函数（即 function(event) { ... } 里的代码）。
                - 但此时函数内部的代码不会执行，只是注册了一个回调函数，
                    告诉浏览器："当 #captcha-btn 被点击时，执行这个函数"。

            - 触发阶段（用户点击后执行）
                - 只有当用户真正点击了 #captcha-btn 按钮时，绑定的函数才会被执行。
                - 此时会传入一个 event 对象（包含点击事件的相关信息，如触发元素、坐标等）。
        */
        $("#captcha-btn").click(function (event) {
            let $this = $(this);
            let email = $("input[name='email']").val();
            if (!email) {
                alert("请先输入邮箱！");
                return;
            }
            // 取消按钮的点击事件
            $this.off('click');

            // 发送ajax请求
            $.ajax('/auth/captcha?email=' + email, {
                // 发送ajax请求
                method: 'GET',
                // 发送成功的回调函数
                success: function (result) {
                    if (result['code'] == 200) {
                        alert("验证码发送成功！");
                    } else {
                        alert(result['message']);
                    }
                },
                // 发送失败的回调函数
                fail: function (error) {
                    // console.log(error);
                }
            })

            // 倒计时
            let countdown = 60;
            let timer = setInterval(function () {
                if (countdown <= 0) {
                    $this.text('获取验证码');
                    // 清掉定时器
                    clearInterval(timer);
                    // 重新绑定点击事件
                    bindCaptchaBtnClick();
                } else {
                    countdown--;
                    $this.text(countdown + "s")
                }
            }, 1000);
        })
    }
    // 执行邦迪函数
    bindCaptchaBtnClick();
});