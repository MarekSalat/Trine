/**
 * Created with PyCharm.
 * User: Marek
 * Date: 7.3.14
 * Time: 15:59
 * To change this template use File | Settings | File Templates.
 */


(function ($) {
    $.fn.getTextWidth = function () {
        var spanText = $("BODY #spanCalculateTextWidth");

        if (spanText.size() <= 0) {
            spanText = $("<span id='spanCalculateTextWidth' style='filter: alpha(0);'></span>");
            spanText.appendTo("BODY");
        }

        var valu = this.val();
        if (!valu) valu = this.text();

        spanText.text(valu);

        spanText.css({
            "fontSize": this.css('fontSize'),
            "fontWeight": this.css('fontWeight'),
            "fontFamily": this.css('fontFamily'),
            "position": "absolute",
            "top": 0,
            "opacity": 0,
            "left": -2000
        });

        return spanText.outerWidth() + parseInt(this.css('paddingLeft')) + 'px';
    };

    /**
     * Adjust the font-size of the text so it fits the container.
     *
     * @param minSize     Minimum font size?
     * @param maxSize     Maximum font size?
     */
    $.fn.autoTextSize = function (minSize, maxSize) {
        var _self = this,
            width = _self.innerWidth(),
            textWidth = parseInt(_self.getTextWidth()),
            fontSize = parseInt(_self.css('font-size'));


        for (var step = fontSize / 2; step > 0.5; step = step / 2) {
            if (textWidth < width)
                fontSize += step;
            else
                fontSize -= step;

            if (maxSize != null) fontSize = fontSize >= parseInt(maxSize) ? maxSize : fontSize;
            if (minSize != null) fontSize = fontSize <= parseInt(minSize) ? minSize : fontSize;

            _self.css('font-size', fontSize + 'px');
            _self.css('line-height: ', fontSize / 2 + 'px');
            textWidth = parseInt(_self.getTextWidth());
        }
    };
})
    (jQuery);