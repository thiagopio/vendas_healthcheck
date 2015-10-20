describe("Healthcheck", function() {
  var h, json_project;

  beforeEach(function() {
    // http://www.michaelfalanga.com/2014/04/03/mock-jquery-ajax-calls-with-jasmine/
   h = healthcheck;
   json_project = {"info": 200, "working": true, "dependents_ids": [], "id": 1, "name": "google"};
  });

  describe("when verify status class", function() {
    it("should return problem_class for working is false", function() {
      expect(h.verify_status_class(false)).toEqual(h.problem_class);
    });
    it("should return ok_class for working is true", function() {
      expect(h.verify_status_class(true)).toEqual(h.ok_class);
    });
  });

  describe("when create box", function() {
    it("shoud return html with project information", function() {
      html_expected = '<li class="project project-green" data-pk="1" data-name="google">google</li>';
      $html_returned = h.create_box_for(json_project);
      expect($html_returned).toHaveClass('project ' + h.ok_class);
      expect($html_returned).toHaveData('pk', json_project['id']);
      expect($html_returned).toHaveData('name', json_project['name']);
      expect($html_returned).toHaveText(json_project['name']);
    });
  });

  describe("when update project name", function() {
    var $html_success;

    beforeEach(function() {
      $html_success = $('<li class="project" data-pk="1" data-name="google"></li>');
    });
    it("shoud change $html sent", function() {
      h.update_project_name($html_success, json_project);
      expect($html_success.text()).toEqual(json_project['name']);
    });
  });
});
