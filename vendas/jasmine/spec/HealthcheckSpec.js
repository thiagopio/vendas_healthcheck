describe("Healthcheck", function() {
  var h, json_project;

  beforeEach(function() {
   h = healthcheck;
   json_project = {"status": 200, "dependents_ids": [], "id": 1, "name": "google"};
  });

  describe("when verify status class", function() {
    it("should return problem class", function() {
      expect(h.fn_verify_status_class(500)).toEqual(h.attr_problem_class);
    });
    it("should return ok class", function() {
      expect(h.fn_verify_status_class(200)).toEqual(h.attr_ok_class);
    });
  });

  describe("when create box", function() {
    it("shoud return html", function() {
      html_expected = '<li class="project project-green" data-pk="1" data-name="google">google</li>';
      $html_returned = h.fn_create_box_for(json_project);
      expect($html_returned).toHaveClass('project ' + h.attr_ok_class);
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
      h.fn_update_project_name($html_success, json_project);
      expect($html_success.text()).toEqual(json_project['name']);
    });
  });
});