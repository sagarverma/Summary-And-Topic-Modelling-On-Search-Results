
$(function() {
    //hang on event of form with id=myform
    $("#searchForm").submit(function(e) {

        //prevent Default functionality
        e.preventDefault();

        //get the action-url of the form
        var actionurl = e.currentTarget.action;

        //do your own request an handle the results
        $.ajax({
                url: "/search",
                type: 'post',
                dataType: 'json',
                data: $("#searchForm").serialize(),
                success: function(data) {
                    $('#nav').empty();
                    var dict = data['result']
                    //console.log(dict)
                    var links = Object.keys(dict)
                    //console.log(links)
                    var table = "<table id='searchResTable'><th>#</th><th>Results</th>";

                    var i = 0
                    for(link in dict){
                        //console.log(link)
                        table += "<tr><td>"+(i+1)+"</td><td><a href='"+ link + "' target='_blank'>" + link + "</a><br><p><i>Topics : " + dict[link].slice(1, 10).toString() + "</i></p><br><p><b>Summary : " + dict[link][0] + "</b></p></td></tr>";
                        i += 1
                    }

                    $("#nav").append(table);
                }
        });

    });

});
