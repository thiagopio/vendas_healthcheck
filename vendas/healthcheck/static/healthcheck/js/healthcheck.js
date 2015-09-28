/**
 * Created by thiago.pio on 9/27/15.
 */
var Healthcheck = (function(){
    $html_ul = $('<ul></ul>');
    $html_site = $('<li>{url}</li>');
    refresh_status_time = 5000;
    ok_class = 'project-green';
    problem_class = 'project-red';

    verify_status_class = function(status){
        return status == 200 ? ok_class : problem_class;
    };

    update_status_class = function($html, data){
        var status_class = verify_status_class(data.status);
        $html.removeClass('project-red', 'project-green').addClass(status_class);
        update_project_name($html, data);
    };

    update_project_name = function($html, data){
        if (data.status == 200) {
            $html.text(data.name);
        } else {
            $html.text(data.name + ' (' + data.status + ')');
        }
    };

    replace_info_for = function(data){
        $html_clone = $html_site.clone();
        update_status_class($html_clone, data);
        $html_clone.addClass('project');
        $html_clone.data('project-id', data.id);
        return $html_clone;
    };

    refresh_status = function(){
        $.each($('.project'), function(key, project_tag){
            var $project = $(project_tag);
            var project_id = $project.data('project-id');
            $.getJSON( '/healthcheck/project/' + project_id + '/json/', function( response ) {
                console.log('updating... ', response);
                update_status_class($project, response)
            });
        });
        setTimeout(function(){ refresh_status() }, refresh_status_time);
        console.log('loading one more time... ' + (refresh_status_time / 1000) + ' seconds');
    };

    init = function(){
        $.getJSON( "/healthcheck/projects/all/json/", function( data ) {
            $.each(data, function(env, projects){
                var title = '<h1>' + env + '</h1>';
                var $html = $html_ul.clone().attr('id', env);
                $.each(projects, function(key, project) {
                    $project_item = replace_info_for(project)
                    $html.append($project_item);
                });
                $('body').append(title, $html);
            });
            setTimeout(function(){ refresh_status() }, refresh_status_time);
        });
    };

    return init();
}());