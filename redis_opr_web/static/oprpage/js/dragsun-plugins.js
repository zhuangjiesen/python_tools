//自定义模态框组件
var DragsunModal = function (dom , options) {
    var _containerId = options.containerId || 'body';
    var _containerDom = null;
    if (_containerId == 'body') {
        _containerDom = $( _containerId);
    } else {
        _containerDom = $('#' + _containerId);
    }

    var _height = options.height || ''
    var _width = options.width || ''

    var _timeStamp = new Date().getTime();

    var modalId = 'modelTmp';
    var contentStyle = 'width: ' + _width + ';margin-left: auto; margin-right: auto;';
    contentStyle += 'height:' + _height + ';';

    var title = options.title || '';

    var contentHtml = '';
    var iframeId = null;
    if (options.url) {
        iframeId = modalId + '-' + _timeStamp + '-iframe'
        var contentWidth = _width - 30;
        contentHtml = '<iframe id="' + iframeId + '" frameborder="0" style=" width: 94%;position: absolute; margin: auto;left: 3%;right: 3%;" src="example.html"></iframe>';
    } else {
        contentHtml = options.html || '' ;
    }



    var html = '';
    html += '<div id="$modalId" class="modal fade in" tabindex="-1" >';
    html = html.replace("$modalId", modalId );

    html += '<div class="modal-content" style="$model-content-style">';
    html = html.replace("$model-content-style", contentStyle );

    html += '<div class="modal-header"> ';
    html += '<a class="close" data-dismiss="modal">×</a> ';
    html += '<h3>$title</h3> ';
    html = html.replace("$title", title );

    html += '</div> ';
    html += '<div class="modal-body" style="padding: 15px;position: relative;"> ';
    html += '$content';
    html = html.replace("$content", contentHtml );

    html += '</div> ';
    html += '<div class="modal-footer" style="    position: absolute;bottom: 0;right: 0;"  > ';
    var saveModalbtnId = null;
    if (options.saveButton) {
        html += '<a href="#"  id="$save-modalbtn" class="btn btn-success">确认</a> ';
        saveModalbtnId = modalId + '-' + _timeStamp + '-save-modalbtn';
        html = html.replace("$save-modalbtn", saveModalbtnId );
    }
    var cancelModalbtnId = null
    if (options.cancelButton) {
        html += '<a href="#" id="$cancel-modalbtn" class="btn" >关闭</a> ';
        cancelModalbtnId = modalId + '-' + _timeStamp + '-cancel-modalbtn';
        html = html.replace("$cancel-modalbtn", cancelModalbtnId );
    }

    html += '</div>';
    html += '</div>';
    html += '</div>';
//        alert(222 + ' html : ' + html);
    _containerDom.append(html);

    var _modelDom = $('#' + modalId );
    if (saveModalbtnId) {
        //确认按钮事件注册
        $('#' + saveModalbtnId).on('click' , function(){
            options.saveButton();
        });
    }
    if (cancelModalbtnId) {
        //取消按钮事件注册
        //确认按钮事件注册
        $('#' + cancelModalbtnId).on('click' , function(){
            options.cancelButton();

            _modelDom.modal('hide');
            setTimeout(function () {
                _modelDom.remove();
            } , 200);
        });
    }


    _modelDom.modal({
        backdrop: 'static',
        keyboard: false,//禁止键盘
        show:false
    });




    var $clone = _modelDom.clone().css('display','block').appendTo(_containerDom);
    var top = Math.round(($clone.height() - $clone.find('.modal-content').height()) / 2);
    top = top > 0 ? top : 0;
    $clone.remove();
    _modelDom.find('.modal-content').css("margin-top", top);


    _modelDom.on('show.bs.modal', function (e) {
        // if (iframeId) {
        //     debugger
        //     var _bodyWidth = _modelDom.find('.modal-body').width();
        //     $('#' + iframeId).width(_bodyWidth) ;
        // }
    })
    _modelDom.modal('show');


    //页面大小变化是仍然保证模态框水平垂直居中
    $(window).on('resize', centerModals);
    function centerModals() {
        $(modalId).each(function(i) {
            var $clone = $(this).clone().css('display','block').appendTo('body');
            var top = Math.round(($clone.height() - $clone.find('.modal-content').height()) / 2);
            top = top > 0 ? top : 0;
            $clone.remove();
            $(this).find('.modal-content').css("margin-top", top);
        });
    };


    //类的拓展方法
    $.extend(DragsunModal.prototype, {
        close: function () {
            _modelDom.modal('hide');
            setTimeout(function () {
                _modelDom.remove();
            } , 200);
        }

    })
};


$.fn.extend({
    dragsun_modal: function (options) {
        /*
         选择项
         {
         title : XXX,
         id : xxx ,
         html : xxx ,
         url : xxx ,
         height: xxx ,
         width : xxx  ,
         //成功按钮
         saveButton: function (){},
         // 关闭按钮
         cancelButton : function () {} ,
         position: xxx ,
         //父类容器id ,模态框展开的区域 ，默认body
         containerId : xxx


         }

         */
        return new DragsunModal( this , options);
    }
});

