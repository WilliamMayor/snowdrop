$(document).ready(function() {
    $(".checkall").change(function() {
        $(".archive .check input").prop("checked", $(this).prop("checked"));
    });
    $(".archive .check input").change(function() {
        var all_on = true;
        var all_off = true;
        $(".archive .check input").each(function(i, input) {
            all_on &= $(input).prop("checked");
            all_off &= !$(input).prop("checked");
        });
        if (all_on) {
            $(".checkall").prop("checked", true);
        } else if (all_off) {
            $(".checkall").prop("checked", false);
        } else {
            $(".checkall").prop("checked", false);
            $(".checkall")[0].indeterminate = true;
        }
    });
    $(".actions .delete").click(function() {
        var aids = $.map($(".archive .check input:checked").parents(".archive"), function(a) {
            return $(a).data("aid");
        });
        if (aids.length > 0) {
            var check = "";
            var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
            for( var i=0; i < 5; i++ ) {
                check += possible.charAt(Math.floor(Math.random() * possible.length));
            }
            var sure = prompt("To confirm that you want to delete these archives type " + check + " here");
            if (sure === check) {
                $.ajax({
                    url: "/delete/",
                    type: "POST",
                    data: JSON.stringify({'aids': aids}),
                    contentType: "application/json; charset=utf-8"}).always(function() {
                        location.reload();
                });
            }
        }
        return false;
    });
});