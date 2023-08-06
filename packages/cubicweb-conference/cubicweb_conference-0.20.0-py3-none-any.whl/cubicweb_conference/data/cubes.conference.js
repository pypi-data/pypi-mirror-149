// This contains template-specific javascript

$(function () {
    $(document).on('click', '.attendance .delete_attend', function (evt) {
        var $mynode = $(evt.currentTarget),
            $parentnode = $mynode.parents('.attendance'),
            eid = $parentnode.data('eid'),
            d = asyncRemoteExec('conference_delete_attend', eid);
        d.addCallback(function () {
            $('.attendance[data-eid=' + eid + ']').each(function() {
                var params = ajaxFuncArgs('render', null, 'ctxcomponents', 'attendance', eid);
                $(this).loadxhtml(AJAX_BASE_URL, params, null, 'swap');
            });
        });
        return false;
    });
});

$(function () {
    $(document).on('click', '.attendance .set_attend', function (evt) {
        var $mynode = $(evt.currentTarget),
            $parentnode = $mynode.parents('.attendance'),
            eid = $parentnode.data('eid'),
            d = asyncRemoteExec('conference_set_attend', eid);
        d.addCallback(function () {
            $('.attendance[data-eid=' + eid + ']').each(function() {
                var params = ajaxFuncArgs('render', null, 'ctxcomponents', 'attendance', eid);
                $(this).loadxhtml(AJAX_BASE_URL, params, null, 'swap');
            });
        });
        return false;
    });
});
