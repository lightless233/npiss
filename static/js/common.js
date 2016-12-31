/**
 * Created by lightless on 2016/12/28.
 */

function makeNoty(message, type="error", layout="top", cb=function(){}) {
    noty({
        text: message,
        theme: 'relax',
        type: type,
        layout: layout,
        animation: {
            open: {height: 'toggle'},
            close: {height: 'toggle'},
            easing: 'swing',
            speed: '500'
        },
        timeout: 3000,
        callback: {
            onShow: cb,
        }
    });
}

