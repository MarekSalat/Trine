$(document).ready(function(){$('#project-progress').css('width','50%');$('#msgs-badge').addClass('animated bounceIn');$('#my-task-list').popover({html:true})
$('#styler-tab a').click(function(e){e.preventDefault();$(this).tab('show');});$('#styler .toggler').click(function(e){e.preventDefault();$('#styler').toggleClass('closed');});$('#styler .items').click(function(){$('#styler .items').removeClass('active');$(this).addClass('active');switcher($(this).attr('data-layout'));});$('#styler .themes').click(function(){$('#styler .themes').removeClass('active');$(this).addClass('active');themeSwitcher($(this).attr('data-theme'));});$('#chkRTL').change(function(){if($(this).is(":checked")){directionSwitcher("rtl");}
else{directionSwitcher("ltr");}});$('#chkBottomHeader').change(function(){if($(this).is(":checked")){$('body').addClass('bottom-header');}
else{$('body').removeClass('bottom-header');}});$('#chkRightSideBar').change(function(){if($(this).is(":checked")){$('body').addClass('right-side-bar');}
else{$('body').removeClass('right-side-bar');}});if($.cookie("layoutOption")!=='undefined')
switcher($.cookie("layoutOption"));else{switcher("default");defaultTheme();}
if($.cookie("theme")!=='undefined'){themeSwitcher($.cookie("theme"));}
else
themeSwitcher("default");if($.cookie("direction")!=='undefined')
directionSwitcher($.cookie("direction"));else
directionSwitcher("ltr");});function switcher(layout){$('#styler .items').removeClass('active');$(this).addClass('active');switch(layout){case"default":$("body").layoutReset();$('[data-layout="default"]').addClass('active');break;case"condensed-menu":$("body").layoutReset();$("body").condensMenu();$('[data-layout="condensed-menu"]').addClass('active');break;case"no-header":$("body").layoutReset();$("body").toggleHeader();$('[data-layout="no-header"]').addClass('active');break;case"no-sidebar":$("body").layoutReset();$("body").toggleMenu();$('[data-layout="no-sidebar"]').addClass('active');break;default:$("body").layoutReset();$('[data-layout="default"]').addClass('active');}
$.cookie("layoutOption",layout);$(".logo").trigger("unveil");};function themeSwitcher(theme){$('#styler .themes').removeClass('active');$(this).addClass('active');switch(theme){case"default":less.modifyVars({'@theme-name':'default','@direction':$.cookie("direction"),'@r-theme-name':'default'});$('[data-theme="default"]').addClass('active');defaultTheme();break;case"coporate":less.modifyVars({'@theme-name':'coporate','@direction':$.cookie("direction"),'@r-theme-name':'coporate'});$('[data-theme="coporate"]').addClass('active');coporateTheme();break;case"simple":less.modifyVars({'@theme-name':'simple','@direction':$.cookie("direction"),'@r-theme-name':'simple'});$('[data-theme="simple"]').addClass('active');simpleTheme();break;case"elegant":less.modifyVars({'@theme-name':'elegant','@direction':$.cookie("direction"),'@r-theme-name':'elegant'});$('[data-theme="elegant"]').addClass('active');elegantTheme();break;}
$.cookie("theme",theme);$(".logo").trigger("unveil");};function directionSwitcher(direction){if(typeof $.cookie("theme")==='undefined'||$.cookie("theme")==''){console.log($.cookie("theme"));$.cookie("theme","default");}
switch(direction){case"rtl":less.modifyVars({'@direction':'rtl','@theme-name':$.cookie("theme")});$('body').addClass('rtl');swapSidr('rtl');break;case"ltr":less.modifyVars({'@direction':'ltr','@theme-name':$.cookie("theme")});$('body').removeClass('rtl');swapSidr('ltr');break;}
$.cookie("direction",direction);};function defaultTheme(){color_green="#0aa699";color_blue="#00acec";color_yellow="#FDD01C";color_red="#f35958";color_grey="#dce0e8";color_black="#1b1e24";color_purple="#6d5eac";color_primary="#6d5eac";color_success="#4eb2f5";color_danger="#f35958";color_warning="#f7cf5e";color_info="#3b4751";$('.logo').each(function(){$(this).attr('src',"assets/img/logo.png");$(this).attr('data-src',"assets/img/logo.png");$(this).attr('data-src-retina',"assets/img/logo2x.png");});$(".craft-map-container").contents().find("body").css("background",color_green).find(".controls").css("background",color_green);}
function simpleTheme(){color_green="#27cebc";color_blue="#00acec";color_yellow="#FDD01C";color_red="#f35958";color_grey="#dce0e8";color_black="#1b1e24";color_purple="#6d5eac";color_primary="#6d5eac";color_success="#4eb2f5";color_danger="#f35958";color_warning="#f7cf5e";color_info="#3b4751";$('.logo').each(function(){$(this).attr('src',"assets/img/logo-b.png");$(this).attr('data-src',"assets/img/logo-b.png");$(this).attr('data-src-retina',"assets/img/logo-b2x.png");});$(".craft-map-container").contents().find("body").css("background",color_green).find(".controls").css("background",color_green);}
function coporateTheme(){color_green="#00bc9a";color_blue="#00acec";color_yellow="#FDD01C";color_red="#f35958";color_grey="#dce0e8";color_black="#1b1e24";color_purple="#6d5eac";color_primary="#6d5eac";color_success="#4eb2f5";color_danger="#f35958";color_warning="#f7cf5e";color_info="#3b4751";$('.logo').each(function(){$(this).attr('src',"assets/img/logo-b.png");$(this).attr('data-src',"assets/img/logo-b.png");$(this).attr('data-src-retina',"assets/img/logo-b2x.png");});$(".craft-map-container").contents().find("body").css("background",color_green).find(".controls").css("background",color_green);}
function elegantTheme(){color_green="#00cdb1";color_blue="#61acf2";color_yellow="#fae274";color_red="#ec7962";color_grey="#dce0e8";color_black="#1b1e24";color_purple="#7981d8";color_primary="#00cdb1";color_success="#61acf2";color_danger="#ec7962";color_warning="#fae274";color_info="#3b4751";$('.logo').each(function(){$(this).attr('src',"assets/img/logo.png");$(this).attr('data-src',"assets/img/logo.png");$(this).attr('data-src-retina',"assets/img/llogo2x.png");});$(".craft-map-container").contents().find("body").css("background",color_green).find(".controls").css("background",color_green);}
function swapSidr(){}