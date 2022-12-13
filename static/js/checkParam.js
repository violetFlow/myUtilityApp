var stayDateObj = document.getElementById('stayDate');
var submitButtonObj = document.getElementById('submitButton');


submitButtonObj.addEventListener('click', (e) => {
	// default event cancle
	e.preventDefault();


	if (stayDateObj.value.length > 0) {
		const stayDate = new Date(stayDateObj.value);
		const now = new Date();
		
	  console.log(stayDate);	
	  console.log(now);	
		if (now > stayDate) {
			alert('今日より未来の日付を選択してください。');
		} else {
			document.makeLinkForm.submit();
		}
	} else {
		alert('宿泊日を入力してください。');
	}

});
