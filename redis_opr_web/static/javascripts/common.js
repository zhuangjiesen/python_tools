/**
 * Created by zhuangjiesen on 2017/7/6.
 */
//模态框
function ModalDialog(options){
    dom_id = options.id;
    parentId = options.parentId;
    url = options.url;
    title = options.title;
    defaultOptions = {
        closeViaDimmer: 0,
        width: 800,
        height: 225
    }
    if (!options.width) {
        options.width = defaultOptions.width
    }
    if (!options.height) {
        options.height = defaultOptions.height
    }

    //模态框源码
    var dialog_content_temp = '<div class="am-modal am-modal-no-btn" tabindex="-1" id="'+ dom_id +'">' +
        '<div class="am-modal-dialog">' +
            '<div class="am-modal-hd"> modal-title-content' +
            '<a href="javascript: void(0)" class="am-close" data-am-modal-close>&times;</a>' +
            '</div>' +
            '<div  class="am-modal-bd">' +
            '<iframe id="modal-dialog-content-id"  frameborder="0" height="100%" width="100%" style="padding: 10px;" ></iframe>' +
            '</div>' +
            '</div>' +
        '</div>';

    var now = new Date();
    var dialog_content_id = dom_id + '-dialog-content' + '-' + now.getTime();
    dialog_content_temp = dialog_content_temp.replace(/modal-dialog-content-id/, dialog_content_id)
    if (title) {
        dialog_content_temp = dialog_content_temp.replace(/modal-title-content/, title)
    } else {
        dialog_content_temp = dialog_content_temp.replace(/modal-title-content/, '')
    }
    this.show = function () {
            if (url && url.length > 0) {
                 if (parentId && parentId.length > 0) {
                $('#' + parentId).append(dialog_content_temp)
                } else {
                    $('body').append(dialog_content_temp)
                }
                $('#' + dialog_content_id).attr('src' , url);
                 if (title) {
                     $('#' + dialog_content_id).height((options.height - 80) + 'px' );
                 } else {
                     $('#' + dialog_content_id).height((options.height - 50) + 'px' );
                 }


                $('#' + dom_id).off( "open.modal.amui")
                $('#' + dom_id).on('open.modal.amui', function() {
                    console.log('第一个演示弹窗打开了');

                    // $('#' + dialog_content_id).html(data);
                });
                $('#' + dom_id).on('closed.modal.amui', function(){
                    $('#' + dom_id).remove();
                });
                $('#' + dom_id).modal(options);
                $('#' + dom_id).modal('open');
                // $.get( url , function(data){
                //
                // });
            }
    };
    this.close = function () {
        $('#' + dom_id).modal('close');

    };
}