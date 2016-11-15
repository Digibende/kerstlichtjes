//console.log = function() {}

$(function(){
    
    var canvas = $('#picker');
    canvas.attr('width', window.innerWidth);
    canvas.attr('height', window.innerHeight);
    var ctx = canvas[0].getContext('2d');
    var image = new Image();
    var color;
    var height;

    draw(canvas, ctx);
    $( window ).resize(function() {
        draw(canvas, ctx);
    });

    function draw(canvas, ctx, x, y) {
        var largest = Math.min(window.innerWidth, window.innerHeight);
        console.log("resize");
        canvas.attr('width', largest);
        canvas.attr('height', largest);
        height = parseInt(canvas.attr("height"));
        image.onload = function(){
            ctx.drawImage(image, 50, 50, height-100, height-100);
        };
        image.src = 'static/colorwheel4.png';
        ctx.beginPath();
        ctx.arc(height/2-50,height/2-50,height/2-50,0,2*Math.PI);
        ctx.lineWidth = 50;
        ctx.strokeStyle = 'green';
        ctx.stroke();
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
        
        ctx.beginPath();
        ctx.arc(height/2-50,height/2-50,height/2-50,0,2*Math.PI);
        ctx.lineWidth = 50;
        ctx.strokeStyle = pixelColor;
        ctx.stroke();
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