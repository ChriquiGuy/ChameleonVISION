<script type="text/javascript">
$(document).ready(function(){
    //initially hide second h1
    $("h1:nth-child(2)").hide();

    function show_second_h1(){
        $("h1:nth-child(1)").hide();
        $("h1:nth-child(2)").show();
        setTimeout(show_first_h1,8000);
    }


    function show_first_h1(){
        $("h1:nth-child(1)").show();
        $("h1:nth-child(2)").hide();
        setTimeout(show_second_h1,3000);
    }

    setTimeout(show_second_h1,3000);
});
</script>
