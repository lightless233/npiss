/**
 * Created by lightless on 2016/12/28.
 */

function makeNoty(message, cb=function(){}, type="error", layout="top") {
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

