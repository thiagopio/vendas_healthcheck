/**
 * Created by thiago.pio on 9/27/15.
 */
 var healthcheck = function(){
    $html_ul = $('<ul></ul>');
    $html_site = $('<li>{url}</li>');
    refresh_status_time = 5000;
    ok_class = 'project-green';
    problem_class = 'project-red';
    warn_class = 'project-yellow';

    verify_status_class = function(status){
        return status == 200 ? ok_class : problem_class;
    };

    verify_dependents = function(data, status_class){
        var $dependent, $current = $('li[data-pk=' + data.id + ']');
        $current.attr('data-problem-pk', null);
        data.dependents_ids.every(function(value){
            $dependent = $('li[data-pk=' + value + ']');
            if (status_class == ok_class && !$dependent.is('.' + ok_class)) {
                status_class = warn_class;
                $current.attr('data-problem-pk', value);
                return;
            }
        });
        return status_class
    };

    update_status_class = function($html, data){
        var status_class = verify_status_class(data.status);
        $html.removeClass(ok_class);
        $html.removeClass(problem_class);
        $html.removeClass(warn_class);
        if (data.status != 404) {
            status_class = verify_dependents(data, status_class);
            $html.addClass(status_class);
        }
        update_project_name($html, data);
    };

    update_project_name = function($html, data){
        var $problem_project, problem_project_id;
        if (data.status == 200) {
            $html.text(data.name);
            problem_project_id = $html.attr('data-problem-pk');
            if (problem_project_id !== undefined){
                $problem_project = $('li[data-pk=' + problem_project_id + ']');
                $html.append('<small>' + $problem_project.data('name') + '</small>');
            }
        } else {
            $html.text(data.name + ' (' + data.status + ')');
        }
    };

    refresh_status = function(){
        $.each($('.project'), function(key, project_tag){
            var $project = $(project_tag);
            var project_id = $project.data('pk');
            $.getJSON( '/healthcheck/project/' + project_id + '/json/', function( response ) {
                update_status_class($project, response)
            });
        });
        setTimeout(function(){ refresh_status() }, refresh_status_time);
    };

    create_box_for = function(data){
        $html_clone = $html_site.clone();
        $html_clone.addClass('project');
        $html_clone.attr('data-pk', data.id);
        $html_clone.attr('data-name', data.name);
        update_status_class($html_clone, data);
        return $html_clone;
    };

    init = function(){
        $.getJSON( "/healthcheck/projects/all/json/", function( environment ) {
            $.each(environment, function(env, projects){
                var title = '<h2>' + env + '</h2>';
                var $html = $html_ul.clone().attr('id', env);
                $.each(projects, function(key, project) {
                    $project_item = create_box_for(project);
                    $html.append($project_item);
                });
                $('body').append(title, $html);
            });
            setTimeout(function(){ refresh_status() }, refresh_status_time);
        });
    };

    return {
        'attr_ok_class': ok_class,
        'attr_problem_class': problem_class,
        'fn_verify_status_class': verify_status_class,
        'fn_create_box_for': create_box_for,
        'fn_update_project_name': update_project_name,
        'init': init
    }
 }();
