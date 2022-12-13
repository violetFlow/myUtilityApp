var pwCopyBtnObj = document.querySelectorAll('.pwCopyBtn')

pwCopyBtnObj.forEach(element => {
  element.addEventListener('click', (e) => {
    let value = e.target.id
    let index = value.replace('pwCopy','')
    let pwName = 'pwIndex'
    let targetId = pwName.concat(index)

    var pwObj = document.getElementById(targetId)
    console.log(pwObj.value)
    pwObj.select();
    document.execCommand("copy");
  })
});

var accountDeleteObj = document.querySelectorAll('.delete');

accountDeleteObj.forEach(elm => {
  elm.addEventListener('click', (e) => {
    const value = e.target.id;
    const accountId = value.replace('accountDelete','');
    const result = window.confirm('本当に消しますか。accountid:'+ accountId);

    if (result) {
      const req = '/account/delete/' + accountId;
      const result = fetch(req, {method: 'GET'});
      console.log(result);
      window.location.href='/'
    } 
  })
});
