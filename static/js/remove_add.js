var next_ingredient_button = document.getElementById('next-ingredient-button');
var delete_ingredient_button = document.getElementById('delete-ingredient-button');
var ingredient_section = document.getElementById('ingredient-section');

next_ingredient_button.onclick = function(){
    var nextIngredient = document.createElement('input');
    nextIngredient.setAttribute('type', 'text');
    nextIngredient.setAttribute('id', 'ingredients');
    nextIngredient.setAttribute('name', 'ingredients');
    nextIngredient.setAttribute('class', 'ingredient-input');
    nextIngredient.setAttribute('minlength', '4');
    nextIngredient.setAttribute('required', 'true');
    nextIngredient.setAttribute('placeholder', 'Another ingredient');
    ingredient_section.appendChild(nextIngredient);
};

delete_ingredient_button.onclick = function(){
    var ingredient_fields = document.getElementsByClassName('ingredient-input');
    if(ingredient_fields.length > 1) {
        ingredient_section.removeChild(ingredient_fields[(ingredient_fields.length) - 1]);
    }
};

var next_step_button = document.getElementById('next-step-button');
var delete_step_button = document.getElementById('delete-step-button');
var cooking_steps_section = document.getElementById('cooking-steps-section');

next_step_button.onclick = function(){
    var nextStep = document.createElement('textarea');
    nextStep.setAttribute('type', 'text');
    nextStep.setAttribute('id', 'cooking_steps');
    nextStep.setAttribute('name', 'cooking_steps');
    nextStep.setAttribute('class', 'materialize-textarea validate cooking_steps');
    nextStep.setAttribute('minlength', '4');
    nextStep.setAttribute('required', 'true');
    nextStep.setAttribute('placeholder', 'Another step');
    cooking_steps_section.appendChild(nextStep);
};

delete_step_button.onclick = function(){
    var step_fields = document.getElementsByClassName('cooking_steps');
    if(step_fields.length > 1) {
        cooking_steps_section.removeChild(step_fields[(step_fields.length) - 1]);
    }
};