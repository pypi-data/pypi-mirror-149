$(document).ready(function () {
    // var str1 = '<div>beforebegin - 插入到元素自身的前面</div>';
    // var str2 = '<div>afterbegin - 插入元素内部的第一个子节点之前</div>';
    // var str3 = '<div>beforeend - 插入元素内部的最后一个子节点之后</div>';
    // var str4 = '<div>afterend - 元素自身的后面</div>';
    // var box = document.querySelector('#box');
    // box.insertAdjacentHTML('beforebegin', str1);
    // box.insertAdjacentHTML('afterbegin', str2);
    // box.insertAdjacentHTML('beforeend', str3);
    // box.insertAdjacentHTML('afterend', str4);
    // 创建富文本编辑器元素节点
    var wehtml = "<div id='wangcontent'></div>"
    // 获取的div
    var field_div = document.querySelectorAll(".field-content>div")
    field_div[0].insertAdjacentHTML('afterbegin', '<b>商品详情：</b>');
    field_div[0].insertAdjacentHTML('beforeend', wehtml);
    $(".field-content>div>label").attr('style', 'display:none')
    
    const E = window.wangEditor
    const editor = new E("#wangcontent")
    // 或者 const editor = new E( document.getElementById('div1') )
    const $text1 = $('#id_content')
    console.log($text1.val())
    editor.config.onchange = function (html) {
        // 第二步，监控变化，同步更新到 textarea
        $text1.val(html)
    }

    editor.config.height = 500
    // 配置 server 接口地址
    editor.config.uploadImgServer = '/happy/upload_img/'
    editor.config.uploadFileName = 'spuImg'
    editor.create()
    editor.txt.html($text1.val())
    // 第一步，初始化 textarea 的值
    $text1.val(editor.txt.html())
    $text1.attr("style","display:none")
    
})
