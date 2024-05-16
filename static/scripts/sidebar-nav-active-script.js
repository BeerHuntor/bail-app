$(document).ready(function() {
    $(".nav-link").click(function() {
        //Remove all 'active' class from all nav links
        $(".nav-link").removeClass("active");
        //Add 'active' class to the clicked nav link
        $(this).addClass("active");
        // If the clicked link is 'Bails', set 'active-tab' to 'bail-search'
        if ($(this).attr("href") === "#nestedNav1") {
            active_tab = 'bail_search';
        }
    });

    const params = new URLSearchParams(window.location.search);
    const modal = params.get('modal');

    if (modal == 'success') {
        console.log("Showing Success Modal");
        $('#reg_modal_success').modal('show');
    } else {
        console.log("Success modal parameter not found or incorrect!");
    }
});