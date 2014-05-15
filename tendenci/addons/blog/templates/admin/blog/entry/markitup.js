{% load url from future %}
$(document).ready(function() {
  mySettings["previewParserPath"] = "{% url 'admin:blog_blogentry_markitup_preview' %}";
  $("#id_content").markItUp(mySettings);
});
