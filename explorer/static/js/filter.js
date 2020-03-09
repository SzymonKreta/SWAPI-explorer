$(function(){
    $(".toggler").click(function () {
        console.log($(this).val());
        $(this).toggleClass('btn-primary');
        let columnClass = '.' + $(this).val();
        $(columnClass).toggle();
    });
});
