// 当浏览器完全加载页面中的所有内容（包括 HTML、CSS、图片、脚本、iframe 等外部资源）后，window.onload 会触发绑定的函数
window.onload = function () {
    const { createEditor, createToolbar } = window.wangEditor

    const editorConfig = {
        placeholder: 'Type here...',
        // 这里有一个监听事件，哟任何变化都会在这里打印
        onChange(editor) {
            const html = editor.getHtml()
            console.log('editor content', html)
            // 也可以同步到 <textarea>
        }
    }

    const editor = createEditor({
        selector: '#editor-container',
        html: '<p><br></p>',
        config: editorConfig,
        mode: 'default', // or 'simple'
    })

    const toolbarConfig = {}

    const toolbar = createToolbar({
        editor,
        selector: '#toolbar-container',
        config: toolbarConfig,
        mode: 'default', // or 'simple'
    })

    $("#submit-btn").click(function (event) {
        /*阻止按钮的默认行为: 
            如果不阻止默认行为，点击发布按钮，就会直接通过表单的形式发布给后端，
            但是富文本框里面的内容，是不能通过表单提交的*/
        event.preventDefault();
        // 找到input标签里面 name='title' 的 要素，然后 .val() 获取它的值
        let title = $("input[name='title']").val();
        // 找到id=category-select 的要是，然后 .val() 获取它的值
        // 用id的方式，要比前面那种方式快，因为id唯一
        let category = $("#category-select").val();
        //  这个方法只能获取文本，不能获取样式，如一级标题，二级标题
        // let content= editor.getText(); 
        // 这个方法可以获取样式
        let content = editor.getHtml();
        /**
         *  获取CSRF的token：
         *  使用{% csrf_token %} 渲染的结果是：
         *  <input type="hidden" name="csrfmiddlewaretoken" value="4nTc...A">
         */
        let csrfmiddlewaretoken = $("input[name='csrfmiddlewaretoken']").val();
        // 实际上只有两个参数：参数1 url=/blog/pub'； 参数2 opotion={}
        $.ajax('/blog/pub', {
            // 请求的方式
            method: 'POST',
            // 上传的数据
            data: { title, category, content, csrfmiddlewaretoken },
            success: function (result) {
                if (result['code'] == 200) {
                    // 获取博客id
                    let blog_id = result['data']['blog_id']
                    // 跳转到博客详情页面
                    window.location = '/blog/detail/' + blog_id
                } else {
                    alert(result['message']);
                }
            }
        })
    });
}