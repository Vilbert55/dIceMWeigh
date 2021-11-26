function render_template(_template,data,fields){
    for (var fd in data){
      if ((fields.length==0)||(fields.indexOf(fd)>=0)){
        const rx = new RegExp("{"+fd+"}","gi");
        _template = _template.replace(rx,data[fd]);
      }
    }
  return _template;  
}
