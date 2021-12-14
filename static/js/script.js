$(document).ready(function(){
    $('.sidenav').sidenav({edge: "right"});
    $('select').formSelect();
    $('textarea#synopsis, textarea#user_review').characterCounter();
    $(".dropdown-trigger").dropdown();
    $('.modal').modal();

    // code below to fix validation issue with materialize select element taken from Code Institute Mini project 
  validateMaterializeSelect();
  function validateMaterializeSelect() {
      let classValid = { "border-bottom": "1px solid #4caf50", "box-shadow": "0 1px 0 0 #4caf50" };
      let classInvalid = { "border-bottom": "1px solid #f44336", "box-shadow": "0 1px 0 0 #f44336" };
      if ($("select.validate").prop("required")) {
          $("select.validate").css({ "display": "block", "height": "0", "padding": "0", "width": "0", "position": "absolute" });
      }
      $(".select-wrapper input.select-dropdown").on("focusin", function () {
          $(this).parent(".select-wrapper").on("change", function () {
              if ($(this).children("ul").children("li.selected:not(.disabled)").on("click", function () { })) {
                  $(this).children("input").css(classValid);
              }
          });
      }).on("click", function () {
          if ($(this).parent(".select-wrapper").children("ul").children("li.selected:not(.disabled)").css("background-color") === "rgba(0, 0, 0, 0.03)") {
              $(this).parent(".select-wrapper").children("input").css(classValid);
          } else {
              $(".select-wrapper input.select-dropdown").on("focusout", function () {
                  if ($(this).parent(".select-wrapper").children("select").prop("required")) {
                      if ($(this).css("border-bottom") != "1px solid rgb(76, 175, 80)") {
                          $(this).parent(".select-wrapper").children("input").css(classInvalid);
                      }
                  }
              });
          }
      });
  }
});

// code to hide author column on add review page found on stack overflow https://stackoverflow.com/questions/15566999/how-to-show-form-input-fields-based-on-select-value
// code to remove required attribute from author name when hidden found on stack overflow https://stackoverflow.com/questions/10407622/addattr-not-working-in-jquery
$('#category_name').on('change', function(){
    if ($(this).val() === "Book"){
        $("#author-col").show();
        $("#author_name").prop('required', true);
        } 
    else {
        $("#author-col").hide();
        $("#author_name").prop('required', false);
    }
    }
);
