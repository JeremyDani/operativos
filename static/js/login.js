// Small scripts to enhance login interactions
document.addEventListener('DOMContentLoaded', function(){
  // Add class when inputs have value (for styling if needed)
  document.querySelectorAll('.card-body input[type="text"], .card-body input[type="password"], .card-body input[type="email"]').forEach(function(inp){
    function update(){
      if(inp.value && inp.value.trim()!="") inp.classList.add('has-value'); else inp.classList.remove('has-value');
    }
    inp.addEventListener('input', update);
    update();
  });

  // Simple enter-to-submit support for forms inside login
  document.querySelectorAll('.card-body form').forEach(function(form){
    form.addEventListener('keydown', function(e){
      if(e.key === 'Enter'){
        // find submit button and click
        const btn = form.querySelector('button[type="submit"], input[type="submit"]');
        if(btn){ btn.classList.add('pressed'); btn.click(); }
      }
    });
  });

});
