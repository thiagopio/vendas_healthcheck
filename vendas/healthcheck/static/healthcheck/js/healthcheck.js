/**
 * Created by thiago.pio on 9/27/15.
 */
 var healthcheck = function(){
    public = {},
    public.ok_class = 'project-green',
    public.problem_class = 'project-red',
    public.warn_class = 'project-yellow',
    $html_ul = $('<ul></ul>'),
    $html_site = $('<li>{url}</li>'),
    local_id = 'body',
    refresh_status_time = 5000;

    verify_dependents = function(data, status_class){
        var $dependent, $current = $('li[data-pk=' + data.id + ']');
        $current.attr('data-problem-pk', null);
        data.dependents_ids.every(function(value){
            $dependent = $('li[data-pk=' + value + ']');
            if (status_class == public.ok_class && !$dependent.is('.' + public.ok_class)) {
                status_class = public.warn_class;
                $current.attr('data-problem-pk', value);
                return;
            }
        });
        return status_class
    };

    update_status_class = function($html, data){
        var status_class = public.verify_status_class(data.working);
        $html.removeClass(public.ok_class);
        $html.removeClass(public.problem_class);
        $html.removeClass(public.warn_class);
        if (data.status != 404) {
            status_class = verify_dependents(data, status_class);
            $html.addClass(status_class);
        }
        public.update_project_name($html, data);
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

    public.verify_status_class = function(status){
        return status == true ? public.ok_class : public.problem_class;
    };

    public.update_project_name = function($html, data){
        var $problem_project, problem_project_id;
        if (data.working == true) {
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

    public.create_box_for = function(data){
        $html_clone = $html_site.clone();
        $html_clone.addClass('project');
        $html_clone.attr('data-pk', data.id);
        $html_clone.attr('data-name', data.name);
        update_status_class($html_clone, data);
        return $html_clone;
    };

    public.init = function(){
        $.getJSON( "/healthcheck/projects/all/json/", function( environment ) {
            $.each(environment, function(env, projects){
                var title = '<h2>' + env + '</h2>';
                var $html = $html_ul.clone().attr('id', env);
                $.each(projects, function(key, project) {
                    $project_item = public.create_box_for(project);
                    $html.append($project_item);
                });
                $(local_id).append(title, $html);
            });
            setTimeout(function(){ refresh_status() }, refresh_status_time);
        });
    };

    return public;
 }();
