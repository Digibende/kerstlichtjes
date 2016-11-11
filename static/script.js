//console.log = function() {}

$(function(){
    
    var canvas = $('#picker');
    canvas.attr('width', window.innerWidth);
    canvas.attr('height', window.innerHeight);
    var ctx = canvas[0].getContext('2d');
    var image = new Image();
    var color;

    draw(canvas, ctx);
    $( window ).resize(function() {
        draw(canvas, ctx);
    });

    function draw(canvas, ctx, x, y) {
        var largest = Math.min(window.innerWidth, window.innerHeight);
        console.log("resize");
        canvas.attr('width', largest);
        canvas.attr('height', largest);
        var height = parseInt(canvas.attr("height"));
        image.onload = function(){
            ctx.drawImage(image, 0, 0, height, height);
        };
        image.src = 'static/colorwheel3.png';
        /*ctx.beginPath();
        ctx.arc(x,y,x+10,y+10,2*Math.PI);
        ctx.stroke();*/
    }

    $('#picker').mousedown(function(e) {
        process(e.pageX, e.pageY);
    });
    $('#picker').mousemove(function(e) {
        if(e.buttons==1){
            process(e.pageX, e.pageY);
        }
    });
    $("#picker").on("tap",function(){
        console.log("drag");
        var touch = e.originalEvent.touches[0] || e.originalEvent.changedTouches[0];
        process(Math.round(touch.pageX), Math.round(touch.pageY));
    });
    $('#picker').bind('touchmove',function(e){
        console.log("drag");
        var touch = e.originalEvent.touches[0] || e.originalEvent.changedTouches[0];
        //process(Math.round(touch.pageX), Math.round(touch.pageY));
    });

    $( "#picker" ).mouseup(function(e) {
        console.log("up");
        update();
    });

    function process(x, y){
        var canvasOffset = canvas.offset();
        var canvasX = Math.floor(x - canvasOffset.left);
        var canvasY = Math.floor(y - canvasOffset.top);
        console.log(canvasX + " " + canvasY);
        var imageData = ctx.getImageData(canvasX, canvasY, 1, 1);
        var pixel = imageData.data;
        color = rgbToHex(pixel);
        console.log(pixel);
        var pixelColor = "rgb("+pixel[0]+", "+pixel[1]+", "+pixel[2]+")";
        $('html').css('backgroundColor', pixelColor);
    }

    function update() {
        var location = document.location.href;
        if( location.slice(-1) != '/') {
            location = location + '/';
        }
        location = location + "color/" + color;
        console.log(location);
        $.ajax({
            url: location,
            context: document.body
        }).done(function() {
            console.log("done");
        });
    }

    //From http://stackoverflow.com/questions/5623838/rgb-to-hex-and-hex-to-rgb
    function componentToHex(c) {
        var hex = c.toString(16);
        return hex.length == 1 ? "0" + hex : hex;
    }

    function rgbToHex(pixel) {
        console.log(pixel)
        return componentToHex(pixel[0]) + componentToHex(pixel[1]) + componentToHex(pixel[2]);
    }
});