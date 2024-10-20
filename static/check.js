document.getElementById("checkCapsuleForm").addEventListener("submit", function(e) {
    checkCapsule(this.getAttribute("method"), this.getAttribute("action"), new FormData(this));
    e.preventDefault();
  });

  window.contentType = 'application/xml';

  function payload(data) {
    var xml = '<?xml version="1.0" encoding="UTF-8"?>';
    xml += '<redservice>';
  
    for(var pair of data.entries()) {
        var key = pair[0];
        var value = pair[1];
  
        xml += '<' + key + '>' + value + '</' + key + '>';
    }
  
    xml += '</redservice>';
    return xml;
  }
  
  function checkCapsule(method, path, data) {
    const retry = (tries) => tries == 0
        ? null
        : fetch(
            path,
            {
                method,
                headers: { 'Content-Type': window.contentType },
                body: payload(data)
            }
          )
            .then(res => res.status === 200
                ? res.text().then(t => isNaN(t) ? t : t + " units")
                : "Could not fetch capsule!"
            )
  
    retry(3);
  }